from django.shortcuts import render, get_object_or_404
from .models import Parfum, Marque
from django.shortcuts import redirect
from django.contrib import messages
from .models import Panier, ArticlePanier
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import AdresseLivraisonForm, PaiementForm, CouponForm
from django.views.generic import ListView
import random
import string

def accueil(request):
    parfums = Parfum.objects.filter(disponible=True).order_by('-date_ajout')[:8]
    marques = Marque.objects.all()
    context = {
        'parfums': parfums,
        'marques': marques,
    }
    return render(request, 'core/index.html', context)

def liste_parfums(request):
    parfums = Parfum.objects.filter(disponible=True)
    genre = request.GET.get('genre', None)
    marque = request.GET.get('marque', None)

    if genre:
        parfums = parfums.filter(genre=genre)
    if marque:
        parfums = parfums.filter(marque__id=marque)

    context = {
        'parfums': parfums,
        'marques': Marque.objects.all(),
    }
    return render(request, 'core/liste_parfums.html', context)

# Pour afficher les détails d'un parfum
def detail_parfum(request, pk):
    parfum = get_object_or_404(Parfum, pk=pk)
    avis = parfum.avis.all().order_by('-date_creation')
    context = {
        'parfum': parfum,
        'avis': avis,
    }
    return render(request, 'core/detail_parfum.html', context)

# Pour la gestion du panier
@login_required
def voir_panier(request):
    panier, created = Panier.objects.get_or_create(utilisateur=request.user)
    context = {
        'panier': panier,
    }
    return render(request, 'core/panier.html', context)

@login_required
def ajouter_au_panier(request, pk):
    parfum = get_object_or_404(Parfum, pk=pk)
    panier, created = Panier.objects.get_or_create(utilisateur=request.user)
    
    article, created = ArticlePanier.objects.get_or_create(
        panier=panier,
        parfum=parfum,
        defaults={'quantite': 1}
    )
    
    if not created:
        article.quantite += 1
        article.save()
    
    messages.success(request, f"{parfum.nom} a été ajouté à votre panier.")
    return redirect(request.META.get('HTTP_REFERER', 'core:accueil'))

@login_required
def supprimer_du_panier(request, pk):
    article = get_object_or_404(ArticlePanier, pk=pk, panier__utilisateur=request.user)
    article.delete()
    messages.success(request, "L'article a été supprimé du panier.")
    return redirect('core:voir_panier')

@login_required
def modifier_quantite(request, pk):
    if request.method == 'POST':
        article = get_object_or_404(ArticlePanier, pk=pk, panier__utilisateur=request.user)
        quantite = int(request.POST.get('quantite', 1))
        
        if quantite > 0:
            article.quantite = quantite
            article.save()
            messages.success(request, "La quantité a été mise à jour.")
        else:
            article.delete()
            messages.success(request, "L'article a été supprimé du panier.")
    
    return redirect('core:voir_panier')

# Pour faire la recherche
def rechercher_parfums(request):
    query = request.GET.get('q', '')
    
    if query:
        parfums = Parfum.objects.filter(
            models.Q(nom__icontains=query) | 
            models.Q(marque__nom__icontains=query) |
            models.Q(note_principale__icontains=query)
        ).distinct()
    else:
        parfums = Parfum.objects.none()
    
    context = {
        'parfums': parfums,
        'query': query,
    }
    return render(request, 'core/recherche.html', context)


# Pour gérer les commandes
@login_required
def passer_commande(request):
    panier = get_object_or_404(Panier, utilisateur=request.user)
    methodes_livraison = MethodeLivraison.objects.filter(actif=True)
     
    if not panier.items.exists():
        messages.warning(request, "Votre panier est vide.")
        return redirect('core:voir_panier')
    
    if request.method == 'POST':
        adresse_form = AdresseLivraisonForm(request.POST, user=request.user)
        paiement_form = PaiementForm(request.POST)
        coupon_form = CouponForm(request.POST)
        methode_livraison_id = request.POST.get('methode_livraison')
        
        
        try:
            methode_livraison = MethodeLivraison.objects.get(id=methode_livraison_id, actif=True)
        except MethodeLivraison.DoesNotExist:
            messages.error(request, "Méthode de livraison invalide.")
            return redirect('core:passer_commande')
        
        if adresse_form.is_valid() and paiement_form.is_valid():
            # Gestion de l'adresse
            if adresse_form.cleaned_data['adresse_existante']:
                adresse = AdresseLivraison.objects.get(
                    id=adresse_form.cleaned_data['adresse_existante'],
                    utilisateur=request.user
                )
            else:
                adresse = AdresseLivraison.objects.create(
                    utilisateur=request.user,
                    nom_complet=adresse_form.cleaned_data['nom_complet'],
                    adresse=adresse_form.cleaned_data['adresse'],
                    ville=adresse_form.cleaned_data['ville'],
                    code_postal=adresse_form.cleaned_data['code_postal'],
                    pays=adresse_form.cleaned_data['pays'],
                    telephone=adresse_form.cleaned_data['telephone'],
                    par_defaut=adresse_form.cleaned_data['par_defaut']
                )
            
            # Gestion du coupon
            reduction = 0
            coupon = None
            if coupon_form.is_valid() and coupon_form.cleaned_data['code']:
                try:
                    coupon = Coupon.objects.get(code=coupon_form.cleaned_data['code'], actif=True)
                    reduction = coupon.calculer_reduction(panier.total)
                except Coupon.DoesNotExist:
                    messages.error(request, "Code promo invalide.")
                    return redirect('core:passer_commande')
            
            # Création de la commande
            numero_commande = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            commande = Commande.objects.create(
                utilisateur=request.user,
                numero_commande=numero_commande,
                adresse_livraison=adresse,
                total=panier.total - reduction + methode_livraison.prix,
                reduction=reduction,
                coupon=coupon,
                methode_paiement=paiement_form.cleaned_data['methode_paiement'],
                #frais_livraison=0,  # À adapter selon votre système de livraison
                frais_livraison=methode_livraison.prix,
                methode_livraison=methode_livraison,
            )
            
            # Création des articles de commande
            for article_panier in panier.items.all():
                ArticleCommande.objects.create(
                    commande=commande,
                    parfum=article_panier.parfum,
                    quantite=article_panier.quantite,
                    prix=article_panier.parfum.prix
                )
            
            # Vider le panier
            panier.items.all().delete()
            
            messages.success(request, f"Votre commande #{numero_commande} a été passée avec succès!")
            return redirect('core:detail_commande', numero_commande=numero_commande)
    else:
        adresse_form = AdresseLivraisonForm(user=request.user)
        paiement_form = PaiementForm()
        coupon_form = CouponForm()
    
    context = {
        'panier': panier,
        'adresse_form': adresse_form,
        'paiement_form': paiement_form,
        'coupon_form': coupon_form,
        'methodes_livraison': methodes_livraison,
    }
    return render(request, 'core/passer_commande.html', context)

@login_required
def detail_commande(request, numero_commande):
    commande = get_object_or_404(Commande, numero_commande=numero_commande, utilisateur=request.user)
    context = {
        'commande': commande,
    }
    return render(request, 'core/detail_commande.html', context)

class HistoriqueCommandes(ListView):
    model = Commande
    template_name = 'core/historique_commandes.html'
    context_object_name = 'commandes'
    
    def get_queryset(self):
        return Commande.objects.filter(utilisateur=self.request.user).order_by('-date_commande')
