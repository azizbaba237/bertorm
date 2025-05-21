from django.shortcuts import render, get_object_or_404
from .models import Parfum, Marque
from django.shortcuts import redirect
from django.contrib import messages
from .models import Panier, ArticlePanier
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import InscriptionForm

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


def detail_parfum(request, pk):
    parfum = get_object_or_404(Parfum, pk=pk)
    avis = parfum.avis.all().order_by('-date_creation')
    context = {
        'parfum': parfum,
        'avis': avis,
    }
    return render(request, 'core/detail_parfum.html', context)


# vue pour ajouter un parfum au panier
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
    return redirect('core:detail_parfum', pk=pk)

@login_required
def voir_panier(request):
    panier = get_object_or_404(Panier, utilisateur=request.user)
    context = {
        'panier': panier,
    }
    return render(request, 'core/panier.html', context)

def supprimer_du_panier(request, pk):
    article = get_object_or_404(ArticlePanier, pk=pk, panier__utilisateur=request.user)
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


# Vue pour le profil utilisateur
@login_required
def inscription(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('core:accueil')
    else:
        form = InscriptionForm()
    return render(request, 'core/inscription.html', {'form': form})