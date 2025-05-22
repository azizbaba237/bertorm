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
    
]