from django.test import TestCase
from django.test.client import Client
from authapp.models import ShopUser
from django.core.management import call_command
from django.conf import settings


class TestUserManagement(TestCase):

    def setUp(self):
        call_command('flush', '--noinput')
        call_command('loaddata', 'test_db.json')
        self.client = Client()

        self.superuser = ShopUser.objects.create_superuser(
            'admin',
            'admin@geekshop.local',
            'cirijifi'
        )
        self.user = ShopUser.objects.create_user(
            'user01',
            'user01@geekshop.local',
            'cirijifi'
        )
        self.user_with__first_name = ShopUser.objects.create_user(
            'user02',
            'user02@geekshop.local',
            'cirijifi',
            first_name='Ann'
        )

    def test_user_login(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_anonymous)
        self.assertEqual(response.context['title'], 'главная')
        self.assertNotContains(response, 'Пользователь', status_code=200)

        self.client.login(username='user01', password='cirijifi')

        response = self.client.get('/auth/login/')
        self.assertFalse(response.context['user'].is_anonymous)
        self.assertEqual(response.context['user'], self.user)

        response = self.client.get('/')
        self.assertContains(response, 'Пользователь', status_code=200)
        self.assertEqual(response.context['user'], self.user)

    def test_basket_login_redirect(self):
        response = self.client.get('/basket/')
        self.assertEqual(response.url, '/auth/login/?next=/basket/')
        self.assertEqual(response.status_code, 302)

        self.client.login(username='user01', password='cirijifi')

        response = self.client.get('/basket/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['basket']), [])
        self.assertEqual(response.request['PATH_INFO'], '/basket/')
        # self.assertIn('Ваша корзина,Пользователь', response.content.decode())

    def test_user_logout(self):
        self.client.login(username='user02', password='cirijifi')

        response = self.client.get('/auth/login/')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_anonymous)

        response = self.client.get('/auth/logout/')
        self.assertEqual(response.status_code, 302)

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_anonymous)

    def test_user_register(self):
        response = self.client.get('/auth/register/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['title'], 'регистрация')
        self.assertTrue(response.context['user'].is_anonymous)

        new_user_data = {
            'username': 'User03',
            'first_name': 'John',
            'last_name': 'Doe',
            'password1': 'cirijifi',
            'password2': 'cirijifi',
            'email': 'john@geekshop.local',
            'age': '33'}

        response = self.client.post('/auth/register/', data=new_user_data)
        self.assertEqual(response.status_code, 302)

        new_user = ShopUser.objects.get(username=new_user_data['username'])

        activation_url = f'{settings.DOMAIN_NAME}/auth/verify/'\
            f'{new_user_data["email"]}/{new_user.activation_key}/'

        response = self.client.get(activation_url)
        self.assertEqual(response.status_code, 200)

        self.client.login(username=new_user_data['username'],
                          password=new_user_data['password1'])

        response = self.client.get('/auth/login/')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_anonymous)

        response = self.client.get('/')
        self.assertContains(response, text=new_user_data['first_name'],
                            status_code=200)

    def test_user_wrong_register(self):
        new_user_data = {
            'username': 'user04',
            'first_name': 'Danis',
            'last_name': 'Smith',
            'password1': 'cirijifi',
            'password2': 'cirijifi',
            'email': 'danis@geekshop.local',
            'age': '10'}

        response = self.client.post('/auth/register/', data=new_user_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'register_form', 'age',
                             'Вы слишком молоды!')

    def tearDown(self):
        call_command('sqlsequencereset', 'mainapp', 'authapp',
                     'ordersapp', 'basketapp')
