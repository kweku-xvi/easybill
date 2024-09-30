import random, string


def generate_id(n:int):
    characters = string.ascii_letters + string.digits
    id_generated = ''.join(random.choices(characters, k=n))

    return id_generated