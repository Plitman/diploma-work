import requests
from vk_api_wrapper import VkApiWrapper
from database_wrapper import DatabaseWrapper
from user import User
from vk_api.longpoll import VkLongPoll, VkEventType
import config
from random import randrange

def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': randrange(10 ** 7)})

# Функция для запроса недостающей информации у пользователя
def request_missing_info(user_id, missing_info):
    message = "Для работы сервиса необходимо заполнить следующую информацию:\n"
    message += ", ".join(missing_info)
    write_msg(user_id, message)

if __name__ == '__main__':
    token = config.TOKEN

    vk_api_wrapper = VkApiWrapper(token)
    db = DatabaseWrapper()

    vk_session = vk_api.VkApi(token=token)
    vk = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:

            if event.to_me:
                request = event.text
                user_id = event.user_id

                if request == "привет":
                    write_msg(user_id, f"Хай, {user_id}")
                elif request == "пока":
                    write_msg(user_id, "Пока((")
                elif request.startswith("поиск"):
                    user = db.get_user(user_id)
                    
                    if user is None:
                        user = get_user_info(vk_api_wrapper, user_id)
                        if user is not None:
                            db.save_user(user)
                        else:
                            continue  # Если не удалось получить достаточную информацию, переходим к следующему событию
                    else:
                        write_msg(user_id, "Вы уже выполнили поиск")
                        continue  # Если поиск уже выполнен, переходим к следующему событию
                    
                    missing_info = []  # Список для хранения недостающей информации
                    if user.get_age() is None:
                        missing_info.append("возраст")
                    if user.get_sex() is None:
                        missing_info.append("пол")
                    if user.get_city() is None:
                        missing_info.append("город")
                    if user.get_relationship_status() is None:
                        missing_info.append("семейное положение")
                    
                    if missing_info:
                        request_missing_info(user_id, missing_info)
                    else:
                        matching_users = vk_api_wrapper.find_matching_users(user)
                        for matching_user in matching_users:
                            top_photos = vk_api_wrapper.get_top_photos(matching_user.id)
                            send_photos(user_id, matching_user, top_photos)
                    
                else:
                    write_msg(user_id, "Переформулируйте Ваш ответ...")
