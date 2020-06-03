from django.utils import timezone
from oauth2_provider.models import get_application_model, get_access_token_model
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User
from .models import Calculate

Application = get_application_model()
AccessToken = get_access_token_model()


class FlowTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='testing@gmail.com', first_name='Test', last_name='User', password='testing321')
        self.application = Application(
            name="Test Application",
            redirect_uris="http://localhost",
            user=self.user,
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_PASSWORD,
        )
        self.application.save()
        self.access_token = AccessToken.objects.create(
            user=self.user, token='1234567890',
            application=self.application, scope='read write',
            expires=timezone.now() + timezone.timedelta(seconds=300)
        )
        self.auth = "Bearer {0}".format(self.access_token.token)
        self.access_token.scope = "read"
        self.access_token.save()

    def test_flow(self):
        response_add = self.client.post('/api/add/', {'array': 16}, HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response_add.status_code, status.HTTP_200_OK)
        print(response_add.data['array'])

        response_calculate = self.client.get('/api/calculate/', HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response_calculate.status_code, status.HTTP_200_OK)
        print(response_calculate.data)

        response_reset = self.client.post('/api/reset/', HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response_reset.status_code, status.HTTP_200_OK)
        print(response_reset.data)

        response_history = self.client.get('/api/history/', HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response_history.status_code, status.HTTP_200_OK)
        print(response_history.data)

        response_history_id = self.client.get('/api/history/1/', HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response_history_id.status_code, status.HTTP_200_OK)
        print(response_history_id.data)


class AddTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='testing@gmail.com', first_name='Test', last_name='User', password='testing321')
        self.application = Application(
            name="Test Application",
            redirect_uris="http://localhost",
            user=self.user,
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_PASSWORD,
        )
        self.application.save()
        self.access_token = AccessToken.objects.create(
            user=self.user, token='1234567890',
            application=self.application, scope='read write',
            expires=timezone.now() + timezone.timedelta(seconds=300)
        )
        self.auth = "Bearer {0}".format(self.access_token.token)
        self.access_token.scope = "read"
        self.access_token.save()

    def test_add_unauthenticated(self):
        response = self.client.post('/api/add/', {'array': 2})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_add(self):
        response = self.client.post('/api/add/', {'array': 6}, HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data['array'][0])

    def test_add_none(self):
        response = self.client.post('/api/add/', {'array': ''}, HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_float(self):
        response = self.client.post('/api/add/', {'array': 23.2}, HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_string(self):
        response = self.client.post('/api/add/', {'array': 'testing'}, HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CalculateTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='testing@gmail.com', first_name='Test', last_name='User', password='testing321')
        self.application = Application(
            name="Test Application",
            redirect_uris="http://localhost",
            user=self.user,
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_PASSWORD,
        )
        self.application.save()
        self.access_token = AccessToken.objects.create(
            user=self.user, token='1234567890',
            application=self.application, scope='read write',
            expires=timezone.now() + timezone.timedelta(seconds=300)
        )
        self.auth = "Bearer {0}".format(self.access_token.token)
        self.access_token.scope = "read"
        self.access_token.save()

    def test_calculate(self):
        self.client.post('/api/add/', data={'array': 16}, HTTP_AUTHORIZATION=self.auth)
        self.client.post('/api/add/', {'array': 20}, HTTP_AUTHORIZATION=self.auth)
        response = self.client.get('/api/calculate/', HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)

    def test_calculate_all(self):
        self.client.post('/api/add/', {'array': 4}, HTTP_AUTHORIZATION=self.auth)
        self.client.post('/api/add/', {'array': 10}, HTTP_AUTHORIZATION=self.auth)
        self.client.get('/api/calculate/', HTTP_AUTHORIZATION=self.auth)
        response = self.client.get('/api/calculate/all/', HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)


class ResetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='testing@gmail.com', first_name='Test', last_name='User', password='testing321')
        self.application = Application(
            name="Test Application",
            redirect_uris="http://localhost",
            user=self.user,
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_PASSWORD,
        )
        self.application.save()
        self.access_token = AccessToken.objects.create(
            user=self.user, token='1234567890',
            application=self.application, scope='read write',
            expires=timezone.now() + timezone.timedelta(seconds=300)
        )
        self.auth = "Bearer {0}".format(self.access_token.token)
        self.access_token.scope = "read"
        self.access_token.save()
        self.client.post('/api/add/', {'array': 4}, HTTP_AUTHORIZATION=self.auth)
        self.client.post('/api/add/', {'array': 10}, HTTP_AUTHORIZATION=self.auth)

    def test_reset(self):
        response = self.client.post('/api/reset/',  HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)

    def test_reset_empty(self):
        from calculate.api.views import ARRAY
        self.obj = ARRAY.clear()
        response = self.client.post('/api/reset/', HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        print(response.data)


class HistoryTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='testing@gmail.com', first_name='Test', last_name='User', password='testing321')
        self.application = Application(
            name="Test Application",
            redirect_uris="http://localhost",
            user=self.user,
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_PASSWORD,
        )
        self.application.save()
        self.access_token = AccessToken.objects.create(
            user=self.user, token='1234567890',
            application=self.application, scope='read write',
            expires=timezone.now() + timezone.timedelta(seconds=300)
        )
        self.auth = "Bearer {0}".format(self.access_token.token)
        self.access_token.scope = "read"
        self.access_token.save()
        self.calculate = Calculate.objects.create(user=self.user, array=[16, 20], calculations=36)

    def test_history(self):
        response = self.client.get('/api/history/', HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(dict(response.data['data'][0]))

    def test_history_empty(self):
        self.obj = Calculate.objects.all().delete()
        response = self.client.get('/api/history/', HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        print(response.data)


class HistoryDetailTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='testing@gmail.com', first_name='Test', last_name='User', password='testing321')
        self.application = Application(
            name="Test Application",
            redirect_uris="http://localhost",
            user=self.user,
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_PASSWORD,
        )
        self.application.save()
        self.access_token = AccessToken.objects.create(
            user=self.user, token='1234567890',
            application=self.application, scope='read write',
            expires=timezone.now() + timezone.timedelta(seconds=300)
        )
        self.auth = "Bearer {0}".format(self.access_token.token)
        self.access_token.scope = "read"
        self.access_token.save()
        self.calculate = Calculate.objects.create(user=self.user, array=[16, 20], calculations=36)

    def test_history_detail(self):
        response = self.client.get('/api/history/{}/'.format(self.calculate.pk), HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)

    def test_history_detail_empty(self):
        self.obj = Calculate.objects.filter(pk=self.calculate.pk).delete()
        response = self.client.get('/api/history/{}/'.format(self.obj), HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

