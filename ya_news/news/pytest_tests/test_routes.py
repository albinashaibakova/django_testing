from http import HTTPStatus
import pytest
from pytest_django.asserts import assertRedirects
from pytest_lazyfixture import lazy_fixture as lf


@pytest.mark.parametrize(
    'reverse_url',
    (lf('home_url_reverse'),
     lf('login_url_reverse'),
     lf('logout_url_reverse'),
     lf('signup_url_reverse'),)
)
def test_pages_availability(client, reverse_url):
    url = reverse_url
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


def test_news_detail_page(client, detail_url_reverse):
    response = client.get(detail_url_reverse)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'reverse_url, parametrized_client, expected_status',
    ((lf('edit_url_reverse'),
      lf('not_author_client'),
      HTTPStatus.NOT_FOUND),
     (lf('delete_url_reverse'),
      lf('author_client'), HTTPStatus.OK))
)
def test_pages_availability_for_different_users(
        parametrized_client, reverse_url,
        expected_status):
    response = parametrized_client.get(reverse_url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'reverse_url',
    (lf('edit_url_reverse'),
     lf('delete_url_reverse'))
)
def test_redirects(client, reverse_url, login_url_reverse):
    expected_url = f'{login_url_reverse}?next={reverse_url}'
    response = client.get(reverse_url)
    assertRedirects(response, expected_url)
