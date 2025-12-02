#!/usr/bin/env python
"""Quiz routes"""
from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import login_required, current_user
from models import db, Quiz, QuizQuestion, QuizAnswer, UserQuizAnswer, QuizAttempt
from datetime import datetime

quiz_bp = Blueprint('quiz', __name__, url_prefix='/quiz')

@quiz_bp.route('/')
@login_required
def index():
    """List all quizzes"""
    quizzes = Quiz.query.all()
    user_attempts = {}
    
    for quiz in quizzes:
        attempts = QuizAttempt.query.filter_by(user_id=current_user.id, quiz_id=quiz.id).all()
        user_attempts[quiz.id] = {
            'count': len(attempts),
            'last_attempt': attempts[-1] if attempts else None,
            'best_score': max([a.percentage for a in attempts]) if attempts else 0
        }
    
    return render_template('quiz/index.html', quizzes=quizzes, user_attempts=user_attempts)

@quiz_bp.route('/<int:quiz_id>')
@login_required
def detail(quiz_id):
    """Quiz detail page"""
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = QuizQuestion.query.filter_by(quiz_id=quiz_id).order_by(QuizQuestion.order).all()
    
    user_attempts = QuizAttempt.query.filter_by(user_id=current_user.id, quiz_id=quiz_id).all()
    
    return render_template('quiz/detail.html', quiz=quiz, questions=questions, user_attempts=user_attempts)

@quiz_bp.route('/<int:quiz_id>/play')
@login_required
def play(quiz_id):
    """Play quiz"""
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = QuizQuestion.query.filter_by(quiz_id=quiz_id).order_by(QuizQuestion.order).all()
    
    if not questions:
        return redirect(url_for('quiz.detail', quiz_id=quiz_id))
    
    # Prepare answers for each question - convert to dictionaries for JSON serialization
    quiz_data = []
    for question in questions:
        answers = QuizAnswer.query.filter_by(question_id=question.id).order_by(QuizAnswer.order).all()
        quiz_data.append({
            'question': {
                'id': question.id,
                'text': question.question_text
            },
            'answers': [
                {
                    'id': answer.id,
                    'text': answer.answer_text
                }
                for answer in answers
            ]
        })
    
    return render_template('quiz/play.html', quiz=quiz, quiz_data=quiz_data)

@quiz_bp.route('/<int:quiz_id>/submit', methods=['POST'])
@login_required
def submit(quiz_id):
    """Submit quiz answers"""
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = QuizQuestion.query.filter_by(quiz_id=quiz_id).all()
    
    data = request.get_json()
    answers = data.get('answers', {})
    
    # Calculate score
    score = 0
    total = len(questions)
    
    # Clear previous answers for this user (if restarting)
    UserQuizAnswer.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()
    
    for question_id, selected_answer_id in answers.items():
        question_id = int(question_id)
        selected_answer_id = int(selected_answer_id) if selected_answer_id else None
        
        question = QuizQuestion.query.get(question_id)
        if not question or question.quiz_id != quiz_id:
            continue
        
        is_correct = False
        selected_answer = None
        
        if selected_answer_id:
            selected_answer = QuizAnswer.query.get(selected_answer_id)
            if selected_answer and selected_answer.is_correct:
                is_correct = True
                score += 1
        
        # Save user answer
        user_answer = UserQuizAnswer(
            user_id=current_user.id,
            question_id=question_id,
            selected_answer_id=selected_answer_id,
            is_correct=is_correct
        )
        db.session.add(user_answer)
    
    # Create quiz attempt
    percentage = (score / total * 100) if total > 0 else 0
    attempt = QuizAttempt(
        user_id=current_user.id,
        quiz_id=quiz_id,
        score=score,
        total_questions=total,
        percentage=percentage,
        completed_at=datetime.utcnow()
    )
    db.session.add(attempt)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'quiz_id': quiz_id,
        'attempt_id': attempt.id,
        'score': score,
        'total': total,
        'percentage': round(percentage, 2)
    })

@quiz_bp.route('/<int:quiz_id>/result/<int:attempt_id>')
@login_required
def result(quiz_id, attempt_id):
    """View quiz result"""
    quiz = Quiz.query.get_or_404(quiz_id)
    attempt = QuizAttempt.query.get_or_404(attempt_id)
    
    if attempt.user_id != current_user.id or attempt.quiz_id != quiz_id:
        return redirect(url_for('quiz.index'))
    
    questions = QuizQuestion.query.filter_by(quiz_id=quiz_id).order_by(QuizQuestion.order).all()
    
    result_data = []
    for question in questions:
        user_answer = UserQuizAnswer.query.filter_by(
            user_id=current_user.id,
            question_id=question.id
        ).first()
        
        answers = QuizAnswer.query.filter_by(question_id=question.id).all()
        correct_answer = next((a for a in answers if a.is_correct), None)
        
        result_data.append({
            'question': question,
            'answers': answers,
            'user_answer': user_answer,
            'correct_answer': correct_answer
        })
    
    return render_template('quiz/result.html', quiz=quiz, attempt=attempt, result_data=result_data)
