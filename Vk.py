from random import randrange
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from Token import token
from pprint import pprint

vk_session = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk_session)


def age(b_date):
    b_date.split('.')
    return b_date  # дописать получение полных лет


def check_data(result_dict):
    extra_list = []
    for key, value in result_dict.items():
        if value is None:
            extra_list.append(key)
    return extra_list  # Получаемы все незаполненые поля


def write_msg(user_id, message):
    vk_session.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': randrange(10 ** 7), })


def get_info(user_id):
    info = vk_session.method('users.get', {"user_ids": user_id, "fields": "bdate,sex,city,relation"})
    result_dict = {'age': info[0].get('bdate'), 'sex': info[0].get('sex'), 'city': info[0].get('city'),
                   'relation': info[0].get('relation')}
    return result_dict # Получаем всю инфу по пользователю


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            info = get_info(event.user_id)
            if len(check_data(info)) != 0:
                write_msg(event.user_id, f"У тебя не заполнены данные по профилю дополни информацию о себе:")
                if info.get("age") is None:
                    write_msg(event.user_id, f"Введи свой возраст:")
                    age = -1
                    while info['age'] is None:
                        response = vk_session.method('messages.getConversations',
                                                     {"offset": 0, "count": 1, "filter": 'unanswered'})
                        if len(response.get("items")) != 0:
                            info['age'] = response.get("items")[0].get('last_message').get("text")
                            print(info.get("age"))
                if info.get("sex") is None:
                    write_msg(event.user_id, f"Введи своё семейное положение:")
                    while info['sex'] is None:
                        response = vk_session.method('messages.getConversations',
                                                     {"offset": 0, "count": 1, "filter": 'unanswered'})
                        if len(response.get("items")) != 0:
                            info['sex'] = response.get("items")[0].get('last_message').get("text")
                            print(info["relation"])
                if info.get("city") is None:
                    write_msg(event.user_id, f"Введи своё семейное положение:")
                    while info['city'] is None:
                        response = vk_session.method('messages.getConversations',
                                                     {"offset": 0, "count": 1, "filter": 'unanswered'})
                        if len(response.get("items")) != 0:
                            info['city'] = response.get("items")[0].get('last_message').get("text")
                            print(info["city"])
                if info.get("relation") is None:
                    write_msg(event.user_id, f"Введи своё семейное положение:")
                    while info['relation'] is None:
                        response = vk_session.method('messages.getConversations',
                                                     {"offset": 0, "count": 1, "filter": 'unanswered'})
                        if len(response.get("items")) != 0:
                            info['relation'] = response.get("items")[0].get('last_message').get("text")
                            print(info["relation"])
            else:
                write_msg(event.user_id, f"У тебя заполнены данные по профилю")
