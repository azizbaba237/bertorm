from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model

class Marque(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    logo = models.ImageField(upload_to='marques/', blank=True, null=True)

    def __str__(self):
        return self.nom

class Parfum(models.Model):
    GENRE_CHOICES = [
        ('F', 'Féminin'),
        ('M', 'Masculin'),
        ('U', 'Unisexe'),
    ]

    nom = models.CharField(max_length=200)
    marque = models.ForeignKey(Marque, on_delete=models.CASCADE)
    genre = models.CharField(max_length=1, choices=GENRE_CHOICES)
    description = models.TextField()
    prix = models.DecimalField(max_digits=8, decimal_places=2)
    volume = models.PositiveIntegerField(help_text="Volume en ml")
    image = models.ImageField(upload_to='parfums/')
    note_principale = models.CharField(max_length=100)
    disponible = models.BooleanField(default=True)
    date_ajout = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom} - {self.marque}"

class Avis(models.Model):
    parfum = models.ForeignKey(Parfum, on_delete=models.CASCADE, related_name='avis')
    nom_client = models.CharField(max_length=100)
    note = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    commentaire = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Avis de {self.nom_client} sur {self.parfum}"

# Modele pour le panier
User = get_user_model()

class Panier(models.Model):
    utilisateur = models.OneToOneField(User, on_delete=models.CASCADE, related_name='panier')
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Panier de {self.utilisateur.username}"

    @property
    def total(self):
        return sum(item.sous_total for item in self.items.all())

    @property
    def nombre_articles(self):
        return sum(item.quantite for item in self.items.all())

class ArticlePanier(models.Model):
    panier = models.ForeignKey(Panier, on_delete=models.CASCADE, related_name='items')
    parfum = models.ForeignKey(Parfum, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=1)
    date_ajout = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantite} x {self.parfum.nom}"

    @property
    def sous_total(self):
        return self.quantite * self.parfum.prix
    
    
# Modele pour le profil utilisateur
class ProfilUtilisateur(models.Model):
    utilisateur = models.OneToOneField(User, on_delete=models.CASCADE)
    telephone = models.CharField(max_length=20, blank=True)
    adresse = models.TextField(blank=True)
    ville = models.CharField(max_length=100, blank=True)
    code_postal = models.CharField(max_length=10, blank=True)
    pays = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Profil de {self.utilisateur.username}"