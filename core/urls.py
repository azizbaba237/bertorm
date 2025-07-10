from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import custom_login_view, privacy_policy
from django.urls import reverse_lazy
from django.contrib.auth.views import LogoutView

app_name = 'core'

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('parfums/', views.liste_parfums, name='liste_parfums'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('parfum/<int:pk>/', views.detail_parfum, name='detail_parfum'),
    path('panier/', views.voir_panier, name='voir_panier'),
    path('panier/ajouter/<int:pk>/', views.ajouter_au_panier, name='ajouter_au_panier'),
    path('panier/supprimer/<int:pk>/', views.supprimer_du_panier, name='supprimer_du_panier'),
    path('panier/modifier/<int:pk>/', views.modifier_quantite, name='modifier_quantite'),
    path('recherche/', views.rechercher_parfums, name='recherche'),
    path('commande/', views.passer_commande, name='passer_commande'),
    path('commande/<str:numero_commande>/', views.detail_commande, name='detail_commande'),
    path('commandes/', views.HistoriqueCommandes.as_view(), name='historique_commandes'),
    # Authentification et profil utilisateur
    path('compte/', views.account_dashboard, name='account_dashboard'),
    #path('compte/profil/', views.ProfileUpdateView.as_view(), name='profile_update'),
    path('login/', auth_views.LoginView.as_view(
        template_name='core/auth/login.html',
        redirect_authenticated_user=True,
        success_url=reverse_lazy('core:accueil'),
    ), name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.custom_logout, name='logout'),
    # path('logout/', LogoutView.as_view(next_page='core:accueil'), name='logout'),
    
    path('compte/', views.account_dashboard, name='account_dashboard'),
    path('compte/profil/', views.profil, name='profil'),
    path('compte/commandes/', views.HistoriqueCommandes.as_view(), name='historique_commandes'),
    # Test URL
    path('test-account_dasboard/', views.test_account_dasboard, name='test_account_dasboard'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='core/auth/password_reset.html'), name='password_reset'),
    path('privacy/', privacy_policy, name='privacy'),
    path('delete-data/', views.delete_data, name='delete-data'),
    
]
    
