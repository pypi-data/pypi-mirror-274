import os

from creatorcore_junction.instagram import Instagram

JUNCTION_URL = os.getenv("JUNCTION_URL")
JUNCTION_API_KEY = os.getenv("JUNCTION_API_KEY")
instagram = Instagram(JUNCTION_URL, JUNCTION_API_KEY)


def test_collect_user():
    user = instagram.collect_user("creatorcore.co")
    assert user["username"] == "creatorcore.co"


def test_collect_user_by_id():
    user = instagram.collect_user_by_id("57185224903")
    assert user["username"] == "creatorcore.co"


def test_collect_posts_by_user_id():
    posts = instagram.collect_posts_by_user_id("57185224903")
    assert len(posts) > 0


def test_collect_hashtag():
    hashtag = instagram.collect_hashtag("conure")
    assert hashtag["name"] == "conure"


def test_collect_posts_by_hashtag():
    posts = instagram.collect_posts_by_hashtag("conure")
    assert len(posts) > 0


def test_collect_sound():
    sound = instagram.collect_sound("1078085933293572")
    assert sound["status"] == "ok"
