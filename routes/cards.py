from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from models import db, Desk, Card, CardReview, UserCardProgress
import os
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage

cards_bp = Blueprint('cards', __name__, url_prefix='/cards')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = 'uploads/desks'

def allowed_file(filename):
    """Check if file is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@cards_bp.route('/simple', methods=['GET'])
@login_required
def play_simple():
    """Display desks with cards using simplified template"""
    desk_id = request.args.get('desk_id', type=int)
    
    if desk_id:
        # Show cards for a specific desk with flip card interface
        desk = Desk.query.get(desk_id)
        if not desk:
            flash('Desk not found', 'error')
            return redirect(url_for('cards.play_simple', desk_id=None))
        
        cards = Card.query.filter_by(desk_id=desk_id).order_by(Card.order.asc()).all()
        
        # Get completed card IDs for current user
        completed_card_ids = [
            review.card_id for review in CardReview.query.filter_by(user_id=current_user.id).filter(
                CardReview.card_id.in_([c.id for c in cards]),
                CardReview.is_correct == True
            ).all()
        ]
        
        # Get due cards (cards that need review)
        now = datetime.utcnow()
        due_card_ids = [
            review.card_id for review in CardReview.query.filter_by(user_id=current_user.id).filter(
                CardReview.card_id.in_([c.id for c in cards]),
                CardReview.next_review_at <= now
            ).all()
        ]
        
        # Prepare cards data for JavaScript
        cards_data = []
        for card in cards:
            cards_data.append({
                'id': card.id,
                'name': card.answer,
                'img': card.example,
                'question': card.question,
                'answer': card.answer,
                'pronunciation': card.pronunciation or '',
                'example': card.example or ''
            })
        
        return render_template('cards/play_simple.html',
                             desk=desk,
                             cards=cards,
                             cards_json_data=cards_data,
                             completed_ids=completed_card_ids,
                             due_ids=due_card_ids)
    else:
        # Show list of desks
        desks = Desk.query.order_by(Desk.id.asc()).all()
        
        # Get desk progress
        desk_progresses = {}
        for desk in desks:
            total_cards = Card.query.filter_by(desk_id=desk.id).count()
            completed_reviews = CardReview.query.join(Card).filter(
                Card.desk_id == desk.id,
                CardReview.user_id == current_user.id,
                CardReview.is_correct == True
            ).count()
            
            desk_progresses[desk.id] = {
                'total': total_cards,
                'completed': completed_reviews,
                'percentage': (completed_reviews / total_cards * 100) if total_cards > 0 else 0
            }
        
        return render_template('cards/index.html',
                             desks=desks,
                             desk_progresses=desk_progresses)

@cards_bp.route('/', methods=['GET'])
@login_required
def play():
    """Display desks with cards for user to play"""
    desk_id = request.args.get('desk_id', type=int)
    
    if desk_id:
        # Show cards for a specific desk with flip card interface
        desk = Desk.query.get(desk_id)
        if not desk:
            flash('Desk not found', 'error')
            return redirect(url_for('cards.play'))
        
        cards = Card.query.filter_by(desk_id=desk_id).order_by(Card.order.asc()).all()
        
        # Get completed card IDs for current user
        completed_card_ids = [
            review.card_id for review in CardReview.query.filter_by(user_id=current_user.id).filter(
                CardReview.card_id.in_([c.id for c in cards]),
                CardReview.is_correct == True
            ).all()
        ]
        
        # Get due cards (cards that need review)
        now = datetime.utcnow()
        due_card_ids = [
            review.card_id for review in CardReview.query.filter_by(user_id=current_user.id).filter(
                CardReview.card_id.in_([c.id for c in cards]),
                CardReview.next_review_at <= now
            ).all()
        ]
        
        # Prepare cards data for JavaScript
        cards_data = []
        for card in cards:
            cards_data.append({
                'id': card.id,
                'name': card.answer,  # Show answer on back
                'img': card.example,   # Show image URL on front
                'question': card.question,
                'answer': card.answer,
                'pronunciation': card.pronunciation or '',
                'example': card.example or ''
            })
        
        # Use simplified template with better data passing
        return render_template('cards/play_simple.html',
                             desk=desk,
                             cards=cards,
                             cards_json_data=cards_data,
                             completed_ids=completed_card_ids,
                             due_ids=due_card_ids)
    else:
        # Show list of desks
        desks = Desk.query.order_by(Desk.id.asc()).all()
        
        # Get desk progress
        desk_progresses = {}
        for desk in desks:
            total_cards = Card.query.filter_by(desk_id=desk.id).count()
            completed_reviews = CardReview.query.join(Card).filter(
                Card.desk_id == desk.id,
                CardReview.user_id == current_user.id,
                CardReview.is_correct == True
            ).count()
            
            desk_progresses[desk.id] = {
                'total': total_cards,
                'completed': completed_reviews,
                'percentage': (completed_reviews / total_cards * 100) if total_cards > 0 else 0
            }
        
        return render_template('cards/index.html',
                             desks=desks,
                             desk_progresses=desk_progresses)

@cards_bp.route('/card/<int:card_id>', methods=['GET'])
@login_required
def get_card(card_id):
    """Get a specific card"""
    card = Card.query.get(card_id)
    if not card:
        return jsonify({'error': 'Card not found'}), 404
    
    return jsonify({
        'id': card.id,
        'question': card.question,
        'answer': card.answer,
        'example': card.example
    })

@cards_bp.route('/review', methods=['POST'])
@login_required
def review_card():
    """Review/answer a card"""
    data = request.get_json() or {}
    card_id = data.get('card_id')
    is_correct = data.get('is_correct', False)
    
    # Convert card_id to int
    try:
        card_id = int(card_id)
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid card_id'}), 400
    
    if not card_id:
        return jsonify({'error': 'Invalid card_id'}), 400
    
    # Check if card exists
    card = Card.query.get(card_id)
    if not card:
        return jsonify({'error': 'Card not found'}), 404
    
    # Get or create review record
    review = CardReview.query.filter_by(
        user_id=current_user.id,
        card_id=card_id
    ).first()
    
    if not review:
        review = CardReview(
            user_id=current_user.id,
            card_id=card_id,
            is_correct=is_correct,
            review_stage=0
        )
        db.session.add(review)
    else:
        review.is_correct = is_correct
    
    # Schedule next review (spaced repetition)
    intervals = {
        0: 1,      # 1 minute
        1: 10,     # 10 minutes
        2: 1440,   # 1 day
        3: 10080,  # 7 days
    }
    
    next_stage = review.review_stage + 1
    next_minutes = intervals.get(next_stage, 10080)
    review.review_stage = next_stage
    review.next_review_at = datetime.utcnow() + timedelta(minutes=next_minutes)
    
    db.session.commit()
    
    return jsonify({
        'ok': True,
        'next_review_at': review.next_review_at.isoformat()
    })

@cards_bp.route('/complete', methods=['POST'])
@login_required
def complete():
    """Mark a desk as completed (legacy endpoint)"""
    data = request.get_json() or {}
    desk_id = data.get('desk_id')
    
    if not desk_id or not isinstance(desk_id, int):
        return jsonify({'error': 'Invalid desk_id'}), 400
    
    # Check if desk exists
    desk = Desk.query.get(desk_id)
    if not desk:
        return jsonify({'error': 'Desk not found'}), 404
    
    # Get or create progress record
    progress = UserCardProgress.query.filter_by(
        user_id=current_user.id,
        desk_id=desk_id
    ).first()
    
    if not progress:
        progress = UserCardProgress(
            user_id=current_user.id,
            desk_id=desk_id
        )
        db.session.add(progress)
    
    # Schedule review
    if progress.completed_at is None:
        progress.completed_at = datetime.utcnow()
        progress.review_stage = 1
        progress.next_review_at = datetime.utcnow() + timedelta(minutes=10)
    else:
        stage = progress.review_stage or 0
        
        if stage < 1:
            stage = 1
        
        if stage == 1:
            progress.review_stage = 2
            progress.next_review_at = datetime.utcnow() + timedelta(minutes=10)
        elif stage == 2:
            progress.review_stage = 3
            progress.next_review_at = datetime.utcnow() + timedelta(days=1)
        else:
            progress.review_stage = 4
            progress.next_review_at = None
    
    db.session.commit()
    return jsonify({'ok': True})
