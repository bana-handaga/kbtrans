# catalog/models.py

from django.db import models
from django.contrib.auth.models import User # Untuk pemesan (Pelanggan)
from django.utils import timezone
from datetime import date


class Car(models.Model):
    """Model untuk menyimpan detail mobil."""
    
    TRANSMISSION_CHOICES = [
        ('A', 'Otomatis'),
        ('M', 'Manual'),
    ]

    STATUS_CHOICES = [
        ('A', 'Available (Tersedia)'),
        ('R', 'Rented (Disewa)'),
        ('M', 'Maintenance (Perawatan)'),
    ]
    
    make = models.CharField(max_length=100, verbose_name="Merek")
    model = models.CharField(max_length=100, verbose_name="Model")
    year = models.IntegerField(verbose_name="Tahun")
    daily_rate = models.DecimalField(max_digits=10, decimal_places=0, default=500000, verbose_name="Tarif sewa 24jam (Rp)")
    
    halfday_rate = models.DecimalField(max_digits=10, decimal_places=0, default=250000, verbose_name="Tarif sewa 12jam (Rp)")
    denda_waktu = models.DecimalField(max_digits=10, decimal_places=0, default=75000, verbose_name="Denda Waktu (Rp)")
    denda_bbm = models.DecimalField(max_digits=10, decimal_places=0, default=50000, verbose_name="Denda BBM (Rp)")
    
    transmission = models.CharField(max_length=1, choices=TRANSMISSION_CHOICES, default='A', verbose_name="Transmisi")
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='A', verbose_name="Status")
    description = models.TextField(blank=True, verbose_name="Deskripsi")
    
    # TAMBAHKAN KOLOM GAMBAR INI:
    image = models.ImageField(upload_to='car_images/', blank=True, null=True, verbose_name="Gambar Mobil")
    
    
    

    def __str__(self):
        return f"{self.make} {self.model} ({self.year})"
    
    class Meta:
        verbose_name = "Mobil"
        verbose_name_plural = "Daftar Mobil"

# --- Model Booking ---

class Booking(models.Model):
    """Model untuk menyimpan informasi pemesanan."""

    STATUS_CHOICES = [
        ('P', 'Pending'),
        ('C', 'Confirmed'),
        ('X', 'Cancelled'),
        ('D', 'Completed'),
    ]

    # Relasi
    car = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True, verbose_name="Mobil yang Disewa")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Penyewa") # Menggunakan model User bawaan Django
    
    # Detail Waktu & Lokasi
    start_date = models.DateField(verbose_name="Tanggal Mulai Sewa", default=timezone.now)
    end_date = models.DateField(verbose_name="Tanggal Selesai Sewa", default=timezone.now)
    pickup_location = models.CharField(max_length=255, verbose_name="Lokasi Penjemputan", default="KembarTrans")
    return_location = models.CharField(max_length=255, verbose_name="Lokasi Pengembalian", default="KembarTrans")
    
    # Finansial & Status
    total_days = models.IntegerField(null=True, blank=True, verbose_name="Jumlah Hari")
    total_price = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True, verbose_name="Total Biaya (Rp)")
    booking_status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P', verbose_name="Status Pemesanan")
    booked_on = models.DateTimeField(auto_now_add=True, verbose_name="Dipesan pada")

    class Meta:
        verbose_name = "Pemesanan"
        verbose_name_plural = "Daftar Pemesanan"
        ordering = ['-booked_on'] # Urutkan dari yang terbaru

    def __str__(self):
        return f"Pemesanan #{self.id} | {self.car.make} {self.car.model}"

    def clean(self):
        """Validasi data sebelum disimpan ke database."""
        # 1. Validasi Tanggal
        if self.start_date < date.today():
            raise ValidationError('Tanggal mulai sewa tidak boleh di masa lalu.')
        if self.end_date < self.start_date:
            raise ValidationError('Tanggal selesai sewa harus setelah tanggal mulai sewa.')

    def save(self, *args, **kwargs):
        """Timpa metode save untuk menghitung harga otomatis."""
        # 1. Hitung jumlah hari
        duration = self.end_date - self.start_date
        self.total_days = duration.days + 1 # +1 untuk memasukkan hari terakhir
        
        # 2. Hitung total harga
        if self.car:
            self.total_price = self.total_days * self.car.daily_rate
        
        # Panggil metode save asli
        super().save(*args, **kwargs)