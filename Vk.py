from random import randrange
import vk_api
import math
from datetime import datetime
from vk_api.longpoll import VkLongPoll, VkEventType
from Token import token, access_token
from db import insert_info_bd, update_param, check_param_bd, check_all_params, get_param_bd, connection
from pprint import pprint

vk_session = vk_api.VkApi(token=token)
vk_user_session = vk_api.VkApi(token=access_token)
longpoll = VkLongPoll(vk_session)


def age(b_date):
    if b_date is not None:
        current_datetime = datetime.now()
        date_format = "%d.%m.%Y"
        delta = (current_datetime - datetime.strptime(b_date, date_format))
        return int(math.floor(delta.days / 365))
    else:
        return None


def write_msg(user_id, message):
    vk_session.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': randrange(10 ** 7), })


def get_info(user_id):
    info = vk_session.method('users.get', {"user_ids": user_id, "fields": "bdate,sex,city,relation"})
    result_dict = {'age': age(info[0].get('bdate')), 'sex': info[0].get('sex'), 'city': info[0].get('city').get('id'),
                   'relation': info[0].get('relation')}
    for key, value in result_dict.items():
        if value is None:
            result_dict[key] = 0  # Обнуляем пустые поля
    return result_dict  # Получаем всю инфу по пользователю


def search(user_id, count, offset):
    while True:
        search_setting = {'count': count, 'offset': offset, 'age_from': 20, 'age_to': 21, 'sex': 2, 'status': 6,
                          'fields': 'bdate'}
        data = ['age', 'sex', 'city', 'relation']
        for param in data:
            if param == 'age' or param == 'sex' or param == 'relation':
                if param == 'age':
                    search_setting['age_from'] = get_param_bd(connection, user_id, param) - 1
                    search_setting['age_to'] = get_param_bd(connection, user_id, param)
                if param == 'sex':
                    if get_param_bd(connection, user_id, param) == '2':
                        search_setting['sex'] = 1
                    else:
                        search_setting['sex'] = 2
                if param == 'relation':
                    pass
            else:
                search_setting[param] = get_param_bd(connection, user_id, param)
        res = vk_user_session.method('users.search', search_setting)
        result = {}
        if len(res['items']) == 0:
            offset += 1
        for elem in res['items']:
            if elem['is_closed'] is False:
                age_user = age(elem['bdate'])
                result[str(elem["id"])] = elem["first_name"] + ' ' + elem["last_name"] + ' ' + str(
                    age_user) + ' ' + 'лет'
                update_param(connection, user_id, 'offset', offset + 1)
                return result
            else:
                offset += 1
                break


def get_photo(user_id):
    result = []
    max_like = {'-1': -1}
    foto_param = {"album_id": "profile", "extended": "1", "photo_sizes": "1", "owner_id": str(user_id)}
    res = vk_user_session.method('photos.get', foto_param)
    for foto in res["items"]:
        if int(foto['likes']['count']) > min(max_like.values()):
            if len(max_like) < 3:
                max_like[str(foto['id'])] = int(foto['likes']['count'])
            else:
                lower = str(min(max_like, key=max_like.get))
                del max_like[lower]
                max_like[str(foto['id'])] = int(foto['likes']['count'])
    for key, val in list(max_like.items()):
        if val == -1:
            del max_like[key]
    return max_like


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            insert_info_bd(connection, event.user_id, get_info(event.user_id))
            if check_all_params(connection, event.user_id) == 0:
                write_msg(event.user_id, f"У тебя не заполнены данные по профилю, дополни информацию о себе:")
                if check_param_bd(connection, event.user_id, 'age') == 0:
                    write_msg(event.user_id, f"Введи свой возраст:")
                    while check_param_bd(connection, event.user_id, 'age') == 0:
                        response = vk_session.method('messages.getConversations',
                                                     {"offset": 0, "count": 1, "filter": 'unanswered'})
                        if len(response.get("items")) != 0:
                            update_param(connection, event.user_id, 'age',
                                         response.get("items")[0].get('last_message').get("text"))
                    continue
                if check_param_bd(connection, event.user_id, 'sex') == 0:
                    write_msg(event.user_id, f"Введи своё пол:\n1-Женский\n2-Мужской")
                    while check_param_bd(connection, event.user_id, 'sex') == 0:
                        response = vk_session.method('messages.getConversations',
                                                     {"offset": 0, "count": 1, "filter": 'unanswered'})
                        if len(response.get("items")) != 0:
                            update_param(connection, event.user_id, 'sex',
                                         response.get("items")[0].get('last_message').get("text"))
                    continue
                if check_param_bd(connection, event.user_id, 'city') == 0:
                    write_msg(event.user_id, f"Введи свой город:\n1-Москва\n2-Санкт-Петербург")
                    while check_param_bd(connection, event.user_id, 'city') == 0:
                        response = vk_session.method('messages.getConversations',
                                                     {"offset": 0, "count": 1, "filter": 'unanswered'})
                        if len(response.get("items")) != 0:
                            update_param(connection, event.user_id, 'city',
                                         response.get("items")[0].get('last_message').get("text"))
                    continue
                if check_param_bd(connection, event.user_id, 'relation') == 0:
                    write_msg(event.user_id,
                              f"Введи своё семейное положение:\n1-Не женат\n2-Встречаетесь\n3-Помолвлен\n6-В активном поиске")
                    while check_param_bd(connection, event.user_id, 'relation') == 0:
                        response = vk_session.method('messages.getConversations',
                                                     {"offset": 0, "count": 1, "filter": 'unanswered'})
                        if len(response.get("items")) != 0:
                            update_param(connection, event.user_id, 'relation',
                                         response.get("items")[0].get('last_message').get("text"))
                    write_msg(event.user_id, f"У тебя заполнены данные по профилю, можем начинать")
                    continue
            else:
                if event.text == 'начать' or event.text == '+':
                    write_msg(event.user_id, f"Поиск")
                    if get_param_bd(connection, event.user_id, 'offset') is None:
                        offset = 1
                    else:
                        offset = get_param_bd(connection, event.user_id, 'offset')
                    for id, name in search(event.user_id, 1, offset).items():
                        write_msg(event.user_id, f"https://vk.com/id{id}\n{name}")
                        for foto in get_photo(id).keys():
                            vk_session.method("messages.send", {"peer_id": event.user_id, "message": "",
                                                                "attachment": f"photo{id}_{foto}",
                                                                "random_id": 0})
                    write_msg(event.user_id, f"Поиск закончен\nЕсли хочешь продолжить введи команду '+'")
                else:
                    write_msg(event.user_id, f"Введи команду 'начать'")
