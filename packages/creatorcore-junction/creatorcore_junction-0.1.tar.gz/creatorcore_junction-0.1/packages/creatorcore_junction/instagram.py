from creatorcore_junction.connection import Connection

INSTAGRAM = "instagram"


class Instagram:
    def __init__(self, url, api_key):
        self.connection = Connection(url, api_key)

    def collect_user(self, username):
        content = self.connection.junction_request(INSTAGRAM, "user", {"username": username})
        return content

    def collect_user_by_id(self, user_id):
        content = self.connection.junction_request(INSTAGRAM, "user_by_id", {"user_id": user_id})
        return content

    def collect_posts_by_user_id(self, user_id):
        content = self.connection.junction_request(INSTAGRAM, "posts_by_user_id", {"user_id": user_id})
        return content

    def collect_hashtag(self, hashtag):
        content = self.connection.junction_request(INSTAGRAM, "hashtag", {"hashtag": hashtag})
        return content

    def collect_posts_by_hashtag(self, hashtag):
        content = self.connection.junction_request(INSTAGRAM, "posts_by_hashtag", {"hashtag": hashtag})
        return content

    def collect_sound(self, sound_id):
        content = self.connection.junction_request(INSTAGRAM, "sound", {"sound_id": sound_id})
        return content
