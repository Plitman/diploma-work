class User:
    def __init__(self, id, age, sex, city, relationship_status):
        self.id = id
        self.age = age
        self.sex = sex
        self.city = city
        self.relationship_status = relationship_status

    def get_id(self):
        return self.id

    def get_age(self):
        return self.age

    def get_sex(self):
        return self.sex

    def get_city(self):
        return self.city

    def get_relationship_status(self):
        return self.relationship_status
