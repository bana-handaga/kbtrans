# catalog/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Booking

class BookingForm(forms.ModelForm):
    """
    Formulir yang terhubung langsung dengan model Booking.
    """
    
    # Tambahkan widget kustom untuk input tanggal agar lebih user-friendly
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Tanggal Mulai Sewa'
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Tanggal Selesai Sewa'
    )

    class Meta:
        model = Booking
        # Field yang akan diinput oleh pengguna
        fields = [
            'start_date', 
            'end_date', 
            'pickup_location', 
            'return_location'
        ]
        # Label dan pesan kustom untuk field
        labels = {
            'pickup_location': 'Lokasi Penjemputan',
            'return_location': 'Lokasi Pengembalian',
        }
        # Kita tidak perlu memasukkan 'car', 'user', dan 'status' 
        # karena akan diisi otomatis di view.
        
        
class RegisterForm(UserCreationForm):
    """Formulir registrasi sederhana berdasarkan UserCreationForm bawaan Django."""
    
    class Meta:
        model = User
        # Hanya meminta username dan password (password dua kali)
        fields = ("username", "email")        