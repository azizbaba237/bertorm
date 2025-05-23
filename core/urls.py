from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('parfums/', views.liste_parfums, name='liste_parfums'),
    path('parfum/<int:pk>/', views.detail_parfum, name='detail_parfum'),
    path('panier/', views.voir_panier, name='voir_panier'),
    path('panier/ajouter/<int:pk>/', views.ajouter_au_panier, name='ajouter_au_panier'),
    path('panier/supprimer/<int:pk>/', views.supprimer_du_panier, name='supprimer_du_panier'),
    path('panier/modifier/<int:pk>/', views.modifier_quantite, name='modifier_quantite'),
    path('recherche/', views.rechercher_parfums, name='recherche'),
    path('commande/', views.passer_commande, name='passer_commande'),
    path('commande/<str:numero_commande>/', views.detail_commande, name='detail_commande'),
    path('commandes/', views.HistoriqueCommandes.as_view(), name='historique_commandes'),
    #path('adresses/', views.gestion_adresses, name='gestion_adresses'),
    #path('coupons/', views.gestion_coupons, name='gestion_coupons'),  # Pour l'admin
    
]