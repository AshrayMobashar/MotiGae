from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from .models import Station, Fare, Offer, Ticket
from django.contrib.auth.models import User
from django import forms
from .models import Station, Train

User = get_user_model()

class UserRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)
        
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')  # Customize fields as needed

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', ]

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['seat_number']

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )

class UserProfileForm(UserChangeForm):
    password = None  # Remove password field

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class RouteSearchForm(forms.Form):
    from_station = forms.ModelChoiceField(
        queryset=Station.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='From Station:'
    )
    to_station = forms.ModelChoiceField(
        queryset=Station.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='To Station:'
    )
    date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        label='Date of Travel:'
    )
    train = forms.ModelChoiceField(
        queryset=Train.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,
        label='Search by Train (Optional):'
    )

class FareCheckForm(forms.Form):
    from_station = forms.ModelChoiceField(
        queryset=Station.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    to_station = forms.ModelChoiceField(
        queryset=Station.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

class TicketBookingForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['seat_number']
        widgets = {
            'seat_number': forms.TextInput(attrs={'class': 'form-control'}),
        }

class OfferApplyForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = []
        # This can be extended if needed for offer application logic

class PaymentForm(forms.Form):
    card_number = forms.CharField(
        max_length=16,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '1234 5678 9012 3456'})
    )
    expiry_date = forms.CharField(
        max_length=5,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'MM/YY'})
    )
    cvv = forms.CharField(
        max_length=3,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'CVV'})
    )