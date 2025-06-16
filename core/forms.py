from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import AdresseLivraison, Coupon
from .models import Marque, MethodeLivraison
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from .models import ProfilUtilisateur
from django.contrib.auth.models import User



class AdresseLivraisonForm(forms.Form):
    adresse_existante = forms.ChoiceField(
        choices=[],
        required=False,
        label="Choisir une adresse enregistrée"
    )
    nom_complet = forms.CharField(max_length=100, required=False)
    adresse = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
    ville = forms.CharField(max_length=100, required=False)
    code_postal = forms.CharField(max_length=20, required=False)
    pays = forms.CharField(max_length=100, required=False)
    telephone = forms.CharField(max_length=20, required=False)
    par_defaut = forms.BooleanField(required=False, label="Enregistrer comme adresse par défaut")

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            # Remplir les choix d'adresses existantes
            adresses = AdresseLivraison.objects.filter(utilisateur=user)
            choices = [('', '--------')] + [(a.id, str(a)) for a in adresses]
            self.fields['adresse_existante'].choices = choices

    def clean(self):
        cleaned_data = super().clean()
        adresse_existante = cleaned_data.get('adresse_existante')
        
        # Si aucune adresse existante n'est sélectionnée, valider les champs de la nouvelle adresse
        if not adresse_existante:
            required_fields = ['nom_complet', 'adresse', 'ville', 'code_postal', 'pays', 'telephone']
            for field in required_fields:
                if not cleaned_data.get(field):
                    self.add_error(field, "Ce champ est obligatoire")
        
        return cleaned_data

class PaiementForm(forms.Form):
    METHODES_PAIEMENT = [
        ('carte', 'Carte de crédit'),
        ('paypal', 'PayPal'),
        ('virement', 'Virement bancaire'),
    ]
    
    methode_paiement = forms.ChoiceField(
        choices=METHODES_PAIEMENT,
        widget=forms.RadioSelect,
        initial='carte'
    )

class CouponForm(forms.Form):
    code = forms.CharField(
        label="Code promo",
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Entrez votre code promo'})
    )

    def clean_code(self):
        code = self.cleaned_data.get('code')
        if code:
            try:
                coupon = Coupon.objects.get(code=code)
                if not coupon.est_valide():
                    raise ValidationError("Ce coupon n'est plus valide")
            except Coupon.DoesNotExist:
                raise ValidationError("Code promo invalide")
        return code

class CouponAdminForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = '__all__'
        widgets = {
            'date_debut': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'date_fin': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        date_debut = cleaned_data.get('date_debut')
        date_fin = cleaned_data.get('date_fin')
        
        if date_debut and date_fin and date_debut > date_fin:
            raise ValidationError("La date de fin doit être postérieure à la date de début")
        
        return cleaned_data

class MethodeLivraisonForm(forms.ModelForm):
    class Meta:
        model = MethodeLivraison
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class FiltreParfumsForm(forms.Form):
    GENRE_CHOICES = [
        ('', 'Tous genres'),
        ('F', 'Féminin'),
        ('M', 'Masculin'),
        ('U', 'Unisexe'),
    ]
    
    genre = forms.ChoiceField(
        choices=GENRE_CHOICES,
        required=False,
        label="Genre"
    )
    marque = forms.ModelChoiceField(
        queryset=Marque.objects.all(),
        required=False,
        label="Marque",
        empty_label="Toutes marques"
    )
    prix_min = forms.DecimalField(
        required=False,
        min_value=0,
        max_digits=10,
        decimal_places=2,
        label="Prix min"
    )
    prix_max = forms.DecimalField(
        required=False,
        min_value=0,
        max_digits=10,
        decimal_places=2,
        label="Prix max"
    )

    def clean(self):
        cleaned_data = super().clean()
        prix_min = cleaned_data.get('prix_min')
        prix_max = cleaned_data.get('prix_max')
        
        if prix_min and prix_max and prix_min > prix_max:
            raise ValidationError("Le prix minimum ne peut pas être supérieur au prix maximum")
        
        return cleaned_data
  
  
User = get_user_model()  

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    accept_cgu = forms.BooleanField(required=True, label="J'accepte les conditions générales d'utilisation")
    newsletter = forms.BooleanField(required=False, label="S'abonner à la newsletter")
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'accept_cgu', 'newsletter']


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone', 'avatar']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = ProfilUtilisateur
        fields = ['date_naissance', 'telephone', 'adresse', 'ville', 'code_postal', 'pays']

class AdresseLivraisonModelForm(forms.ModelForm):
    class Meta:
        model = AdresseLivraison
        fields = ['nom_complet', 'societe', 'adresse', 'complement', 'ville', 'code_postal', 'pays', 'telephone', 'par_defaut', 'notes']
        widgets = {
            'par_defaut': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class EmailVerificationForm(forms.Form):
    email = forms.EmailField()

class PasswordResetForm(forms.Form):
    email = forms.EmailField()