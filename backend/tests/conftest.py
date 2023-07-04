import os
import sys

import django
from django.conf import settings
from django.utils.version import get_version

os.environ[
    'DJANGO_SETTINGS_MODULE'
] = 'backend.settings'  # замените на ваш путь
django.setup()


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

root_dir_content = os.listdir(BASE_DIR)
PROJECT_DIR_NAME = 'backend'

if PROJECT_DIR_NAME not in root_dir_content or not os.path.isdir(
    os.path.join(BASE_DIR, PROJECT_DIR_NAME)
):
    assert False, (
        f'В директории `{BASE_DIR}` не найдена папка c проектом '
        f'`{PROJECT_DIR_NAME}`. Убедитесь, что у вас верная структура проекта.'
    )

MANAGE_PATH = os.path.join(BASE_DIR)
project_dir_content = os.listdir(MANAGE_PATH)
FILENAME = 'manage.py'

if FILENAME not in project_dir_content:
    assert False, (
        f'В директории `{MANAGE_PATH}` не найден файл `{FILENAME}`. '
        f'Убедитесь, что у вас верная структура проекта.'
    )

pytest_plugins = [
    'tests.fixtures.fixture_user',
]
