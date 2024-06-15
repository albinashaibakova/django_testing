from datetime import datetime, timedelta

import pytest
from django.conf import settings
from django.test.client import Client
from django.urls import reverse
from django.utils import timezone

from news.models import Comment, News


@pytest.fixture(autouse=True)
def enable_db_access(db):
    pass


@pytest.fixture
def home_url_reverse():
    return reverse('news:home')


@pytest.fixture
def login_url_reverse():
    return reverse('users:login')


@pytest.fixture
def logout_url_reverse():
    return reverse('users:logout')


@pytest.fixture
def signup_url_reverse():
    return reverse('users:signup')


@pytest.fixture
def detail_url_reverse(news):
    return reverse('news:detail', args=(news.id,))


@pytest.fixture
def edit_url_reverse(comment):
    return reverse('news:edit', args=(comment.id,))


@pytest.fixture
def delete_url_reverse(comment):
    return reverse('news:delete', args=(comment.id,))


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
    multiple_news = [
        News(title=f'Новость {index}',
             text='Просто текст.',
             date=today - timedelta(days=index))
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ]
    News.objects.bulk_create(multiple_news)


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
