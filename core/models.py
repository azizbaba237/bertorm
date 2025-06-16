from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone

# Modele pour les utilisateurs (déplacé en premier)
class User(AbstractUser):
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    email_verified = models.BooleanField(default=False)
    newsletter_subscription = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'

    def __str__(self):
        return self.username

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
class Panier(models.Model):
    utilisateur = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='panier')
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
    utilisateur = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profil')
    telephone = models.CharField(max_length=20, blank=True)
    adresse = models.TextField(blank=True)
    ville = models.CharField(max_length=100, blank=True)
    code_postal = models.CharField(max_length=10, blank=True)
    pays = models.CharField(max_length=100, blank=True)
    date_naissance = models.DateField(null=True, blank=True)
    preferences_newsletter = models.JSONField(default=dict, blank=True)  # Pour stocker les préférences

    def __str__(self):
        return f"Profil de {self.utilisateur.username}"
    
    def adresse_complete(self):
        return f"{self.adresse}, {self.code_postal} {self.ville}, {self.pays}"
    
# Modele pour les commandes
class AdresseLivraison(models.Model):
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='adresses_livraison')
    nom_complet = models.CharField(max_length=100)
    adresse = models.CharField(max_length=255)
    societe = models.CharField(max_length=100, blank=True)  # Optionnel pour les livraisons en entreprise
    ville = models.CharField(max_length=100)
    complement = models.CharField(max_length=255, blank=True)
    code_postal = models.CharField(max_length=20)
    pays = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)
    par_defaut = models.BooleanField(default=False)
    notes = models.TextField(blank=True)  # Instructions spéciales pour la livraison

    class Meta:
        verbose_name_plural = "Adresses de livraison"
        ordering = ['-par_defaut', 'ville']
        
    def __str__(self):
        return f"{self.nom_complet}, {self.adresse}, {self.ville}"
    

    def save(self, *args, **kwargs):
        # S'assurer qu'il n'y a qu'une seule adresse par défaut
        if self.par_defaut:
            AdresseLivraison.objects.filter(utilisateur=self.utilisateur, par_defaut=True).update(par_defaut=False)
        super().save(*args, **kwargs)

class Commande(models.Model):
    STATUT_CHOICES = (
        ('en_attente', 'En attente'),
        ('en_traitement', 'En traitement'),
        ('expediee', 'Expédiée'),
        ('livree', 'Livrée'),
        ('annulee', 'Annulée'),
    )

    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    numero_commande = models.CharField(max_length=20, unique=True)
    adresse_livraison = models.ForeignKey(AdresseLivraison, on_delete=models.SET_NULL, null=True)
    date_commande = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    total = models.DecimalField(max_digits=10, decimal_places=2)
    coupon = models.ForeignKey('Coupon', on_delete=models.SET_NULL, null=True, blank=True)
    reduction = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    frais_livraison = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    methode_paiement = models.CharField(max_length=50)
    methode_livraison = models.ForeignKey(
        'MethodeLivraison',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Méthode de livraison"
    )

    def __str__(self):
        return f"Commande #{self.numero_commande}"
    
    @property
    def total_avant_reduction(self):
        return self.total - self.frais_livraison

class ArticleCommande(models.Model):
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE, related_name='articles')
    parfum = models.ForeignKey(Parfum, on_delete=models.SET_NULL, null=True)
    quantite = models.PositiveIntegerField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantite} x {self.parfum.nom}"

    @property
    def sous_total(self):
        return self.quantite * self.prix
    
# Modele pour les coupons
class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    reduction = models.DecimalField(max_digits=5, decimal_places=2)
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    actif = models.BooleanField(default=True)
    utilisations_max = models.PositiveIntegerField(default=1)
    utilisations = models.PositiveIntegerField(default=0)
    min_panier = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.code

    def est_valide(self):
        now = timezone.now()
        return (self.actif and 
                self.date_debut <= now <= self.date_fin and 
                self.utilisations < self.utilisations_max)

    def calculer_reduction(self, total_panier):
        if not self.est_valide():
            return 0
        if self.min_panier and total_panier < self.min_panier:
            return 0
        return min(total_panier * (self.reduction / 100), total_panier)
    
# Modele pour les méthodes de livraison
class MethodeLivraison(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    delai = models.CharField(max_length=100)
    actif = models.BooleanField(default=True)

    def __str__(self):
        return self.nom
    
# model de paiement
class Paiement(models.Model):
    METHODE_CHOICES = (
        ('carte', 'Carte de crédit'),
        ('paypal', 'PayPal'),
        ('virement', 'Virement bancaire'),
    )
    
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    methode = models.CharField(max_length=20, choices=METHODE_CHOICES)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=100, blank=True)
    statut = models.CharField(max_length=20, default='en_attente')

    def __str__(self):
        return f"Paiement {self.id} - {self.methode}"
    
# Modèle pour la vérification d'email
class EmailVerificationToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_valid(self):
        return timezone.now() < self.expires_at

# Modèle pour les tokens de réinitialisation
class PasswordResetToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_valid(self):
        return timezone.now() < self.expires_at

# Modèle pour l'historique des connexions
class UserLoginHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    user_agent = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Historique des connexions"
        ordering = ['-timestamp']