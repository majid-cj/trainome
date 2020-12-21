from uuid import uuid4
import os

def wrapper_center_logo(instance, filename):
    ext = filename.split('.')[-1]
    return os.path.join('center/', '{}.{}'.format(uuid4().hex, ext))


def wrapper_course_cover(instance, filename):
    ext = filename.split('.')[-1]
    return os.path.join('course/', '{}.{}'.format(uuid4().hex, ext))


def wrapper_lecture_file(instance, filename):
    ext = filename.split('.')[-1]
    return os.path.join('lecture/', '{}.{}'.format(uuid4().hex, ext))


def wrapper_trainee_image(instance, filename):
    ext = filename.split('.')[-1]
    return os.path.join('trainee/', '{}.{}'.format(uuid4().hex, ext))


def wrapper_payment_screen_shot(instance, filename):
    ext = filename.split('.')[-1]
    return os.path.join('payment/', '{}.{}'.format(uuid4().hex, ext))
