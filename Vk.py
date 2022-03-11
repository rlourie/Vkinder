import vk_api
from Token import token, access_token
from vk_api.longpoll import VkLongPoll, VkEventType
from db import BD
from algo import write_msg, get_info, search, get_photo

if __name__ == '__main__':

    vk_session = vk_api.VkApi(token=token)
    vk_user_session = vk_api.VkApi(token=access_token)
    longpoll = VkLongPoll(vk_session)
    My_bd = BD()
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                My_bd.insert_info_bd(event.user_id, get_info(event.user_id, vk_session))
                if My_bd.check_all_params(event.user_id) == 0:
                    write_msg(event.user_id, vk_session,
                              f"У тебя не заполнены данные по профилю, дополни информацию о себе:")
                    if My_bd.check_param_bd(event.user_id, 'age') == 0:
                        write_msg(event.user_id, vk_session, f"Введи свой возраст:")
                        while My_bd.check_param_bd(event.user_id, 'age') == 0:
                            response = vk_session.method('messages.getConversations',
                                                         {"offset": 0, "count": 1, "filter": 'unanswered'})
                            if len(response.get("items")) != 0:
                                My_bd.update_param(event.user_id, 'age',
                                                   response.get("items")[0].get('last_message').get("text"))
                        continue
                    if My_bd.check_param_bd(event.user_id, 'sex') == 0:
                        write_msg(event.user_id, vk_session, f"Введи своё пол:\n1-Женский\n2-Мужской")
                        while My_bd.check_param_bd(event.user_id, 'sex') == 0:
                            response = vk_session.method('messages.getConversations',
                                                         {"offset": 0, "count": 1, "filter": 'unanswered'})
                            if len(response.get("items")) != 0:
                                My_bd.update_param(event.user_id, 'sex',
                                                   response.get("items")[0].get('last_message').get("text"))
                        continue
                    if My_bd.check_param_bd(event.user_id, 'city') == 0:
                        write_msg(event.user_id, vk_session, f"Введи свой город:\n1-Москва\n2-Санкт-Петербург")
                        while My_bd.check_param_bd(event.user_id, 'city') == 0:
                            response = vk_session.method('messages.getConversations',
                                                         {"offset": 0, "count": 1, "filter": 'unanswered'})
                            if len(response.get("items")) != 0:
                                My_bd.update_param(event.user_id, 'city',
                                                   response.get("items")[0].get('last_message').get("text"))
                        continue
                    if My_bd.check_param_bd(event.user_id, 'relation') == 0:
                        write_msg(event.user_id, vk_session,
                                  f"Введи своё семейное положение:\n1-Не женат\n2-Встречаетесь\n3-Помолвлен\n6-В активном поиске")
                        while My_bd.check_param_bd(event.user_id, 'relation') == 0:
                            response = vk_session.method('messages.getConversations',
                                                         {"offset": 0, "count": 1, "filter": 'unanswered'})
                            if len(response.get("items")) != 0:
                                My_bd.update_param(event.user_id, 'relation',
                                                   response.get("items")[0].get('last_message').get("text"))
                        write_msg(event.user_id, vk_session, f"У тебя заполнены данные по профилю, можем начинать")
                        continue
                else:
                    if event.text == 'начать' or event.text == '+':
                        write_msg(event.user_id, vk_session, f"Поиск")
                        if My_bd.get_param_bd(event.user_id, 'offset') is None:
                            offset = 1
                        else:
                            offset = My_bd.get_param_bd(event.user_id, 'offset')
                        for id, name in search(event.user_id, 1, offset, vk_user_session).items():
                            write_msg(event.user_id, vk_session, f"https://vk.com/id{id}\n{name}")
                            My_bd.insert_search(event.user_id, id)
                            for foto in get_photo(id, vk_user_session).keys():
                                vk_session.method("messages.send", {"peer_id": event.user_id, "message": "",
                                                                    "attachment": f"photo{id}_{foto}",
                                                                    "random_id": 0})
                        write_msg(event.user_id, vk_session,
                                  f"Поиск закончен\nЕсли хочешь продолжить введи команду '+'")
                    else:
                        write_msg(event.user_id, vk_session, f"Введи команду 'начать' или '+'")
