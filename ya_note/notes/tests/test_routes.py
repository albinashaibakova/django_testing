from http import HTTPStatus

from .test_fixtures import BaseTestCase


class TestRoutes(BaseTestCase):

    def test_page_availability_for_anonymous_user(self):
        urls = (
            self.HOME_URL_REVERSE,
            self.LOGIN_URL_REVERSE,
            self.LOGOUT_URL_REVERSE,
            self.SIGNUP_URL_REVERSE,
        )

        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_availability_for_auth_user(self):
        urls = (
            self.NOTES_URL_REVERSE,
            self.NOTE_ADD_URL_REVERSE,
            self.SUCCESS_URL_REVERSE,
        )
        for url in urls:
            with self.subTest(url=url):
                response = self.auth_client.get(url)
                assert response.status_code == HTTPStatus.OK

    def test_availability_for_different_users(self):
        users_statuses = (
            (self.auth_client, HTTPStatus.OK),
            (self.not_author_client, HTTPStatus.NOT_FOUND),)
        for user, status in users_statuses:
            for url in (self.EDIT_URL_REVERSE,
                        self.DELETE_URL_REVERSE,
                        self.DETAIL_URL_REVERSE):
                with self.subTest(user=user, url=url):
                    response = user.get(url)
                    self.assertEqual(response.status_code, status)

    def test_redirect(self):
        urls = (
            self.EDIT_URL_REVERSE,
            self.DELETE_URL_REVERSE,
            self.DETAIL_URL_REVERSE,
            self.NOTE_ADD_URL_REVERSE,
            self.SUCCESS_URL_REVERSE,
            self.NOTES_URL_REVERSE,
        )

        for url in urls:
            with self.subTest(url=url):
                redirect_url = f'{self.LOGIN_URL_REVERSE}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)
