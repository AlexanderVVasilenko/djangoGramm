import pytest

from djangoGramm import settings


@pytest.fixture(scope='session')
def django_db_setup():
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgres',
        'HOST': 'localhost',
        'NAME': 'test',
        'ATOMIC_REQUESTS': True
}
