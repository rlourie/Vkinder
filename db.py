from pprint import pprint
import sqlalchemy


def insert_info_bd(user_id, result_dict):
    db = 'postgresql://azvezdin:12345@localhost:5432/vkinder'
    engine = sqlalchemy.create_engine(db)
    connection = engine.connect()
    user_id = 1
    sel = connection.execute(f'''
    SELECT vk_id FROM vk_users
    WHERE vk_id = '{user_id}'
    ''').fetchall()
    if len(sel) == 0:
        connection.execute(f'''
        INSERT  INTO vk_users (vk_id,vk_age,vk_sex,vk_city,vk_relation)
        VALUES ({user_id},{result_dict.get('age')},{result_dict.get('sex')},{result_dict.get('city')},{result_dict.get('relation')})
        ''').fetchall()

    return 0


insert_info_bd(134, {'age': 18, 'sex': 1, 'city': 1, 'relation': 1})
