#!/usr/bin/env python
"""Database initialization script"""

from app import create_app
from models import db, User, Desk, Card, CardReview
from datetime import datetime, timedelta
from seed_quizzes import seed_quizzes
import sys

def init_db(reset=False):
    """Initialize database with sample data"""
    app = create_app()
    
    with app.app_context():
        # Create tables
        print("Creating database tables...")
        db.create_all()
        
        # Check if data already exists
        if User.query.first() and not reset:
            print("Database already initialized!")
            return
        
        # Reset if requested
        if reset and User.query.first():
            print("Resetting database...")
            db.drop_all()
            db.create_all()
            print("Database reset complete!")
        
        # Create admin user
        print("Creating admin user...")
        admin = User(
            name='Administrator',
            email='admin@flashmaster.local',
            is_admin=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
        
        # Create regular user
        print("Creating test user...")
        user = User(
            name='Test User',
            email='user@flashmaster.local',
            is_admin=False
        )
        user.set_password('user123')
        db.session.add(user)
        
        db.session.commit()
        
        # Create sample desks - Learning Vocabulary
        print("Creating Learning Vocabulary...")
        sample_desks = [
            Desk(name_en='English Vocabulary', image_path='desks/english.jpg'),
        ]
        
        for desk in sample_desks:
            db.session.add(desk)
        
        db.session.commit()
        
        # Create cards for desks
        print("Creating vocabulary cards...")
        
        # English Vocabulary cards with pronunciation
        english_cards = [
            {
                'question': 'What does "serendipity" mean?',
                'answer': 'Finding something good by chance',
                'example': 'It was pure serendipity that we met.',
                'pronunciation': '/ˌserənˈdɪpɪti/'
            },
            {
                'question': 'What is "eloquent"?',
                'answer': 'Fluent and persuasive in speaking',
                'example': 'The president gave an eloquent speech.',
                'pronunciation': '/ˈeləkwənt/'
            },
            {
                'question': 'Define "ephemeral"',
                'answer': 'Lasting for a very short time',
                'example': 'The beauty of cherry blossoms is ephemeral.',
                'pronunciation': '/ɪˈfem(ə)rəl/'
            },
            {
                'question': 'What does "pragmatic" mean?',
                'answer': 'Dealing with things practically',
                'example': 'We need a pragmatic approach to solve this.',
                'pronunciation': '/præɡˈmætɪk/'
            },
            {
                'question': 'Define "meticulous"',
                'answer': 'Very careful and precise',
                'example': 'Her meticulous research led to discoveries.',
                'pronunciation': '/məˈtɪkjələs/'
            },
        ]
        
        # Add cards to desks
        cards_data = [
            (1, english_cards),
        ]
        
        for desk_id, cards_list in cards_data:
            for idx, card_data in enumerate(cards_list, 1):
                card = Card(
                    desk_id=desk_id,
                    question=card_data['question'],
                    answer=card_data['answer'],
                    example=card_data['example'],
                    pronunciation=card_data.get('pronunciation', ''),
                    order=idx
                )
                db.session.add(card)
        
        db.session.commit()
        
        # Create sample review history for test user
        print("Creating sample review history...")
        test_user = User.query.filter_by(email='user@flashmaster.local').first()
        
        # Get some cards and create reviews
        cards_list = Card.query.limit(5).all()
        for idx, card in enumerate(cards_list):
            review = CardReview(
                user_id=test_user.id,
                card_id=card.id,
                is_correct=idx % 2 == 0,
                review_stage=1,
                next_review_at=datetime.utcnow() + timedelta(minutes=10)
            )
            db.session.add(review)
        
        db.session.commit()
        
        print("✓ Database initialized successfully!")
        print(f"✓ Created 1 desk with {len(english_cards)} vocabulary cards")
        print("\nTest accounts:")
        print("  Admin: admin@flashmaster.local / admin123")
        print("  User:  user@flashmaster.local / user123")
        
        # Seed quizzes
        print("\n📝 Seeding quizzes...")
        seed_quizzes()

if __name__ == '__main__':
    reset = '--reset' in sys.argv
    init_db(reset=reset)
