import random
import string
import uuid


def id_generator(length=7, chars=string.ascii_lowercase + string.digits):
    return "".join(random.choice(chars) for _ in range(length))


def user_id_generator():
    return "u-" + id_generator()


def question_id_generator():
    return "q-" + id_generator()


def observation_id_generator():
    return "o-" + id_generator()


def gen_uuid():
    return uuid.uuid4().hex


def gen_image_file_name(file_name: str) -> str:
    return gen_uuid() + "." + file_name.split(".")[-1]


def email_verification_token():
    return gen_uuid()
