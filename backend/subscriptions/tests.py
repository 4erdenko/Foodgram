# import pytest
# from faker import Faker
# from rest_framework import status
# from rest_framework.test import APIClient
# from subscriptions.models import Subscription
# from users.models import User
#
# class TestSubscriptionViews:
#     fake = Faker()
#
#     @pytest.fixture
#     def api_client(self):
#         return APIClient()
#
#     @pytest.fixture
#     def test_username(self):
#         return self.fake.unique.user_name()
#
#     @pytest.fixture
#     def test_password(self):
#         return self.fake.password()
#
#     @pytest.fixture
#     def test_email(self):
#         return self.fake.unique.email()
#
#     @pytest.fixture
#     def create_user(self, db, test_password, test_username, test_email):
#         return User.objects.create_user(
#             username=test_username, email=test_email, password=test_password
#         )
#
#     @pytest.fixture
#     def create_second_user(self, db, test_password, test_username, test_email):
#         return User.objects.create_user(
#             username=f'second_{test_username}',
#             email=f'second_{test_email}',
#             password=test_password,
#         )
#
#     @pytest.fixture
#     def get_or_create_subscription(self, db):
#         def _create_subscription(follower, following):
#             subscription, created = Subscription.objects.get_or_create(
#                 follower=follower, following=following
#             )
#             return subscription
#
#         return _create_subscription
#
#     @pytest.fixture
#     def authorized_client(self, db, create_user, api_client):
#         api_client.force_authenticate(user=create_user)
#         return api_client
#
#     @pytest.mark.django_db
#     def test_user_subscriptions_list_view(
#             self,
#             create_user,
#             authorized_client,
#             get_or_create_subscription,
#             create_second_user,
#     ):
#         get_or_create_subscription(create_user, create_second_user)
#         response = authorized_client.get('/api/users/subscriptions/')
#         assert response.status_code == status.HTTP_200_OK
#         assert len(response.data['results']) == 1
#
#     @pytest.mark.django_db
#     def test_user_subscribe_view(self, authorized_client, create_second_user):
#         response = authorized_client.post(
#             f'/api/users' f'/{create_second_user.id}/subscribe/'
#         )
#         assert response.status_code == status.HTTP_201_CREATED
#         assert Subscription.objects.count() == 1
#
#     @pytest.mark.django_db
#     def test_user_unsubscribe_view(
#             self,
#             create_user,
#             authorized_client,
#             create_second_user,
#             get_or_create_subscription,
#     ):
#         get_or_create_subscription(create_user, create_second_user)
#         assert Subscription.objects.count() == 1
#         response = authorized_client.delete(
#             f'/api/users/{create_second_user.id}/subscribe/'
#         )
#         assert response.status_code == status.HTTP_204_NO_CONTENT
#         assert Subscription.objects.count() == 0
