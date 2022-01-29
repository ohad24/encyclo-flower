import random
import string
import uuid


def id_generator(length=7, chars=string.ascii_uppercase + string.digits):
    return "".join(random.choice(chars) for _ in range(length))


def question_id_generator():
    return "q-" + id_generator()


def gen_uuid():
    return str(uuid.uuid4())
