from pprint import pprint
import sqlalchemy


def insert_info_bd(connection_db, user_id, result_dict):
    sel = connection_db.execute(f'''
    SELECT vk_id FROM vk_users
    WHERE vk_id = '{user_id}'
    ''').fetchall()
    if len(sel) == 0:
        connection_db.execute(f'''
        INSERT  INTO vk_users (vk_id,vk_age,vk_sex,vk_city,vk_relation)
        VALUES ({user_id},{result_dict.get('age')},{result_dict.get('sex')},{result_dict.get('city')},{result_dict.get('relation')})
        ''')
        return 1  # Заполнение произошло
    return 0  # Заполнение не произошло


def update_param(connection_db, user_id, param, data):
    param = 'vk_' + param
    sel = connection_db.execute(f'''
    UPDATE vk_users SET {param}='{data}'
    WHERE vk_id = {user_id}
    ''')


def check_param_bd(connection_db, user_id, param):
    param = 'vk_' + param
    sel = connection_db.execute(f'''
        SELECT {param} FROM vk_users
        WHERE vk_id = '{user_id}'
        ''').fetchall()
    if sel[0][0] == 0 or sel[0][0] == '0':
        return 0  # Поле незаполнено
    return 1  # Поле заполнено


def check_all_params(connection_bd, user_id):
    data = ['age', 'sex', 'city', 'relation']
    for param in data:
        if check_param_bd(connection_bd, user_id, param) == 0:
            return 0
    return 1


db = 'postgresql://azvezdin:12345@localhost:5432/vkinder'
engine = sqlalchemy.create_engine(db)
connection = engine.connect()
