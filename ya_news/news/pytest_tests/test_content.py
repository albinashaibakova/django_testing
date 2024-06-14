from django.conf import settings

from news.forms import CommentForm


def test_news_count(client, home_url_reverse, multiple_news):
    response = client.get(home_url_reverse)
    news_count = response.context['object_list'].count()
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_order(client, home_url_reverse, multiple_news):
    response = client.get(home_url_reverse)
    all_dates = [news.date for news in response.context['object_list']]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


def test_comments_order(client, detail_url_reverse, multiple_comments):
    response = client.get(detail_url_reverse)
    assert 'news' in response.context
    all_comments = response.context['news'].comment_set.all()
    all_timestamps = [comment.created for comment in all_comments]
    sorted_timestamps = sorted(all_timestamps)
    assert all_timestamps == sorted_timestamps


def test_anonymous_client_has_no_form(client, detail_url_reverse):
    response = client.get(detail_url_reverse)
    assert 'form' not in response.context


def test_authorized_client_has_form(author_client, detail_url_reverse):
    response = author_client.get(detail_url_reverse)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)
