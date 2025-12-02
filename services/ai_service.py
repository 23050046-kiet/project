"""
AI Service for generating questions and answers
Using free APIs or built-in generators
"""

import random
from typing import List, Dict
from models import db, Card, Desk


class AIQuestionGenerator:
    """Generate questions for cards using various methods"""
    
    @staticmethod
    def generate_vocabulary_questions(topic: str, count: int = 5) -> List[Dict]:
        """Generate vocabulary questions for a topic"""
        
        # Sample vocabulary data
        vocabulary_bank = {
            'English Vocabulary': [
                {
                    'question': 'What does "serendipity" mean?',
                    'answer': 'Finding something good by chance; luck',
                    'example': 'It was pure serendipity that we met at the coffee shop.'
                },
                {
                    'question': 'What is the meaning of "eloquent"?',
                    'answer': 'Fluent, persuasive, and expressive in speaking or writing',
                    'example': 'The president gave an eloquent speech at the conference.'
                },
                {
                    'question': 'Define "ephemeral"',
                    'answer': 'Lasting for a very short time; temporary',
                    'example': 'The beauty of cherry blossoms is ephemeral, lasting only a few weeks.'
                },
                {
                    'question': 'What does "pragmatic" mean?',
                    'answer': 'Dealing with things in a practical, realistic way based on actual circumstances',
                    'example': 'We need a pragmatic approach to solve this budget problem.'
                },
                {
                    'question': 'Define "meticulous"',
                    'answer': 'Very careful and precise; paying close attention to detail',
                    'example': 'Her meticulous research led to groundbreaking discoveries.'
                },
                {
                    'question': 'What is "nostalgia"?',
                    'answer': 'A sentimental longing for the past, typically for a period or place with happy memories',
                    'example': 'Looking at old photographs filled him with nostalgia.'
                },
                {
                    'question': 'Define "ubiquitous"',
                    'answer': 'Present, appearing, or found everywhere',
                    'example': 'Smartphones have become ubiquitous in modern society.'
                },
                {
                    'question': 'What does "ambiguous" mean?',
                    'answer': 'Open to more than one interpretation; unclear in meaning',
                    'example': 'The contract language was ambiguous and led to disputes.'
                },
                {
                    'question': 'Define "benevolent"',
                    'answer': 'Showing kindness and generous concern for others',
                    'example': 'The benevolent organization donated millions to charity.'
                },
                {
                    'question': 'What is "resilience"?',
                    'answer': 'The ability to recover quickly from difficulties; toughness',
                    'example': 'The community showed great resilience after the disaster.'
                },
            ],
            'Spanish Basics': [
                {
                    'question': '¿Cómo se dice "hello" en español?',
                    'answer': 'Hola',
                    'example': 'Hola, ¿cómo estás?'
                },
                {
                    'question': '¿Cuál es la palabra en español para "thank you"?',
                    'answer': 'Gracias',
                    'example': 'Muchas gracias por tu ayuda.'
                },
                {
                    'question': '¿Cómo se dice "goodbye" en español?',
                    'answer': 'Adiós',
                    'example': 'Adiós, nos vemos mañana.'
                },
                {
                    'question': '¿Cuál es "water" en español?',
                    'answer': 'Agua',
                    'example': 'Un vaso de agua, por favor.'
                },
                {
                    'question': '¿Cómo se dice "yes" en español?',
                    'answer': 'Sí',
                    'example': 'Sí, me gustaría probar eso.'
                },
                {
                    'question': '¿Cuál es "no" en español?',
                    'answer': 'No',
                    'example': 'No, gracias, estoy lleno.'
                },
                {
                    'question': '¿Cómo se dice "I love you" en español?',
                    'answer': 'Te amo',
                    'example': 'Te amo mucho, mi amor.'
                },
                {
                    'question': '¿Cuál es "friend" en español?',
                    'answer': 'Amigo',
                    'example': 'Mi amigo es muy divertido.'
                },
                {
                    'question': '¿Cómo se dice "beautiful" en español?',
                    'answer': 'Hermoso/Hermosa',
                    'example': 'Qué día tan hermoso para pasear.'
                },
                {
                    'question': '¿Cuál es "food" en español?',
                    'answer': 'Comida',
                    'example': 'La comida española es deliciosa.'
                },
            ],
            'Python Basics': [
                {
                    'question': 'What is the correct syntax for a Python function?',
                    'answer': 'def function_name(parameters): followed by indented code block',
                    'example': 'def greet(name):\n    print(f"Hello, {name}!")'
                },
                {
                    'question': 'How do you create a list in Python?',
                    'answer': 'Using square brackets: [item1, item2, item3]',
                    'example': 'my_list = [1, 2, 3, 4, 5]'
                },
                {
                    'question': 'What is a dictionary in Python?',
                    'answer': 'An unordered collection of key-value pairs enclosed in curly braces',
                    'example': 'person = {"name": "John", "age": 30}'
                },
                {
                    'question': 'How do you import a module in Python?',
                    'answer': 'Using the import statement: import module_name',
                    'example': 'import math\nresult = math.sqrt(16)'
                },
                {
                    'question': 'What is a loop in Python?',
                    'answer': 'A control structure that repeats a code block until a condition is met',
                    'example': 'for i in range(5):\n    print(i)'
                },
            ],
            'Math Formulas': [
                {
                    'question': 'What is the Pythagorean theorem?',
                    'answer': 'a² + b² = c² (where c is the hypotenuse of a right triangle)',
                    'example': 'For a triangle with sides 3 and 4, the hypotenuse is √(3² + 4²) = 5'
                },
                {
                    'question': 'What is the formula for the area of a circle?',
                    'answer': 'A = πr² (where r is the radius)',
                    'example': 'A circle with radius 5 has area = π(5)² ≈ 78.54'
                },
                {
                    'question': 'How do you calculate simple interest?',
                    'answer': 'I = P × r × t (Principal × rate × time)',
                    'example': '$1000 at 5% for 2 years = $1000 × 0.05 × 2 = $100'
                },
                {
                    'question': 'What is the quadratic formula?',
                    'answer': 'x = (-b ± √(b² - 4ac)) / 2a',
                    'example': 'For x² + 5x + 6 = 0, x = (-5 ± √(25-24)) / 2 = -2 or -3'
                },
                {
                    'question': 'What is the formula for the perimeter of a rectangle?',
                    'answer': 'P = 2(l + w) (length + width)',
                    'example': 'A rectangle 5cm × 3cm has perimeter = 2(5+3) = 16cm'
                },
            ],
        }
        
        # Get questions for the topic
        questions = vocabulary_bank.get(topic, [])
        
        # Return random sample if available, otherwise return what we have
        if len(questions) > count:
            return random.sample(questions, count)
        return questions
    
    @staticmethod
    def create_cards_for_desk(desk_id: int, topic: str = None, count: int = 5):
        """Create cards for a desk based on AI generated content"""
        
        desk = Desk.query.get(desk_id)
        if not desk:
            return None
        
        # Use desk name as topic if not provided
        if not topic:
            topic = desk.name_en
        
        # Generate questions
        questions = AIQuestionGenerator.generate_vocabulary_questions(topic, count)
        
        # Create cards in database
        cards = []
        for idx, q in enumerate(questions):
            card = Card(
                desk_id=desk_id,
                question=q['question'],
                answer=q['answer'],
                example=q.get('example', ''),
                order=idx + 1
            )
            db.session.add(card)
            cards.append(card)
        
        db.session.commit()
        return cards
    
    @staticmethod
    def get_available_topics() -> List[str]:
        """Get list of available topics for generation"""
        return [
            'English Vocabulary',
            'Spanish Basics',
            'Python Basics',
            'Math Formulas',
        ]


class SpacedRepetitionScheduler:
    """Schedule card reviews using spaced repetition algorithm"""
    
    # Schedule intervals in minutes
    INTERVALS = {
        0: 1,      # First review: 1 minute
        1: 10,     # Second review: 10 minutes
        2: 1440,   # Third review: 1 day (1440 minutes)
        3: 10080,  # Fourth review: 7 days (10080 minutes)
    }
    
    @staticmethod
    def get_next_review_time(review_stage: int) -> int:
        """Get next review time in minutes based on stage"""
        return SpacedRepetitionScheduler.INTERVALS.get(review_stage, 10080)
    
    @staticmethod
    def get_user_due_cards(user_id: int, desk_id: int = None):
        """Get cards due for review"""
        from datetime import datetime
        
        query = Card.query.join(
            CardReview,
            Card.id == CardReview.card_id
        ).filter(
            CardReview.user_id == user_id,
            CardReview.next_review_at <= datetime.utcnow()
        )
        
        if desk_id:
            query = query.filter(Card.desk_id == desk_id)
        
        return query.all()
