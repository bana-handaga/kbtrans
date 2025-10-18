# catalog/admin.py

from django.contrib import admin
from .models import Car, Booking

# Daftarkan model Car
@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('make', 'model', 'daily_rate', 'status')
    list_filter = ('status', 'transmission')

# --- Pendaftaran Model Booking ---
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """
    Mengatur tampilan model Booking di halaman admin.
    """
    
    list_display_links = ('user',)
    
    # Kolom yang akan ditampilkan dalam daftar tabel Booking
    list_display = (
        'id', 
        'user', 
        'car', 
        'start_date', 
        'end_date', 
        'total_price',
        'booking_status',
        'booked_on',
    )
    
    # Filter samping yang bisa digunakan untuk menyaring data
    list_filter = (
        'booking_status', 
        'start_date', 
        'car__make',  # Filter berdasarkan merek mobil
        'booked_on',
    )
    
    # Field yang dapat dicari
    search_fields = (
        'user__username',  # Memungkinkan pencarian berdasarkan username
        'car__make',
        'car__model',
    )
    
    # Field yang hanya bisa dibaca (agar admin tidak mengubah nilai yang dihitung otomatis)
    readonly_fields = (
        'total_price', 
        'total_days', 
        'booked_on',
    )

    # Mengelompokkan field dalam form edit/tambah booking
    fieldsets = (
        (None, {
            'fields': ('car', 'user', 'booking_status')
        }),
        ('Detail Sewa', {
            'fields': ('start_date', 'end_date', 'pickup_location', 'return_location')
        }),
        ('Rincian Biaya (Otomatis)', {
            'fields': ('total_days', 'total_price', 'booked_on'),
            'classes': ('collapse',), # Sembunyikan bagian ini secara default
        }),
    )