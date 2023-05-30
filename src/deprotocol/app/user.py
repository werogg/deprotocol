class UserHelper:
    _instance = None

    def __init__(self, nickname='default', profile_img=''):
        self.user = User(nickname=nickname, profile_img=profile_img)

    @classmethod
    def get_user(cls):
        return cls._instance.user if cls._instance else User()

    @classmethod
    def set_nickname(cls, nickname):
        if cls._instance:
            cls._instance.user.nickname = nickname

    @classmethod
    def set_profile_img(cls, profile_img):
        if cls._instance:
            cls._instance.user.profile_img = profile_img

    @classmethod
    def get_user_helper(cls):
        """ Singleton method to get the UserHelper instance """
        if not cls._instance:
            cls._instance = cls(nickname='default', profile_img='')
        return cls._instance


class User:
    def __init__(self, nickname='default', profile_img=''):
        self.nickname = nickname
        self.profile_img = profile_img
