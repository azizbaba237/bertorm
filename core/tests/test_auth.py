from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from core.models import ProfilUtilisateur, Panier

User = get_user_model()

class AuthTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_user_creation(self):
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(self.user.username, 'testuser')
    
    def test_profile_creation(self):
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertEqual(ProfilUtilisateur.objects.count(), 1)
    
    def test_panier_creation(self):
        self.assertTrue(hasattr(self.user, 'panier'))
        self.assertEqual(Panier.objects.count(), 1)
    
    def test_login_view(self):
        response = self.client.get(reverse('core:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/auth/login.html')
    
    def test_successful_login(self):
        response = self.client.post(reverse('core:login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertRedirects(response, reverse('core:account_dashboard'))
    
    def test_account_dashboard_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('core:account_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/auth/account_dashboard.html')
    
    def test_account_dashboard_unauthenticated(self):
        response = self.client.get(reverse('core:account_dashboard'))
        self.assertRedirects(response, f"{reverse('core:login')}?next={reverse('core:account_dashboard')}")