#!/usr/bin/env python
"""Seed quiz data for English learning"""
from app import create_app
from models import db, Quiz, QuizQuestion, QuizAnswer

app = create_app()

# Quiz data structure
QUIZZES_DATA = [
    {
        'title': 'English Vocabulary Basics',
        'description': 'Test your basic English vocabulary skills',
        'category': 'English',
        'questions': [
            {
                'question': 'What is the opposite of "big"?',
                'type': 'multiple_choice',
                'answers': [
                    {'text': 'small', 'correct': True},
                    {'text': 'large', 'correct': False},
                    {'text': 'huge', 'correct': False},
                    {'text': 'tall', 'correct': False},
                ]
            },
            {
                'question': 'Complete the sentence: "I ___ to school every day."',
                'type': 'fill_blank',
                'answers': [
                    {'text': 'go', 'correct': True},
                    {'text': 'goes', 'correct': False},
                    {'text': 'going', 'correct': False},
                    {'text': 'gone', 'correct': False},
                ]
            },
            {
                'question': 'What is a synonym for "happy"?',
                'type': 'multiple_choice',
                'answers': [
                    {'text': 'joyful', 'correct': True},
                    {'text': 'sad', 'correct': False},
                    {'text': 'angry', 'correct': False},
                    {'text': 'tired', 'correct': False},
                ]
            },
            {
                'question': 'Fill in the blank: "She ___ a teacher."',
                'type': 'fill_blank',
                'answers': [
                    {'text': 'is', 'correct': True},
                    {'text': 'are', 'correct': False},
                    {'text': 'am', 'correct': False},
                    {'text': 'be', 'correct': False},
                ]
            },
            {
                'question': 'What does "appreciate" mean?',
                'type': 'multiple_choice',
                'answers': [
                    {'text': 'to value or be grateful for', 'correct': True},
                    {'text': 'to disapprove', 'correct': False},
                    {'text': 'to ignore', 'correct': False},
                    {'text': 'to criticize', 'correct': False},
                ]
            },
            {
                'question': 'Choose the correct form: "They ___ playing football."',
                'type': 'fill_blank',
                'answers': [
                    {'text': 'are', 'correct': True},
                    {'text': 'is', 'correct': False},
                    {'text': 'am', 'correct': False},
                    {'text': 'been', 'correct': False},
                ]
            },
            {
                'question': 'What is the past tense of "eat"?',
                'type': 'multiple_choice',
                'answers': [
                    {'text': 'ate', 'correct': True},
                    {'text': 'eats', 'correct': False},
                    {'text': 'eating', 'correct': False},
                    {'text': 'eaten', 'correct': False},
                ]
            },
            {
                'question': 'Fill in: "I have never ___ Paris before."',
                'type': 'fill_blank',
                'answers': [
                    {'text': 'been to', 'correct': True},
                    {'text': 'go to', 'correct': False},
                    {'text': 'went to', 'correct': False},
                    {'text': 'be', 'correct': False},
                ]
            },
            {
                'question': 'What is the plural of "child"?',
                'type': 'multiple_choice',
                'answers': [
                    {'text': 'children', 'correct': True},
                    {'text': 'childs', 'correct': False},
                    {'text': 'childes', 'correct': False},
                    {'text': 'child\'s', 'correct': False},
                ]
            },
            {
                'question': 'Choose the correct sentence:',
                'type': 'multiple_choice',
                'answers': [
                    {'text': 'She go to the library every weekend.', 'correct': False},
                    {'text': 'She goes to the library every weekend.', 'correct': True},
                    {'text': 'She are going to the library every weekend.', 'correct': False},
                    {'text': 'She going to the library every weekend.', 'correct': False},
                ]
            },
        ]
    },
    {
        'title': 'English Grammar Essentials',
        'description': 'Master English grammar rules and structures',
        'category': 'English',
        'questions': [
            {
                'question': 'Which is the correct use of present perfect?',
                'type': 'multiple_choice',
                'answers': [
                    {'text': 'I have lived here for 5 years.', 'correct': True},
                    {'text': 'I live here for 5 years.', 'correct': False},
                    {'text': 'I lived here for 5 years.', 'correct': False},
                    {'text': 'I am living here for 5 years.', 'correct': False},
                ]
            },
            {
                'question': 'What is the correct form of third person singular?',
                'type': 'multiple_choice',
                'answers': [
                    {'text': 'He watches TV every evening.', 'correct': True},
                    {'text': 'He watch TV every evening.', 'correct': False},
                    {'text': 'He watching TV every evening.', 'correct': False},
                    {'text': 'He is watch TV every evening.', 'correct': False},
                ]
            },
            {
                'question': 'Choose the correct conditional sentence:',
                'type': 'multiple_choice',
                'answers': [
                    {'text': 'If I were rich, I would travel around the world.', 'correct': True},
                    {'text': 'If I am rich, I will travel around the world.', 'correct': False},
                    {'text': 'If I was rich, I will travel around the world.', 'correct': False},
                    {'text': 'If I were rich, I will travel around the world.', 'correct': False},
                ]
            },
            {
                'question': 'What is the object pronoun for "they"?',
                'type': 'multiple_choice',
                'answers': [
                    {'text': 'them', 'correct': True},
                    {'text': 'their', 'correct': False},
                    {'text': 'theirs', 'correct': False},
                    {'text': 'themselves', 'correct': False},
                ]
            },
            {
                'question': 'Fill in: "I wish I ___ speak French fluently."',
                'type': 'fill_blank',
                'answers': [
                    {'text': 'could', 'correct': True},
                    {'text': 'can', 'correct': False},
                    {'text': 'will', 'correct': False},
                    {'text': 'would', 'correct': False},
                ]
            },
            {
                'question': 'Which sentence uses the passive voice correctly?',
                'type': 'multiple_choice',
                'answers': [
                    {'text': 'The book was written by the author.', 'correct': True},
                    {'text': 'The book written by the author.', 'correct': False},
                    {'text': 'The author wrote by the book.', 'correct': False},
                    {'text': 'The book is write by the author.', 'correct': False},
                ]
            },
            {
                'question': 'What is the correct use of "too" or "very"?',
                'type': 'multiple_choice',
                'answers': [
                    {'text': 'The coffee is very hot. (I can drink it)', 'correct': True},
                    {'text': 'The coffee is too hot. (I can drink it)', 'correct': False},
                    {'text': 'The coffee is very cold.', 'correct': False},
                    {'text': 'The coffee is very boiling.', 'correct': False},
                ]
            },
            {
                'question': 'Fill in: "Neither John nor Mary ___ coming to the party."',
                'type': 'fill_blank',
                'answers': [
                    {'text': 'is', 'correct': True},
                    {'text': 'are', 'correct': False},
                    {'text': 'am', 'correct': False},
                    {'text': 'be', 'correct': False},
                ]
            },
            {
                'question': 'What is the difference between "a" and "an"?',
                'type': 'multiple_choice',
                'answers': [
                    {'text': 'Use "an" before vowel sounds', 'correct': True},
                    {'text': 'Use "a" before vowel sounds', 'correct': False},
                    {'text': 'There is no difference', 'correct': False},
                    {'text': 'Use "an" only before the letter "a"', 'correct': False},
                ]
            },
            {
                'question': 'Complete: "I would rather ___ stay at home than go out."',
                'type': 'fill_blank',
                'answers': [
                    {'text': '(nothing)', 'correct': True},
                    {'text': 'to', 'correct': False},
                    {'text': 'would', 'correct': False},
                    {'text': 'be', 'correct': False},
                ]
            },
        ]
    },
    {
        'title': 'Daily English Conversations',
        'description': 'Common phrases and expressions in English conversations',
        'category': 'English',
        'questions': [
            {
                'question': 'How do you greet someone formally?',
                'type': 'multiple_choice',
                'answers': [
                    {'text': 'Good morning, how do you do?', 'correct': True},
                    {'text': 'Hey, what\'s up?', 'correct': False},
                    {'text': 'Yo!', 'correct': False},
                    {'text': 'Hiya!', 'correct': False},
                ]
            },
            {
                'question': 'What do you say when someone thanks you?',
                'type': 'multiple_choice',
                'answers': [
                    {'text': 'You\'re welcome.', 'correct': True},
                    {'text': 'No problem.', 'correct': False},
                    {'text': 'Sure.', 'correct': False},
                    {'text': 'Both "You\'re welcome" and "No problem" are acceptable.', 'correct': False},
                ]
            },
            {
                'question': 'How do you politely ask for something?',
                'type': 'multiple_choice',
                'answers': [
                    {'text': 'Could you please pass the salt?', 'correct': True},
                    {'text': 'Pass the salt!', 'correct': False},
                    {'text': 'I want the salt!', 'correct': False},
                    {'text': 'Give me the salt!', 'correct': False},
                ]
            },
            {
                'question': 'What do you say to express sympathy?',
                'type': 'multiple_choice',
                'answers': [
                    {'text': 'I\'m sorry to hear that.', 'correct': True},
                    {'text': 'That\'s funny!', 'correct': False},
                    {'text': 'Good for you!', 'correct': False},
                    {'text': 'Congratulations!', 'correct': False},
                ]
            },
            {
                'question': 'Fill in: "I don\'t feel well. I think I ___ a cold."',
                'type': 'fill_blank',
                'answers': [
                    {'text': 'have', 'correct': True},
                    {'text': 'have got', 'correct': False},
                    {'text': 'am having', 'correct': False},
                    {'text': 'had', 'correct': False},
                ]
            },
            {
                'question': 'How do you introduce someone?',
                'type': 'multiple_choice',
                'answers': [
                    {'text': 'I\'d like you to meet my friend John.', 'correct': True},
                    {'text': 'This is John, he\'s my friend.', 'correct': False},
                    {'text': 'Meet John.', 'correct': False},
                    {'text': 'All of the above are acceptable.', 'correct': False},
                ]
            },
            {
                'question': 'What is a polite way to disagree?',
                'type': 'multiple_choice',
                'answers': [
                    {'text': 'I see your point, but I disagree.', 'correct': True},
                    {'text': 'You\'re wrong!', 'correct': False},
                    {'text': 'That\'s stupid!', 'correct': False},
                    {'text': 'No way!', 'correct': False},
                ]
            },
            {
                'question': 'How do you ask about someone\'s health?',
                'type': 'multiple_choice',
                'answers': [
                    {'text': 'How are you feeling?', 'correct': True},
                    {'text': 'Are you sick?', 'correct': False},
                    {'text': 'What\'s wrong with you?', 'correct': False},
                    {'text': 'Do you feel bad?', 'correct': False},
                ]
            },
            {
                'question': 'Fill in: "Nice to meet you too. How have you ___?"',
                'type': 'fill_blank',
                'answers': [
                    {'text': 'been', 'correct': True},
                    {'text': 'be', 'correct': False},
                    {'text': 'are', 'correct': False},
                    {'text': 'done', 'correct': False},
                ]
            },
            {
                'question': 'What do you say when saying goodbye?',
                'type': 'multiple_choice',
                'answers': [
                    {'text': 'Goodbye! It was nice talking to you.', 'correct': True},
                    {'text': 'Bye! See you never.', 'correct': False},
                    {'text': 'Get out!', 'correct': False},
                    {'text': 'Leave me alone!', 'correct': False},
                ]
            },
        ]
    },
]

def seed_quizzes():
    """Seed quiz data"""
    with app.app_context():
        print("🗑️  Deleting old quizzes...")
        Quiz.query.delete()
        db.session.commit()
        
        print("📝 Creating new quizzes...\n")
        
        for quiz_data in QUIZZES_DATA:
            quiz = Quiz(
                title=quiz_data['title'],
                description=quiz_data['description'],
                category=quiz_data['category']
            )
            db.session.add(quiz)
            db.session.flush()
            
            for order, question_data in enumerate(quiz_data['questions'], 1):
                question = QuizQuestion(
                    quiz_id=quiz.id,
                    question_text=question_data['question'],
                    question_type=question_data['type'],
                    order=order
                )
                db.session.add(question)
                db.session.flush()
                
                for ans_order, answer_data in enumerate(question_data['answers'], 1):
                    answer = QuizAnswer(
                        question_id=question.id,
                        answer_text=answer_data['text'],
                        is_correct=answer_data['correct'],
                        order=ans_order
                    )
                    db.session.add(answer)
            
            print(f"✅ {quiz.title}: {len(quiz_data['questions'])} questions")
        
        db.session.commit()
        print(f"\n🎉 Quiz seeding complete!")
        print(f"   📊 {len(QUIZZES_DATA)} quizzes created")
        print(f"   🎯 Total questions: {sum(len(q['questions']) for q in QUIZZES_DATA)}")

if __name__ == '__main__':
    seed_quizzes()
