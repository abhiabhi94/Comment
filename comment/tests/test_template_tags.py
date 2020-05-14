from unittest.mock import patch

from django.core.exceptions import ImproperlyConfigured
from django.test import RequestFactory
from django.template import TemplateSyntaxError

from comment.forms import CommentForm
from comment.templatetags.comment_tags import (
    get_model_name, get_app_name, get_comment_count, get_img_path, get_profile_url, render_comments,
    include_static_jquery, include_bootstrap, include_static, render_field, add_one_arg, has_reacted
)
from comment.tests.base import BaseCommentTest
from django.conf import settings


class TemplateTagsTest(BaseCommentTest):
    def setUp(self):
        super().setUp()
        self.factory = RequestFactory()
        settings.PROFILE_APP_NAME = 'profile'
        self.parent_comment_1 = self.create_comment(self.content_object_1)
        self.parent_comment_2 = self.create_comment(self.content_object_1)
        self.parent_comment_3 = self.create_comment(self.content_object_1)
        self.child_comment_1 = self.create_comment(self.content_object_1, parent=self.parent_comment_1)
        self.child_comment_2 = self.create_comment(self.content_object_1, parent=self.parent_comment_2)
        self.child_comment_3 = self.create_comment(self.content_object_1, parent=self.parent_comment_2)
        self.reaction_1 = self.create_reaction(self.user_1, self.parent_comment_1, 'like')
        self.reaction_2 = self.create_reaction(self.user_1, self.parent_comment_2, 'dislike')
        self.reaction_3 = self.create_reaction(self.user_1, self.parent_comment_3, 'like')

    def test_get_model_name(self):
        model_name = get_model_name(self.post_1)
        self.assertEqual(model_name, 'Post')

    def test_get_app_name(self):
        app_name = get_app_name(self.post_1)
        self.assertEqual(app_name, 'post')

    def test_comment_count(self):
        counts = get_comment_count(self.post_1)
        self.assertEqual(counts, 6)

    def test_profile_url(self):
        # success
        url = get_profile_url(self.parent_comment_1)
        self.assertEqual(url, '/profile/profile/test-1')
        # fail
        settings.PROFILE_APP_NAME = 'app not exist'
        url = get_profile_url(self.parent_comment_1)
        self.assertEqual(url, '')

        settings.PROFILE_APP_NAME = None
        url = get_profile_url(self.parent_comment_1)
        self.assertEqual(url, '')

    def test_img_url(self):
        url = get_img_path(self.parent_comment_1)
        self.assertNotEqual(url, '')
        # fail
        settings.PROFILE_APP_NAME = 'app not exist'
        url = get_img_path(self.parent_comment_1)
        self.assertEqual(url, '')

        settings.PROFILE_APP_NAME = None
        url = get_img_path(self.parent_comment_1)
        self.assertEqual(url, '')

    def test_profile_has_no_image_field(self):
        mocked_hasattr = patch('comment.templatetags.comment_tags.hasattr').start()
        mocked_hasattr.return_value = False
        url = get_img_path(self.parent_comment_1)
        self.assertEqual(url, '')

    def test_render_comments(self):
        request = self.factory.get('/')
        request.user = self.user_1
        data = render_comments(self.post_1, request, comments_per_page=None)
        self.assertEqual(data['comments'].count(), 3)  # parent comment only
        self.assertEqual(data['login_url'], '/' + settings.LOGIN_URL)

        # LOGIN_URL is not provided
        setattr(settings, 'LOGIN_URL', None)
        with self.assertRaises(ImproperlyConfigured) as error:
            render_comments(self.post_1, request)
        self.assertIsInstance(error.exception, ImproperlyConfigured)

        # check pagination
        setattr(settings, 'LOGIN_URL', '/login')
        request = self.factory.get('/?page=2')
        request.user = self.user_1
        data = render_comments(self.post_1, request, comments_per_page=2)
        self.assertTrue(data['comments'].has_previous())
        self.assertEqual(data['comments'].paginator.per_page, 2)  # 2 comment per page
        self.assertEqual(data['comments'].number, 2)  # 3 comment fit in 2 pages
        self.assertEqual(data['login_url'], settings.LOGIN_URL)

        # check not integer page
        request = self.factory.get('/?page=string')
        request.user = self.user_1
        data = render_comments(self.post_1, request, comments_per_page=2)
        self.assertFalse(data['comments'].has_previous())

        # check empty page
        request = self.factory.get('/?page=10')
        request.user = self.user_1
        data = render_comments(self.post_1, request, comments_per_page=2)
        self.assertTrue(data['comments'].has_previous())

    def test_static_functions(self):
        self.assertIsNone(include_static())
        self.assertIsNone(include_bootstrap())
        self.assertIsNone(include_static_jquery())

    def test_render_field(self):
        form = CommentForm()
        for field in form.visible_fields():
            self.assertIsNone(field.field.widget.attrs.get('placeholder'))
            field = render_field(field, placeholder='placeholder')
            self.assertEqual(field.field.widget.attrs.get('placeholder'), 'placeholder')

    def test_add_one_arg(self):
        """Test whether this function returns a tuple of the elements passed"""
        comment = self.parent_comment_1
        user = self.user_1
        self.assertTupleEqual((comment, user), add_one_arg(comment, user))

    def test_has_reacted_on_incorrect_reaction(self):
        """Test whether this function raises an error when incorrect reaction is passed"""
        comment = self.parent_comment_1
        user = self.user_1
        self.client.force_login(user)
        comment_and_user = add_one_arg(comment, user)
        self.assertRaises(TemplateSyntaxError, has_reacted, comment_and_user, 'likes')

    def test_has_reacted_on_correct_reaction(self):
        """Test whether this function returns an appropriate boolean when correct reaction is passed"""
        comment = self.parent_comment_1
        user = self.user_1
        self.client.force_login(user)
        comment_and_user = add_one_arg(comment, user)
        self.assertEqual(True, has_reacted(comment_and_user, 'like'))
        self.assertEqual(False, has_reacted(comment_and_user, 'dislike'))

        # check for other users
        user = self.user_2
        self.client.force_login(user)
        comment_and_user = add_one_arg(comment, user)

        self.assertEqual(False, has_reacted(comment_and_user, 'like'))
        self.assertEqual(False, has_reacted(comment_and_user, 'dislike'))

        # check for other comments
        comment_and_user = add_one_arg(self.parent_comment_2, user)
        self.assertEqual(False, has_reacted(comment_and_user, 'like'))
        self.assertEqual(False, has_reacted(comment_and_user, 'dislike'))
