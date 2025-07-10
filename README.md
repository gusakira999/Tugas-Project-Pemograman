# Gamepedia Pribadi Django

## Deskripsi Aplikasi

Gamepedia Pribadi adalah aplikasi web berbasis Django yang berfungsi sebagai katalog pribadi game yang pernah dimainkan. Pengguna dapat menambah, melihat, mengedit, dan menghapus data game, lengkap dengan deskripsi, genre, rating, dan gambar. Aplikasi ini juga menyediakan fitur filter berdasarkan genre dan halaman kontak.

### Fitur Utama

- CRUD Game: Tambah, lihat, edit, dan hapus data game.
- Filter Genre: Menampilkan game berdasarkan genre tertentu.
- Upload Gambar: Setiap game dapat memiliki gambar sampul.
- Halaman Kontak: Menampilkan informasi kontak pemilik web.
- Tampilan Responsive: Menggunakan Bootstrap untuk tampilan yang menarik di berbagai perangkat.

---

## Panduan Instalasi & Menjalankan Aplikasi

1. **Clone Repository**
    ```
    git clone https://github.com/username/gamepedia-django.git
    cd gamepedia-django
    ```

2. **Buat Virtual Environment (Opsional tapi disarankan)**
    ```
    python -m venv venv
    venv\Scripts\activate
    ```

3. **Install Dependencies**
    ```
    pip install -r requirements.txt
    ```

4. **Migrasi Database**
    ```
    python manage.py migrate
    ```

5. **Jalankan Server**
    ```
    python manage.py runserver
    ```

6. **Akses di Browser**
    Buka [http://localhost:8000](http://localhost:8000) di browser.

---

## Struktur Folder

```
projectweb/
│
├── app/                  # Django app utama (views, models, forms, dll)
│   ├── migrations/
│   ├── templates/        # HTML templates (home, game, edit, delete, dsb)
│   ├── static/           # File statis (CSS, JS, gambar ikon)
│   ├── models.py         # Model Game
│   ├── views.py          # Logika tampilan (CRUD, filter, dsb)
│   ├── forms.py          # Form Django untuk tambah/edit game
│   └── ...
│
├── media/                # File upload gambar game
│
├── projectweb/           # Folder project Django (settings, urls, wsgi)
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
├── db.sqlite3            # Database SQLite (default)
├── manage.py             # Django management script
└── requirements.txt      # Daftar dependencies Python
```

---

## Penjelasan Logika Algoritma & Contoh Kode

### Model Game

```python
from django.db import models

class Game(models.Model):
    nama = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    deskripsi = models.TextField()
    rating = models.FloatField()
    gambar = models.ImageField(upload_to='game_images/', blank=True, null=True)

    def __str__(self):
        return self.nama
```

### Form Game

```python
from django import forms
from .models import Game

class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['nama', 'genre', 'deskripsi', 'rating', 'gambar']
```

### View CRUD

**Create (Tambah Game):**
```python
def tambah_game(request):
    if request.method == 'POST':
        form = GameForm(request.POST, request.FILES)
        if form.is_valid():
            game = form.save(commit=False)
            referensi = GAME_REFERENSI.get(game.nama)
            if referensi:
                game.genre = referensi['genre']
                game.deskripsi = referensi['deskripsi']
                game.rating = referensi['rating']
                if not game.gambar and 'gambar' in referensi:
                    game.gambar.name = referensi['gambar']
            game.save()
            return redirect('game')
    else:
        form = GameForm()
    return render(request, 'tambah_game.html', {'form': form})
```

**Read (Daftar Game):**
```python
def game(request):
    genre = request.GET.get('genre')
    if genre and genre != 'all':
        games = Game.objects.filter(genre__icontains=genre).order_by('nama')
    else:
        games = Game.objects.all().order_by('nama')
    return render(request, 'game.html', {
        'games': games,
        'genres': GENRE_LIST,
        'selected_genre': genre
    })
```

**Update (Edit Game):**
```python
def edit_game(request, pk):
    game = get_object_or_404(Game, pk=pk)
    if request.method == 'POST':
        form = GameForm(request.POST, request.FILES, instance=game)
        if form.is_valid():
            form.save()
            return redirect('game')
    else:
        form = GameForm(instance=game)
    return render(request, 'edit_game.html', {'form': form, 'game': game})
```

**Delete (Hapus Game):**
```python
def delete_game(request, pk):
    game = get_object_or_404(Game, pk=pk)
    if request.method == 'POST':
        game.delete()
        return redirect('game')
    return render(request, 'delete_game.html', {'game': game})
```

---

### Filter Genre

Pengguna dapat memilih genre tertentu untuk menampilkan hanya game dengan genre tersebut. Filtering dilakukan dengan query ke database menggunakan:
```python
games = Game.objects.filter(genre__icontains=genre)
```

---

### Upload & Tampilkan Gambar

**Template (tambah/edit game):**
```html
<form method="post" enctype="multipart/form-data">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Simpan</button>
</form>
```
`enctype="multipart/form-data"` wajib agar upload file bisa berjalan.

**Template (tampilkan gambar):**
```html
{% if game.gambar %}
    <img src="{{ game.gambar.url }}" alt="{{ game.nama }}" width="200">
{% endif %}
```
Kode ini menampilkan gambar game jika ada.

---

### Halaman Kontak

**View:**
```python
def kontak(request):
    return render(request, 'connections.html')
```
**Template:**
```html
<ul>
    <li>Email: hidayatachmad316@gmail.com</li>
    <li>Steam: steamcommunity.com/id/Yatte/</li>
    <li>Instagram: @yatt.zip</li>
</ul>
```

---

### Tampilan Navbar & Logo Platform Game

Navbar menampilkan menu utama dan logo platform game (Steam, Xbox, PlayStation) agar tampilan lebih menarik dan sesuai tema gaming.

**Navbar di `base.html`:**
```html
<nav class="navbar navbar-expand-lg navbar-light bg-white shadow-sm mb-4">
  <div class="container">
    <a class="navbar-brand" href="{% url 'home' %}">Gamepedia</a>
    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav me-auto mb-2 mb-lg-0">
        <li class="nav-item">
            <a class="nav-link" href="{% url 'game' %}"><i class="bi bi-controller"></i> Game</a>
        </li>
        <li class="nav-item">
            <a class="nav-link" href="{% url 'kontak' %}"><i class="bi bi-person-lines-fill"></i> Connections</a>
        </li>
      </ul>
      <div class="d-flex gap-3">
        <i class="bi bi-steam fs-3" style="color:#171a21"></i>
        <i class="bi bi-xbox fs-3" style="color:#107c10"></i>
        <i class="bi bi-playstation fs-3" style="color:#003087"></i>
      </div>
    </div>
  </div>
</nav>
```
Bagian `<div class="d-flex gap-3">...</div>` menampilkan logo platform game menggunakan Bootstrap Icons.

---

## Penutup

Aplikasi ini dibuat untuk keperluan tugas kuliah dan dapat dikembangkan lebih lanjut sesuai kebutuhan.  
Jika ingin menambah genre atau game baru, cukup edit list di `app/views.py` dan tambahkan gambar di folder `media/game_images`.

---

**Link repository GitHub:**  
_Silakan isi link repository kamu di sini setelah upload
