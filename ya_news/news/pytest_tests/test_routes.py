from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects


@pytest.mark.parametrize(
    'reverse_url',
    (pytest.lazy_fixture('home_url_reverse'),
     pytest.lazy_fixture('login_url_reverse'),
     pytest.lazy_fixture('logout_url_reverse'),
     pytest.lazy_fixture('signup_url_reverse'),)
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
    ((pytest.lazy_fixture('edit_url_reverse'),
      pytest.lazy_fixture('not_author_client'),
      HTTPStatus.NOT_FOUND),
     (pytest.lazy_fixture('delete_url_reverse'),
      pytest.lazy_fixture('author_client'), HTTPStatus.OK))
)
def test_pages_availability_for_different_users(
        parametrized_client, reverse_url,
        expected_status):
    response = parametrized_client.get(reverse_url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'reverse_url',
    (pytest.lazy_fixture('edit_url_reverse'),
     pytest.lazy_fixture('delete_url_reverse'))
)
def test_redirects(client, reverse_url, login_url_reverse):
    expected_url = f'{login_url_reverse}?next={reverse_url}'
    response = client.get(reverse_url)
    assertRedirects(response, expected_url)
