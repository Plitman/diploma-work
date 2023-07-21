import requests
from vk_api_wrapper import VkApiWrapper
from database_wrapper import DatabaseWrapper
from user import User
from vk_api.longpoll import VkLongPoll, VkEventType
import config  # Импорт файла конфигурации

def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7),})

def get_user_info(vk_api_wrapper, user_id):
    user = vk_api_wrapper.get_user_info(user_id)
    if user.get_age() is None or user.get_sex() is None or user.get_city() is None or user.get_relationship_status() is None:
        # Запросить недостающую информацию у пользователя
        write_msg(user_id, "Для работы сервиса необходимо заполнить информацию в профиле. Пожалуйста, укажите свой возраст, пол, город и семейное положение.")
        # Дополнительно запрашиваем информацию у пользователя, если она недостаточна
        # Для каждого атрибута можно использовать отдельное сообщение или одно сообщение с разделителями (например, "Введите информацию через пробел: возраст пол город семейное_положение")
        # Затем разделить полученные данные и заполнить значения атрибутов
        # Пример:
        # data = request.split()
        # age = data[0]
        # sex = data[1]
        # city = data[2]
        # relationship_status = data[3]
        # user.set_age(age)
        # user.set_sex(sex)
        # user.set_city(city)
        # user.set_relationship_status(relationship_status)
        return None
    else:
        return user

def send_photos(user_id, user, photos):
    message = f"Найден пользователь: vk.com/id{user.get_id()}\n\n"
    for i, (photo_url, likes_count, comments_count) in enumerate(photos, 1):
        message += f"Фото {i}:\n"
        message += f"Лайков: {likes_count}\n"
        message += f"Комментариев: {comments_count}\n"
        message += f"{photo_url}\n\n"
    write_msg(user_id, message)

if __name__ == '__main__':
    token = config.TOKEN

    vk_api_wrapper = VkApiWrapper(token)  # Инициализация объекта для работы с VK API
    db = DatabaseWrapper()  # Инициализация объекта для работы с базой данных

    vk_session = vk_api.VkApi(token=token)
    vk = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:

            if event.to_me:
                request = event.text

                if request == "привет":
                    write_msg(event.user_id, f"Хай, {event.user_id}")
                elif request == "пока":
                    write_msg(event.user_id, "Пока((")
                elif request.startswith("поиск"):
                    # Обработка команды поиска
                    user_id = event.user_id
                    user = db.get_user(user_id)
                    if user is None:
                        user = get_user_info(vk_api_wrapper, user_id)
                        if user is not None:
                            db.save_user(user)
                    else:
                        write_msg(user_id, "Вы уже выполнили поиск")

                    if user is not None:
                        matching_users = vk_api_wrapper.find_matching_users(user)
                        for matching_user in matching_users:
                            top_photos = vk_api_wrapper.get_top_photos(matching_user.id)
                            send_photos(user_id, matching_user, top_photos)
                    
                else:
                    write_msg(event.user_id, "Переформулируйте Ваш ответ...")
