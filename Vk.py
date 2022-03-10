from vk_api.longpoll import VkEventType
from db import insert_info_bd, update_param, check_param_bd, check_all_params, get_param_bd, connection
from algo import write_msg, get_info, search, get_photo, vk_session, longpoll

if __name__ == '__main__':
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
                        write_msg(event.user_id, f"Введи команду 'начать' или '+'")
