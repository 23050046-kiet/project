#!/usr/bin/env python
"""Restore all English vocabulary cards"""
from app import create_app
from models import db, Desk, Card

app = create_app()

# English vocabulary data
DESKS_DATA = {
    'Animals': {
        'cards': [
            ('Dog', 'Chó', 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/61/20110425_German_Shepherd_Dog_8505.jpg/640px-20110425_German_Shepherd_Dog_8505.jpg', '/dɔːɡ/'),
            ('Cat', 'Mèo', 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c1/Six_weeks_old_cat_%28aka%29.jpg/640px-Six_weeks_old_cat_%28aka%29.jpg', '/kæt/'),
            ('Bird', 'Chim', 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c8/Asian_pied_starlings_%28Gracupica_contra%29.jpg/640px-Asian_pied_starlings_%28Gracupica_contra%29.jpg', '/bɜːrd/'),
            ('Fish', 'Cá', 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6c/Pristis_pristis_-_Georgia_Aquarium_Jan_2006.jpg/640px-Pristis_pristis_-_Georgia_Aquarium_Jan_2006.jpg', '/fɪʃ/'),
            ('Lion', 'Sư tử', 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/011_The_lion_king_Tryggve_in_the_Serengeti_National_Park_Photo_by_Giles_Laurent.jpg/640px-011_The_lion_king_Tryggve_in_the_Serengeti_National_Park_Photo_by_Giles_Laurent.jpg', '/ˈlaɪən/'),
            ('Elephant', 'Voi', 'https://upload.wikimedia.org/wikipedia/commons/3/3b/African_elephant_%28Loxodonta_africana%29_3.jpg', '/ˈelɪfənt/'),
            ('Tiger', 'Hổ', 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/71/Sibirischer_tiger_de_edit02.jpg/640px-Sibirischer_tiger_de_edit02.jpg', '/ˈtaɪɡər/'),
            ('Monkey', 'Khỉ', 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/2b/Rhesus_Macaque_monkey_the_look.jpg/640px-Rhesus_Macaque_monkey_the_look.jpg', '/ˈmʌŋki/'),
            ('Butterfly', 'Bươm bướm', 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/3d/Gold_rim_swallowtail_%28Battus_polydamas_jamaicensis%29_underside_worn_2.JPG/640px-Gold_rim_swallowtail_%28Battus_polydamas_jamaicensis%29_underside_worn_2.JPG', '/ˈbʌtərflaɪ/'),
            ('Bee', 'Ong', 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/99/Apis_mellifera_flying.jpg/640px-Apis_mellifera_flying.jpg', '/biː/'),
        ]
    },
    'Numbers': {
        'cards': [
            ('One', 'Một', 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/Calendar_Icon_1_BW.png/640px-Calendar_Icon_1_BW.png', '/wʌn/'),
            ('Two', 'Hai', 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/Sign_number_2_on_Jerusalem_Street.jpg/640px-Sign_number_2_on_Jerusalem_Street.jpg', '/tuː/'),
            ('Three', 'Ba', 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/29/Symbol_3.svg/640px-Symbol_3.svg.png', '/θriː/'),
            ('Four', 'Bốn', 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/O-Train_Line_4.svg/640px-O-Train_Line_4.svg.png', '/fɔːr/'),
            ('Five', 'Năm', 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/97/Number_five_sign_%28cropped%29.jpg/640px-Number_five_sign_%28cropped%29.jpg', '/faɪv/'),
            ('Six', 'Sáu', 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Number_6_in_blue_circle.svg/640px-Number_6_in_blue_circle.svg.png', '/sɪks/'),
            ('Seven', 'Bảy', 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/37/Calendar_Icon_7_BW.png/640px-Calendar_Icon_7_BW.png', '/ˈsevən/'),
            ('Eight', 'Tám', 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/08/Number_eight_ornament.jpg/640px-Number_eight_ornament.jpg', '/eɪt/'),
            ('Nine', 'Chín', 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/76/Sign_number_9_on_Jerusalem_Street.jpg/640px-Sign_number_9_on_Jerusalem_Street.jpg', '/naɪn/'),
            ('Ten', 'Mười', 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c7/Calendar_Icon_10_BW.png/640px-Calendar_Icon_10_BW.png', '/ten/'),
        ]
    },
    'Kitchen': {
        'cards': [
            ('Knife', 'Dao', 'https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Knives_%2832778862921%29.jpg/640px-Knives_%2832778862921%29.jpg', '/naɪf/'),
            ('Fork', 'Nĩa', 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/7c/Assorted_forks.jpg/640px-Assorted_forks.jpg', '/fɔːrk/'),
            ('Spoon', 'Muỗng', 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/08/SpoonCollection.jpg/640px-SpoonCollection.jpg', '/spuːn/'),
            ('Pan', 'Chảo', 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a1/Bacon_in_a_pan_%28cooked%29.jpg/640px-Bacon_in_a_pan_%28cooked%29.jpg', '/pæn/'),
            ('Pot', 'Nồi', 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/81/Pot_on_stove.jpg/640px-Pot_on_stove.jpg', '/pɑːt/'),
            ('Cup', 'Cốc', 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/cc/Kaffeetasse_halbhoch_Golddekor_05%2C_KPM.jpg/640px-Kaffeetasse_halbhoch_Golddekor_05%2C_KPM.jpg', '/kʌp/'),
            ('Plate', 'Đĩa', 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a8/Plate_Poland_02.jpg/640px-Plate_Poland_02.jpg', '/pleɪt/'),
            ('Bowl', 'Tô', 'https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/Salisbury_%27Greba%27_bowl_-_2022-07-20_-_Andy_Mabbett_-_02.jpg/640px-Salisbury_%27Greba%27_bowl_-_2022-07-20_-_Andy_Mabbett_-_02.jpg', '/boʊl/'),
            ('Spatula', 'Chít mỏng', 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Spatulas.jpg/640px-Spatulas.jpg', '/ˈspætʃʊlə/'),
            ('Whisk', 'Cọ trộn', 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/1c/Balloon_spiral_ball_whisks.jpg/640px-Balloon_spiral_ball_whisks.jpg', '/wɪsk/'),
        ]
    },
    'Fruits': {
        'cards': [
            ('Apple', 'Táo', 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Red_Apple.jpg/640px-Red_Apple.jpg', '/ˈæpəl/'),
            ('Banana', 'Chuối', 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/Cavendish_banana_from_Maracaibo.jpg/640px-Cavendish_banana_from_Maracaibo.jpg', '/bəˈnɑːnə/'),
            ('Orange Fruit', 'Cam', 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/43/Ambersweet_oranges.jpg/640px-Ambersweet_oranges.jpg', '/ˈɑːrɪndʒ/'),
            ('Strawberry', 'Dâu', 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8b/Strawberry-1.jpg/640px-Strawberry-1.jpg', '/ˈstrɔːberi/'),
            ('Grape', 'Nho', 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/03/Grape_Plant_and_grapes9.jpg/640px-Grape_Plant_and_grapes9.jpg', '/ɡreɪp/'),
            ('Watermelon', 'Dưa hấu', 'https://upload.wikimedia.org/wikipedia/commons/thumb/d/d9/%D8%A7%D9%84%D8%A8%D8%B7%D9%8A%D8%AE_%D8%A7%D9%84%D8%A3%D8%AD%D9%85%D8%B1.JPG/640px-%D8%A7%D9%84%D8%A8%D8%B7%D9%8A%D8%AE_%D8%A7%D9%84%D8%A3%D8%AD%D9%85%D8%B1.JPG', '/ˈwɔːtərmelən/'),
            ('Mango', 'Xoài', 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/af/Mango_fruit_Nam_Dok_Mai.jpg/640px-Mango_fruit_Nam_Dok_Mai.jpg', '/ˈmæŋɡoʊ/'),
            ('Pineapple', 'Dứa', 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e8/The_pineapple_%28Ananas_comosus%29.JPG/640px-The_pineapple_%28Ananas_comosus%29.JPG', '/ˈpaɪnæpəl/'),
            ('Cherry', 'Cherry', 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/08/02024_May_Duke_Cherry%2C_Beskids_mts.jpg/640px-02024_May_Duke_Cherry%2C_Beskids_mts.jpg', '/ˈtʃeri/'),
            ('Lemon', 'Chanh', 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Lemon.jpg/640px-Lemon.jpg', '/ˈlemən/'),
            ('Peach', 'Đào', 'https://commons.wikimedia.org/wiki/Special:FilePath/Peach_fruit.jpg?width=400', '/piːtʃ/'),
        ]
    },
    'Vegetables': {
        'cards': [
            ('Carrot', 'Cà rốt', 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Carrots_at_Ljubljana_Central_Market.JPG/640px-Carrots_at_Ljubljana_Central_Market.JPG', '/ˈkærət/'),
            ('Tomato', 'Cà chua', 'https://commons.wikimedia.org/wiki/Special:FilePath/Tomato_red.jpg?width=400', '/təˈmɑːtoʊ/'),
            ('Lettuce', 'Xà lách', 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/02/Lactuca_sativa_%27Lollo_Bionda%27.jpg/640px-Lactuca_sativa_%27Lollo_Bionda%27.jpg', '/ˈletɪs/'),
            ('Cucumber', 'Dưa chuột', 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Cucumber_plants.jpg/640px-Cucumber_plants.jpg', '/ˈkjuːkʌmbər/'),
            ('Onion', 'Hành', 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Mixed_onions.jpg/640px-Mixed_onions.jpg', '/ˈʌnjən/'),
            ('Potato', 'Khoai tây', 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/ab/Patates.jpg/640px-Patates.jpg', '/pəˈteɪtoʊ/'),
            ('Pepper', 'Ớt', 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/11/Capsicum_annuum_var._Fiesta_-_MHNT.jpg/640px-Capsicum_annuum_var._Fiesta_-_MHNT.jpg', '/ˈpepər/'),
            ('Bell Pepper', 'Ớt chuông', 'https://upload.wikimedia.org/wikipedia/commons/thumb/d/de/Capsicum_annuum_fruits_IMGP0049.jpg/640px-Capsicum_annuum_fruits_IMGP0049.jpg', '/bel ˈpepər/'),
            ('Broccoli', 'Súp lơ xanh', 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/79/Broccoli_3.jpg/640px-Broccoli_3.jpg', '/ˈbrɑːkəli/'),
            ('Cabbage', 'Bắp cải', 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/42/Brassica_oleracea_var._capitata_zum_Verkauf_2011.JPG/640px-Brassica_oleracea_var._capitata_zum_Verkauf_2011.JPG', '/ˈkæbɪdʒ/'),
            ('Corn', 'Ngô', 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/f1/Corn_-_Zea_mays.jpg/640px-Corn_-_Zea_mays.jpg', '/kɔːrn/'),
            ('Garlic', 'Tỏi', 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/Garlic_bulbs_and_cloves.jpg/640px-Garlic_bulbs_and_cloves.jpg', '/ˈɡɑːrlɪk/'),
            ('Mushroom', 'Nấm', 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8d/Edible_mushrooms_in_baskets_2022_G1.jpg/640px-Edible_mushrooms_in_baskets_2022_G1.jpg', '/ˈmʌʃruːm/'),
        ]
    },
    'Colors': {
        'cards': [
            ('Red', 'Đỏ', '', '/red/'),
            ('Blue', 'Xanh dương', '', '/bluː/'),
            ('Green', 'Xanh lá', '', '/ɡriːn/'),
            ('Yellow', 'Vàng', '', '/ˈjeloʊ/'),
            ('Purple', 'Tím', '', '/ˈpɜːrpəl/'),
            ('Pink', 'Hồng', '', '/pɪŋk/'),
            ('Black', 'Đen', '', '/blæk/'),
            ('White', 'Trắng', '', '/waɪt/'),
            ('Brown', 'Nâu', '', '/braʊn/'),
            ('Orange', 'Cam (màu)', '', '/ˈɑːrɪndʒ/'),
        ]
    },
    'Clothes': {
        'cards': [
            ('Shirt', 'Áo sơ mi', 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c9/T-shirt_%28drawing%29.jpg/640px-T-shirt_%28drawing%29.jpg', '/ʃɜːrt/'),
            ('Pants', 'Quần', 'https://upload.wikimedia.org/wikipedia/commons/thumb/d/da/Trousers-colourisolated.jpg/640px-Trousers-colourisolated.jpg', '/pænts/'),
            ('Dress', 'Váy', 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Dress_MET_DT11828.jpg/640px-Dress_MET_DT11828.jpg', '/dres/'),
            ('Jacket', 'Áo khoác', 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/10/Harrington-jacket-marque-francaise-Harrington-bleu-Tartan-Royal-Stewart-byRundvald.jpg/640px-Harrington-jacket-marque-francaise-Harrington-bleu-Tartan-Royal-Stewart-byRundvald.jpg', '/ˈdʒækɪt/'),
            ('Sweater', 'Áo len', 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/ea/Jersei-coll-alt.jpg/640px-Jersei-coll-alt.jpg', '/ˈsweɪtər/'),
            ('Hat', 'Mũ', 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/43/1920s_Stetson_carlsbad_cowboy_hat_side.jpg/640px-1920s_Stetson_carlsbad_cowboy_hat_side.jpg', '/hæt/'),
            ('Shoes', 'Giày', 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/f0/Reebok_Royal_Glide_Ripple_Clip_shoe.jpg/640px-Reebok_Royal_Glide_Ripple_Clip_shoe.jpg', '/ʃuːz/'),
            ('Socks', 'Tất', 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/fd/Villased_sokid%2C_STM_1998.jpg/640px-Villased_sokid%2C_STM_1998.jpg', '/sɑːks/'),
            ('Tie', 'Cà vạt', 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/bc/Memphis_tie_1A.JPG/640px-Memphis_tie_1A.JPG', '/taɪ/'),
            ('Scarf', 'Khăn quàng', 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/Traditional_Hajong_scarf%2C_kompes.png/640px-Traditional_Hajong_scarf%2C_kompes.png', '/skɑːrf/'),
            ('Gloves', 'Găng tay', 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/01/Centre_de_Documentaci%C3%B3_Museu_T%C3%A8xtil_de_Terrassa-_Reserves-_Teixits-_Guants002.JPG/640px-Centre_de_Documentaci%C3%B3_Museu_T%C3%A8xtil_de_Terrassa-_Reserves-_Teixits-_Guants002.JPG', '/ɡlʌvz/'),
        ]
    },
    'Household': {
        'cards': [
            ('Table', 'Bàn', 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Handlebar_Table_designed_by_Jasper_Morrison.jpg/640px-Handlebar_Table_designed_by_Jasper_Morrison.jpg', '/ˈteɪbəl/'),
            ('Chair', 'Ghế', 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/86/Fauteuil_Riviera_Chaise_Bleue_Neptune_SBR.jpg/640px-Fauteuil_Riviera_Chaise_Bleue_Neptune_SBR.jpg', '/tʃer/'),
            ('Bed', 'Giường', 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/7f/Bed_Making04.svg/640px-Bed_Making04.svg.png', '/bed/'),
            ('Door', 'Cửa', 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/Door_Handle_4.jpg/640px-Door_Handle_4.jpg', '/dɔːr/'),
            ('Window', 'Cửa sổ', 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/23/Santorin_%28GR%29%2C_Fira_--_2017_--_2624.jpg/640px-Santorin_%28GR%29%2C_Fira_--_2017_--_2624.jpg', '/ˈwɪndoʊ/'),
            ('Lamp', 'Đèn', 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Lamp_with_a_lampshade_illuminated_by_sunlight.jpg/640px-Lamp_with_a_lampshade_illuminated_by_sunlight.jpg', '/læmp/'),
            ('Mirror', 'Gương', 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/Noto_Emoji_v2.034_1fa9e.svg/640px-Noto_Emoji_v2.034_1fa9e.svg.png', '/ˈmɪrər/'),
            ('Sofa', 'Ghế sofa', 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e8/Sofa_MET_1999.396.jpg/640px-Sofa_MET_1999.396.jpg', '/ˈsoʊfə/'),
            ('Refrigerator', 'Tủ lạnh', 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/LG_refrigerator_interior.jpg/640px-LG_refrigerator_interior.jpg', '/rɪˈfrɪdʒəreɪtər/'),
            ('Oven', 'Lò nướng', 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/ee/Panasonic_ELECTRIC_OVEN_NB-H3800.jpg/640px-Panasonic_ELECTRIC_OVEN_NB-H3800.jpg', '/ˈʌvən/'),
        ]
    },
}

def restore_vocabulary():
    """Restore English vocabulary desks and cards"""
    with app.app_context():
        print("🗑️  Deleting old desks and cards...")
        Desk.query.delete()
        Card.query.delete()
        db.session.commit()
        
        print("📚 Creating new English desks and cards...\n")
        
        desk_id = 1
        total_cards = 0
        
        for desk_name, desk_info in DESKS_DATA.items():
            # Create desk with correct schema
            desk = Desk(
                id=desk_id,
                name_en=desk_name,
                image_path=f"learn-{desk_name.lower().replace(' ', '-')}"
            )
            db.session.add(desk)
            db.session.flush()
            
            # Add cards
            for order, card_data in enumerate(desk_info['cards'], 1):
                question, answer, image_url, pronunciation = card_data
                card = Card(
                    desk_id=desk_id,
                    question=question,
                    answer=answer,
                    example=image_url,
                    pronunciation=pronunciation,
                    order=order
                )
                db.session.add(card)
                total_cards += 1
            
            print(f"✅ {desk_name}: {len(desk_info['cards'])} cards")
            desk_id += 1
        
        db.session.commit()
        print(f"\n🎉 Restoration complete!")
        print(f"   📊 {desk_id - 1} desks created")
        print(f"   🎯 {total_cards} vocabulary cards restored")

if __name__ == '__main__':
    restore_vocabulary()
