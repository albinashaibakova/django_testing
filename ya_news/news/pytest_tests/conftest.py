from datetime import datetime, timedelta

import pytest

from django.test.client import Client
from django.conf import settings
from django.utils import timezone

from news.models import Comment, News


@pytest.fixture(autouse=True)
def enable_db_access(db):
    pass


@pytest.fixture
def news(db):
    news = News.objects.create(
        title='Заголовок',
        text='Текст',
    )
    return news


@pytest.fixture
def multiple_news(db):
    today = datetime.today()
    multiple_news = []
    for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1):
        news = News(title=f'Новость {index}',
                    text='Просто текст.',
                    date=today - timedelta(days=index))
        multiple_news.append(news)
    News.objects.bulk_create(multiple_news)
    return multiple_news


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def comment(author, news):
    comment = Comment.objects.create(
        news=news,
        text='Текст',
        author=author,
    )
    return comment


@pytest.fixture
def multiple_comments(author, news):
    now = timezone.now()
    for index in range(10):
        comment = Comment.objects.create(
            news=news,
            author=author,
            text=f'Текст {index}',
        )
        comment.created = now + timedelta(days=index)
        comment.save()


@pytest.fixture
def id_for_args_comment(comment):
    return (comment.id,)


@pytest.fixture
def id_for_args_news(news):
    return (news.id,)


@pytest.fixture
def form_data():
    return {
        'text': 'Новый текст комментария',
        'news': news,
        'author': author_client,
    }


@pytest.fixture
def new_text():
    return 'Новый текст комментария'
