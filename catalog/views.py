# catalog/views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import Car, Booking
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import BookingForm, RegisterForm # Pastikan RegisterForm sudah diimport

# from datetime import date # Akan digunakan untuk perhitungan yang lebih kompleks

def car_home(request):
    """Menampilkan daftar mobil yang tersedia (status 'A')."""
    available_cars = Car.objects.filter(status='A').order_by('daily_rate')
    context = {
        'cars': available_cars,
        'title': 'Daftar Mobil Tersedia'
    }
    return render(request, 'catalog/car_home.html', context)


def car_list(request):
    """Menampilkan daftar mobil yang tersedia (status 'A')."""
    available_cars = Car.objects.filter(status='A').order_by('daily_rate')
    context = {
        'cars': available_cars,
        'title': 'Daftar Mobil Tersedia'
    }
    return render(request, 'catalog/car_list.html', context)

def car_detail(request, car_id):
    """Menampilkan detail satu mobil."""
    car = get_object_or_404(Car, pk=car_id)
    context = {
        'car': car,
        'title': f'Detail {car.make} {car.model}'
    }
    return render(request, 'catalog/car_detail.html', context)

@login_required
def book_car(request, car_id):
    """
    Menangani proses pemesanan mobil.
    """
    car = get_object_or_404(Car, pk=car_id)
    
    # Cek ketersediaan mobil sebelum melanjutkan
    if car.status != 'A': # 'A' = Available
        messages.error(request, 'Mobil ini sedang tidak tersedia untuk disewa.')
        return redirect('car_detail', car_id=car.id)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            try:
                # 1. Simpan objek Booking, tapi jangan di-commit ke DB dulu
                booking = form.save(commit=False)
                
                # 2. Tambahkan data yang hilang (Foreign Keys)
                booking.car = car
                booking.user = request.user
                
                # Metode clean() dan save() di model Booking akan otomatis 
                # menghitung total_days dan total_price, serta validasi tanggal.
                booking.full_clean() # Panggil validasi model (clean)
                booking.save() # Simpan ke database

                # 3. Update Status Mobil (Optional, untuk simulasi ketersediaan)
                car.status = 'R' # 'R' = Rented/Disewa
                car.save()

                messages.success(request, f'Pemesanan untuk {car.make} {car.model} berhasil dibuat! Total biaya: Rp{booking.total_price:,.0f}')
                return redirect('booking_confirmation', booking_id=booking.id)

            except Exception as e:
                # Tangani error validasi (misalnya tanggal mundur) atau error lain
                messages.error(request, f'Pemesanan gagal: {e}')
                return render(request, 'catalog/booking_form.html', {'form': form, 'car': car})

    else:
        # Permintaan GET: Tampilkan formulir kosong
        form = BookingForm()
        
    context = {
        'form': form,
        'car': car,
        'title': f'Pesan {car.make} {car.model}'
    }
    return render(request, 'catalog/booking_form.html', context)


def booking_confirmation(request, booking_id):
    """Menampilkan detail konfirmasi pemesanan."""
    booking = get_object_or_404(Booking, pk=booking_id)
    # Anda bisa menambahkan pengecekan user_id di sini
    
    context = {
        'booking': booking,
        'title': 'Konfirmasi Pemesanan'
    }
    return render(request, 'catalog/confirmation.html', context)
    
def register(request):
    """Menangani proses registrasi pengguna baru."""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Setelah berhasil daftar, arahkan pengguna ke halaman login
            messages.success(request, 'Akun berhasil dibuat! Silakan Login.')
            return redirect('login') 
        else:
            # Jika ada error (misalnya username sudah ada)
            messages.error(request, 'Registrasi gagal. Cek kembali data Anda.')
    else:
        # Permintaan GET: Tampilkan formulir kosong
        form = RegisterForm()
        
    context = {
        'form': form,
        'title': 'Registrasi Akun Baru'
    }
    return render(request, 'registration/register.html', context)
    
    