import requests

class VkApiWrapper:
    def __init__(self, token):
        self.token = token

    def get_user_info(self, user_id):
        params = {
            'user_ids': user_id,
            'fields': 'bdate,sex,city,relation',
            'access_token': self.token,
            'v': '5.131'
        }
        response = requests.get('https://api.vk.com/method/users.get', params=params)
        data = response.json()
        user_data = data['response'][0]
        id = user_data['id']
        age = self.calculate_age(user_data['bdate'])
        sex = user_data['sex']
        city = user_data.get('city', {}).get('title', '')
        relationship_status = user_data.get('relation', '')

        return User(id=id, age=age, sex=sex, city=city, relationship_status=relationship_status)

    def calculate_age(self, bdate):
        # Реализовать функцию для расчета возраста пользователя по его дате рождения
        pass

    def get_top_photos(self, user_id):
        params = {
            'owner_id': user_id,
            'album_id': 'profile',
            'extended': 1,
            'count': 3,
            'access_token': self.token,
            'v': '5.131'
        }
        response = requests.get('https://api.vk.com/method/photos.get', params=params)
        data = response.json()
        photos = data['response']['items']
        top_photos = []
        for photo in photos:
            photo_url = photo['sizes'][-1]['url']
            likes_count = photo['likes']['count']
            comments_count = photo['comments']['count']
            top_photos.append((photo_url, likes_count, comments_count))
        return top_photos
