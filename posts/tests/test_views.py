from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from posts.views import UserView, PostView, CommentViewList
from posts.models import User, Post, Comment


class UserTests(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()

    def create_user(self):
        url = reverse('users')
        data = {'displayName': 'test1', 'firstName': 'testFirstName', 'lastName': 'testLastName', 'password1': '1234', 'password2': '1234', 'email': 'test@test.com'}
        request = self.factory.post(url, data=data)
        view = UserView.as_view()
        response = view(request)
        user = User.objects.get(username='test1')
        return user

    def test_user_create_account(self):

        url = reverse('users')
        data = {'displayName': 'test1', 'firstName': 'testFirstName', 'lastName': 'testLastName', 'password1': '1234', 'password2': '1234', 'email': 'test@test.com'}
        request = self.factory.post(url, data=data)
        view = UserView.as_view()
        response = view(request)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

    def test_user_creation_requires_valid_email(self):
        url = reverse('users')
        data = {'displayName': 'test1', 'firstName': 'testFirstName', 'lastName': 'testLastName', 'password1': '1234',
                'password2': '1234', 'email': 'testtest.com'}
        request = self.factory.post(url, data=data)
        view = UserView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_get_info(self):
        user = self.create_user()
        url = reverse('users')
        request = self.factory.get(url)
        view = UserView.as_view()
        force_authenticate(request, user=user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['displayName'], user.username)
        self.assertEqual(response.data['lastName'], user.last_name)

    def test_user_update_info(self):
        user = self.create_user()
        url = reverse('users')
        data = {'firstName': 'New First Name'}
        request = self.factory.put(url, data=data)
        view = UserView.as_view()
        force_authenticate(request, user)
        response = view(request)
        self.assertEqual(response.data['firstName'], 'New First Name')


# class PostTests(APITestCase):
#
#     def setUp(self):
#         self.factory = APIRequestFactory()
#
#     def create_user(self):
#         url = reverse('users')
#         data = {'displayName': 'user1', 'firstName': 'James', 'lastName': 'Bond', 'password1': '1234', 'password2': '1234', 'email': 'test@test.com'}
#         request = self.factory.post(url, data=data)
#         view = UserView.as_view()
#         response = view(request)
#         user = User.objects.get(username='user1')
#         return user
#
#     def test_create_post(self):
#         user = self.create_user()
#         url = reverse('posts')
#         # data = {'displayName': 'test1', 'firstName': 'testFirstName', 'lastName': 'testLastName', 'password1': '1234', 'password2': '1234', 'email': 'test@test.com'}
#         data = {
#             'title':'A post title', 'source':'http://lastplaceigotthisfrom.com/posts/yyyyy',
#             'origin':'http://whereitcamefrom.com/posts/zzzzz', 'description':'A post description',
#             'contentType':'text/plain', 'content':'some content', 'author':user,
#             'published':'2015-03-09T13:07:04+00:00', 'visibility':'PUBLIC', 'unlisted':False
#         }
#         request = self.factory.post(url, data=data, format='json')
#         print(request.body)
#         view = PostView.as_view()
#         response = view(request)
#         print(response)
#
#         # user = Post.objects.get(username='test1')
#         # return user
