#!/usr/bin/env python
"""Script để thêm chủ đề học từ vựng mới"""

from app import create_app
from models import db, Desk, Card

def add_vocabulary_topic(topic_name, cards_data):
    app = create_app()
    
    with app.app_context():
        # Kiểm tra xem topic đã tồn tại chưa
        existing_desk = Desk.query.filter_by(name_en=topic_name).first()
        if existing_desk:
            print(f"❌ Topic '{topic_name}' đã tồn tại!")
            return
        
        # Tạo Desk mới
        print(f"📚 Tạo topic '{topic_name}'...")
        desk = Desk(
            name_en=topic_name,
            image_path=f"topics/{topic_name.lower().replace(' ', '-')}"
        )
        db.session.add(desk)
        db.session.flush()  # Để lấy desk.id
        
        # Thêm các card
        print(f"📝 Thêm {len(cards_data)} cards...")
        for order, card_data in enumerate(cards_data, 1):
            card = Card(
                desk_id=desk.id,
                question=card_data['question'],
                answer=card_data['answer'],
                example=card_data.get('example', ''),
                pronunciation=card_data.get('pronunciation', ''),
                order=order
            )
            db.session.add(card)
        
        # Lưu vào database
        db.session.commit()
        
        print(f"✅ Topic '{topic_name}' được tạo thành công!")
        print(f"   📊 Desk ID: {desk.id}")
        print(f"   🎯 Cards added: {len(cards_data)}")


if __name__ == '__main__':
    # ==========================================
    # VÍ DỤ: Thêm chủ đề "SPORTS" (Thể thao)
    # ==========================================
    
    sports_cards = [
        {
            'question': 'Football',
            'answer': 'Bóng đá',
            'example': 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/41/Soccerball.svg/640px-Soccerball.svg.png',
            'pronunciation': '/ˈfʊtbɔːl/'
        },
        {
            'question': 'Basketball',
            'answer': 'Bóng rổ',
            'example': 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/Basketball.png/640px-Basketball.png',
            'pronunciation': '/ˈbɑːskɪtbɔːl/'
        },
        {
            'question': 'Tennis',
            'answer': 'Quần vợt',
            'example': 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/fe/Tennis_Racket_and_Balls.jpg/640px-Tennis_Racket_and_Balls.jpg',
            'pronunciation': '/ˈtenɪs/'
        },
        {
            'question': 'Swimming',
            'answer': 'Bơi lội',
            'example': 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Swim.jpg/640px-Swim.jpg',
            'pronunciation': '/ˈswɪmɪŋ/'
        },
        {
            'question': 'Running',
            'answer': 'Chạy bộ',
            'example': 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e9/Runner_in_race.jpg/640px-Runner_in_race.jpg',
            'pronunciation': '/ˈrʌnɪŋ/'
        },
        {
            'question': 'Volleyball',
            'answer': 'Bóng chuyền',
            'example': 'https://upload.wikimedia.org/wikipedia/commons/thumb/d/d1/Volleyball_%28indoor%29.jpg/640px-Volleyball_%28indoor%29.jpg',
            'pronunciation': '/ˈvɑːlibɔːl/'
        },
        {
            'question': 'Badminton',
            'answer': 'Cầu lông',
            'example': 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/be/Badminton_players.jpg/640px-Badminton_players.jpg',
            'pronunciation': '/ˈbædmɪntən/'
        },
        {
            'question': 'Cycling',
            'answer': 'Đạp xe',
            'example': 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/f5/Cycling_Tour_de_France_2014.jpg/640px-Cycling_Tour_de_France_2014.jpg',
            'pronunciation': '/ˈsaɪklɪŋ/'
        },
        {
            'question': 'Boxing',
            'answer': 'Quyền Anh',
            'example': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Boxing_2_2015-04-04.jpg/640px-Boxing_2_2015-04-04.jpg',
            'pronunciation': '/ˈbɑːksɪŋ/'
        },
        {
            'question': 'Golf',
            'answer': 'Golf',
            'example': 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Golf_ball.jpg/640px-Golf_ball.jpg',
            'pronunciation': '/ɡɑːlf/'
        },
    ]
    
    # Thêm chủ đề "Sports"
    add_vocabulary_topic('Sports', sports_cards)
    
    # ==========================================
    # TẠO THÊM TOPIC KHÁC
    # ==========================================
    # Uncomment dòng dưới để thêm topic khác:
    
    # professions_cards = [
    #     {
    #         'question': 'Doctor',
    #         'answer': 'Bác sĩ',
    #         'example': 'https://...',
    #         'pronunciation': '/ˈdɑːktər/'
    #     },
    #     ...
    # ]
    # add_vocabulary_topic('Professions', professions_cards)
