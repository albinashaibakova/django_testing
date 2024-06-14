from http import HTTPStatus
from random import choice

from django.urls import reverse
from pytest_django.asserts import assertRedirects, assertFormError

from news.models import Comment
from news.forms import BAD_WORDS, WARNING


def test_anonymous_user_cant_create_comment(client, delete_url_reverse):
    COMMENT_TEXT = 'Текст комментария'
    Comment.objects.all().delete()
    form_data = {'text': COMMENT_TEXT}
    response = client.post(delete_url_reverse, data=form_data)
    login_url = reverse('users:login')
    expected_url = f'{login_url}?next={delete_url_reverse}'
    assertRedirects(response, expected_url)
    assert Comment.objects.count() == 0


def test_user_can_create_note(author_client, news, author, detail_url_reverse):
    COMMENT_TEXT = 'Текст комментария'
    Comment.objects.all().delete()
    form_data = {'text': COMMENT_TEXT}
    response = author_client.post(detail_url_reverse, data=form_data)
    assertRedirects(response, f'{detail_url_reverse}#comments')
    assert Comment.objects.count() == 1
    new_comment = Comment.objects.get()
    assert new_comment.text == form_data['text']
    assert new_comment.author == author
    assert new_comment.news == news


def test_user_cant_use_bad_words(author_client, detail_url_reverse):
    bad_words_data = {'text': f'Какой-то текст, '
                              f'{choice(BAD_WORDS)}, еще текст'}
    Comment.objects.all().delete()
    response = author_client.post(detail_url_reverse, data=bad_words_data)
    comments_count = Comment.objects.all().count()
    assert comments_count == 0
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING
    )


def test_author_can_edit_comment(author_client, comment, news,
                                 detail_url_reverse,
                                 author, edit_url_reverse):
    NEW_COMMENT_TEXT = 'Новый текст комментария'
    form_data = {'text': NEW_COMMENT_TEXT}
    response = author_client.post(edit_url_reverse, form_data)
    assertRedirects(response,
                    f'{detail_url_reverse}#comments')
    comment.refresh_from_db()
    assert comment.text == form_data['text']
    assert comment.author == author
    assert comment.news == news


def test_user_cant_edit_comment_of_another_user(not_author_client,
                                                comment,
                                                edit_url_reverse,
                                                author, news):
    NEW_COMMENT_TEXT = 'Новый текст комментария'
    form_data = {'text': NEW_COMMENT_TEXT}
    form_data['text'] = NEW_COMMENT_TEXT
    response = not_author_client.post(edit_url_reverse, form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment_from_db = Comment.objects.get(id=comment.id)
    assert comment_from_db.text == comment.text
    assert comment.author == author
    assert comment.news == news


def test_author_can_delete_comment(author_client, detail_url_reverse,
                                   delete_url_reverse):
    response = author_client.post(delete_url_reverse)
    assertRedirects(response,
                    f'{detail_url_reverse}#comments')
    assert Comment.objects.count() == 0


def test_user_cant_delete_comment_of_another_user(not_author_client,
                                                  delete_url_reverse):
    response = not_author_client.post(delete_url_reverse)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == 1
