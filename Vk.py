from random import randrange
import vk_api
import math
from vk_api.longpoll import VkLongPoll, VkEventType
from Token import token
from db import insert_info_bd, update_param, check_param_bd, check_all_params, connection
from datetime import datetime
from pprint import pprint

vk_session = vk_api.VkApi(token=token)
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


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            flag = 1
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
                    write_msg(event.user_id, f"Введи своё семейное положение:\n1-Встречаюсь\n2-В браке\n3-Свободен")
                    while check_param_bd(connection, event.user_id, 'relation') == 0:
                        response = vk_session.method('messages.getConversations',
                                                     {"offset": 0, "count": 1, "filter": 'unanswered'})
                        if len(response.get("items")) != 0:
                            update_param(connection, event.user_id, 'relation',
                                         response.get("items")[0].get('last_message').get("text"))
                    write_msg(event.user_id,
                              f"У тебя заполнены данные по профилю, можем начинать")
                    continue
            else:
                if event.text == 'начать':
                    write_msg(event.user_id, f"Поиск")
                else:
                    write_msg(event.user_id, f"Введи команду 'начать'")
