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
        if response.status_code == 200:
            data = response.json()
            if 'response' in data:
                user_data = data['response'][0]
                id = user_data.get('id', None)
                bdate = user_data.get('bdate', None)
                sex = user_data.get('sex', None)
                city = user_data.get('city', {}).get('title', '') if 'city' in user_data else ''
                relationship_status = user_data.get('relation', '') if 'relation' in user_data else ''

                if id is not None and bdate is not None and sex is not None:
                    age = self.calculate_age(bdate)
                    return User(id=id, age=age, sex=sex, city=city, relationship_status=relationship_status)

        return None

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
        if response.status_code == 200:
            data = response.json()
            if 'response' in data:
                photos = data['response']['items']
                top_photos = []
                for photo in photos:
                    photo_url = photo['sizes'][-1]['url']
                    likes_count = photo['likes']['count']
                    comments_count = photo['comments']['count']
                    top_photos.append((photo_url, likes_count, comments_count))
                return top_photos

        return []
