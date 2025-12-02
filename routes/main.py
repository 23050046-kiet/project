from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models import db, Desk, User, UserCardProgress, Card, CardReview
from sqlalchemy import func

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Welcome page"""
    return render_template('welcome.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    """User dashboard with progress data"""
    user = current_user
    
    # Total cards and completed
    total_cards = Card.query.count()
    completed_cards = CardReview.query.filter_by(
        user_id=user.id,
        is_correct=True
    ).count()
    
    # Get top desks
    top_desks = db.session.query(
        Desk.id,
        Desk.name_en,
        func.count(CardReview.id).label('reviews')
    ).join(Card, Desk.id == Card.desk_id).join(
        CardReview, Card.id == CardReview.card_id
    ).filter(
        CardReview.user_id == user.id,
        CardReview.is_correct == True
    ).group_by(Desk.id, Desk.name_en).order_by(
        func.count(CardReview.id).desc()
    ).limit(5).all()
    
    # Leaderboard: top users by completed cards
    leaderboard_data = db.session.query(
        CardReview.user_id,
        func.count(CardReview.id).label('cnt')
    ).filter(
        CardReview.is_correct == True
    ).group_by(
        CardReview.user_id
    ).order_by(
        func.count(CardReview.id).desc()
    ).limit(10).all()
    
    # Get user info for leaderboard
    user_ids = [row[0] for row in leaderboard_data]
    users_map = {u.id: u for u in User.query.filter(User.id.in_(user_ids)).all()} if user_ids else {}
    
    leaderboard = []
    for user_id, count in leaderboard_data:
        u = users_map.get(user_id)
        if u:
            leaderboard.append({
                'id': user_id,
                'name': u.name,
                'email': u.email,
                'count': count
            })
    
    # Get user rank
    user_rank = 1
    for rank, (uid, count) in enumerate(leaderboard_data, 1):
        if uid == user.id:
            user_rank = rank
            break
    
    # Recent activity
    recent_reviews = CardReview.query.filter_by(user_id=user.id).order_by(
        CardReview.created_at.desc()
    ).limit(10).all()
    
    recent_activity = []
    for review in recent_reviews:
        card = Card.query.get(review.card_id)
        desk = Desk.query.get(card.desk_id) if card else None
        if card and desk:
            recent_activity.append({
                'desk': desk.name_en,
                'question': card.question[:50] + '...' if len(card.question) > 50 else card.question,
                'is_correct': review.is_correct,
                'created_at': review.created_at
            })
    
    return render_template('dashboard.html',
                         total_cards=total_cards,
                         completed_cards=completed_cards,
                         top_desks=top_desks,
                         leaderboard=leaderboard,
                         user_rank=user_rank,
                         recent_activity=recent_activity)
