#!/usr/bin/env python
"""Script để thêm bộ quiz mới"""

from app import create_app
from models import db, Quiz, QuizQuestion, QuizAnswer

def add_quiz(quiz_title, quiz_description, questions_data):
    """
    Thêm bộ quiz mới
    
    Args:
        quiz_title: Tên quiz (VD: "English Vocabulary Basics")
        quiz_description: Mô tả quiz
        questions_data: List các câu hỏi trong format:
                        [
                            {
                                'question': 'Nội dung câu hỏi',
                                'answers': [
                                    {'text': 'Đáp án A', 'is_correct': False},
                                    {'text': 'Đáp án B', 'is_correct': True},
                                    {'text': 'Đáp án C', 'is_correct': False},
                                    {'text': 'Đáp án D', 'is_correct': False},
                                ]
                            },
                            ...
                        ]
    
    Example:
        questions = [
            {
                'question': 'What is the opposite of "big"?',
                'answers': [
                    {'text': 'small', 'is_correct': True},
                    {'text': 'large', 'is_correct': False},
                    {'text': 'huge', 'is_correct': False},
                    {'text': 'tall', 'is_correct': False},
                ]
            },
            ...
        ]
        add_quiz('English Vocab', 'Test your vocabulary', questions)
    """
    
    app = create_app()
    
    with app.app_context():
        # Kiểm tra xem quiz đã tồn tại chưa
        existing_quiz = Quiz.query.filter_by(title=quiz_title).first()
        if existing_quiz:
            print(f"❌ Quiz '{quiz_title}' đã tồn tại!")
            return
        
        # Tạo Quiz mới
        print(f"📝 Tạo quiz '{quiz_title}'...")
        quiz = Quiz(
            title=quiz_title,
            description=quiz_description,
            category='Vocabulary'
        )
        db.session.add(quiz)
        db.session.flush()  # Để lấy quiz.id
        
        # Thêm các câu hỏi
        print(f"❓ Thêm {len(questions_data)} câu hỏi...")
        for order, q_data in enumerate(questions_data, 1):
            question = QuizQuestion(
                quiz_id=quiz.id,
                question_text=q_data['question'],
                question_type='multiple_choice',
                order=order
            )
            db.session.add(question)
            db.session.flush()  # Để lấy question.id
            
            # Thêm các đáp án
            for answer_order, answer_data in enumerate(q_data['answers'], 1):
                answer = QuizAnswer(
                    question_id=question.id,
                    answer_text=answer_data['text'],
                    is_correct=answer_data['is_correct'],
                    order=answer_order
                )
                db.session.add(answer)
        
        # Lưu vào database
        db.session.commit()
        
        print(f"✅ Quiz '{quiz_title}' được tạo thành công!")
        print(f"   📊 Quiz ID: {quiz.id}")
        print(f"   🎯 Questions added: {len(questions_data)}")
        print(f"   📌 Total answers: {len(questions_data) * 4}")


if __name__ == '__main__':
    # ==========================================
    # VÍ DỤ: Thêm quiz "SPORTS VOCABULARY"
    # ==========================================
    
    sports_quiz_questions = [
        {
            'question': 'What sport uses a ball and a racket?',
            'answers': [
                {'text': 'Tennis', 'is_correct': True},
                {'text': 'Football', 'is_correct': False},
                {'text': 'Swimming', 'is_correct': False},
                {'text': 'Running', 'is_correct': False},
            ]
        },
        {
            'question': 'Which sport is played in a pool?',
            'answers': [
                {'text': 'Basketball', 'is_correct': False},
                {'text': 'Swimming', 'is_correct': True},
                {'text': 'Boxing', 'is_correct': False},
                {'text': 'Golf', 'is_correct': False},
            ]
        },
        {
            'question': 'What is the opposite sport of "Swimming"?',
            'answers': [
                {'text': 'Running', 'is_correct': False},
                {'text': 'Flying', 'is_correct': False},
                {'text': 'Walking', 'is_correct': False},
                {'text': 'None - all are different', 'is_correct': True},
            ]
        },
        {
            'question': 'Which sport involves hitting a ball with a club?',
            'answers': [
                {'text': 'Tennis', 'is_correct': False},
                {'text': 'Golf', 'is_correct': True},
                {'text': 'Badminton', 'is_correct': False},
                {'text': 'Cricket', 'is_correct': False},
            ]
        },
        {
            'question': 'What is the main equipment in Basketball?',
            'answers': [
                {'text': 'Racket', 'is_correct': False},
                {'text': 'Ball', 'is_correct': True},
                {'text': 'Stick', 'is_correct': False},
                {'text': 'Gloves', 'is_correct': False},
            ]
        },
        {
            'question': 'Which sport is played on ice?',
            'answers': [
                {'text': 'Football', 'is_correct': False},
                {'text': 'Ice Skating', 'is_correct': True},
                {'text': 'Volleyball', 'is_correct': False},
                {'text': 'Badminton', 'is_correct': False},
            ]
        },
        {
            'question': 'What do you wear when cycling?',
            'answers': [
                {'text': 'Helmet', 'is_correct': True},
                {'text': 'Swimsuit', 'is_correct': False},
                {'text': 'Skates', 'is_correct': False},
                {'text': 'Gloves only', 'is_correct': False},
            ]
        },
        {
            'question': 'Which sport requires a net?',
            'answers': [
                {'text': 'Tennis', 'is_correct': True},
                {'text': 'Golf', 'is_correct': False},
                {'text': 'Boxing', 'is_correct': False},
                {'text': 'Running', 'is_correct': False},
            ]
        },
        {
            'question': 'What is the ball used in Football called?',
            'answers': [
                {'text': 'Sphere', 'is_correct': False},
                {'text': 'Round', 'is_correct': False},
                {'text': 'Soccer ball', 'is_correct': True},
                {'text': 'Oval', 'is_correct': False},
            ]
        },
        {
            'question': 'How many players are usually on a Basketball team on court?',
            'answers': [
                {'text': '3', 'is_correct': False},
                {'text': '5', 'is_correct': True},
                {'text': '7', 'is_correct': False},
                {'text': '9', 'is_correct': False},
            ]
        },
    ]
    
    # Thêm quiz "Sports Vocabulary"
    add_quiz(
        'Sports Vocabulary Quiz',
        'Test your knowledge about sports terminology and rules',
        sports_quiz_questions
    )
    
    # ==========================================
    # TẠO THÊM QUIZ KHÁC
    # ==========================================
    # Uncomment dòng dưới để thêm quiz khác:
    
    # food_quiz_questions = [
    #     {
    #         'question': 'What is a popular Italian pasta?',
    #         'answers': [
    #             {'text': 'Spaghetti', 'is_correct': True},
    #             {'text': 'Kimchi', 'is_correct': False},
    #             {'text': 'Sushi', 'is_correct': False},
    #             {'text': 'Burrito', 'is_correct': False},
    #         ]
    #     },
    #     ...
    # ]
    # add_quiz('Food & Cuisine Quiz', 'Learn about international food', food_quiz_questions)
