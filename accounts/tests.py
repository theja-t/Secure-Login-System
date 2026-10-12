from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class AuthenticationFlowTests(TestCase):
    def test_signup_creates_user_with_hashed_password_and_logs_in(self):
        response = self.client.post(reverse('signup'), {
            'username': 'mira',
            'email': 'Mira@example.com',
            'password1': 'a-strong-test-password-482!',
            'password2': 'a-strong-test-password-482!',
        })

        user = User.objects.get(username='mira')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(user.email, 'mira@example.com')
        self.assertTrue(user.check_password('a-strong-test-password-482!'))
        self.assertIn('_auth_user_id', self.client.session)

    def test_signup_rejects_duplicate_email_case_insensitively(self):
        User.objects.create_user(
            username='existing', email='person@example.com', password='a-strong-test-password-482!'
        )

        response = self.client.post(reverse('signup'), {
            'username': 'another',
            'email': 'PERSON@example.com',
            'password1': 'a-strong-test-password-482!',
            'password2': 'a-strong-test-password-482!',
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'An account with this email already exists.')
        self.assertFalse(User.objects.filter(username='another').exists())

    def test_dashboard_requires_authentication(self):
        response = self.client.get(reverse('dashboard'))

        self.assertRedirects(response, f"{reverse('login')}?next={reverse('dashboard')}")

    def test_user_can_sign_in_and_sign_out(self):
        User.objects.create_user(
            username='mira', email='mira@example.com', password='a-strong-test-password-482!'
        )

        login_response = self.client.post(reverse('login'), {
            'username': 'mira',
            'password': 'a-strong-test-password-482!',
        })
        self.assertRedirects(login_response, reverse('dashboard'))
        self.assertEqual(self.client.get(reverse('dashboard')).status_code, 200)

        logout_response = self.client.post(reverse('logout'))
        self.assertRedirects(logout_response, reverse('login'))
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_logout_rejects_get_requests(self):
        response = self.client.get(reverse('logout'))

        self.assertEqual(response.status_code, 405)

    def test_repeated_failed_signins_lock_out_valid_login(self):
        User.objects.create_user(
            username='mira', email='mira@example.com', password='a-strong-test-password-482!'
        )
        for _ in range(5):
            self.client.post(reverse('login'), {
                'username': 'mira',
                'password': 'incorrect-password',
            })

        response = self.client.post(reverse('login'), {
            'username': 'mira',
            'password': 'a-strong-test-password-482!',
        })

        self.assertNotEqual(response.status_code, 302)
        self.assertNotIn('_auth_user_id', self.client.session)
