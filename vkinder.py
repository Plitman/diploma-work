from random import randrange
from vk_api_wrapper import VkApiWrapper
from database_wrapper import DatabaseWrapper
from user import User

def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7),})

def get_user_info(vk_api_wrapper, user_id):
    user = vk_api_wrapper.get_user_info(user_id)
    # Дополнительно запрашиваем информацию у пользователя, если она недостаточна
    return user

...

token = input('Token: ')

vk_api_wrapper = VkApiWrapper(token)  # Инициализация объекта для работы с VK API
db = DatabaseWrapper()  # Инициализация объекта для работы с базой данных

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:

        if event.to_me:
            request = event.text

            if request == "привет":
                write_msg(event.user_id, f"Хай, {event.user_id}")
            elif request == "пока":
                write_msg(event.user_id, "Пока((")
            else:
                write_msg(event.user_id, "Не поняла вашего ответа...")

            user_id = event.user_id
            user = db.get_user(user_id)
            if user is None:
                user = get_user_info(vk_api_wrapper, user_id)
                db.save_user(user)

            matching_users = db.find_matching_users(user)
            for matching_user in matching_users:
                top_photos = vk_api_wrapper.get_top_photos(matching_user.id)
                send_photos(user_id, matching_user, top_photos)
def send_photos(user_id, user, photos):
    message = f"Найден пользователь: vk.com/id{user.get_id()}\n\n"
    for i, (photo_url, likes_count, comments_count) in enumerate(photos, 1):
        message += f"Фото {i}:\n"
        message += f"Лайков: {likes_count}\n"
        message += f"Комментариев: {comments_count}\n"
        message += f"{photo_url}\n\n"
    write_msg(user_id, message)
