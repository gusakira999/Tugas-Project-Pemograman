from django.shortcuts import render, redirect, get_object_or_404
from .models import Game
from .forms import GameForm
from collections import OrderedDict

# Create your views here.
def home(request):
    return render(request, 'home.html')

def kontak(request):
    return render(request, 'connections.html')

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
                # Jika user tidak upload gambar, pakai gambar default dari referensi
                if not game.gambar and 'gambar' in referensi:
                    game.gambar.name = referensi['gambar']
            game.save()
            return redirect('game')
    else:
        form = GameForm()
    return render(request, 'tambah_game.html', {'form': form})

def connections(request):
    return render(request, 'connections.html')

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

def delete_game(request, pk):
    game = get_object_or_404(Game, pk=pk)
    if request.method == 'POST':
        game.delete()
        return redirect('game')
    return render(request, 'delete_game.html', {'game': game})

GAME_REFERENSI = OrderedDict(sorted({
    "Assassin's Creed": {
        "genre": "Action-Adventure, Stealth, Open World",
        "deskripsi": "Game open-world berlatar sejarah, stealth, dan parkour. Pemain menjadi Altair, assassin di era Perang Salib, menjalankan misi rahasia dan mengungkap konflik antara Assassin dan Templar.",
        "rating": 8.5,
        "gambar": "game_images/assassins_creed.jpg",
    },
    "Assassin's Creed Brotherhood": {
        "genre": "Action-Adventure, Stealth, Open World",
        "deskripsi": "Melanjutkan kisah Ezio di Roma, membangun Brotherhood dan melawan Ordo Templar. Fitur multiplayer pertama di seri ini.",
        "rating": 8.8,
        "gambar": "game_images/ac_brotherhood.jpg",
    },
    "Assassin's Creed II": {
        "genre": "Action-Adventure, Stealth, Open World",
        "deskripsi": "Petualangan Ezio Auditore di Italia Renaissance. Game ini memperkenalkan sistem ekonomi, senjata baru, dan cerita balas dendam yang mendalam di kota-kota seperti Firenze dan Venezia.",
        "rating": 9.0,
        "gambar": "game_images/assassins_creed_ii.jpg",
    },
    "Assassin's Creed III": {
        "genre": "Action-Adventure, Stealth, Open World",
        "deskripsi": "Berlatar Revolusi Amerika, main sebagai Connor, memperkenalkan pertempuran laut dan dunia terbuka yang luas.",
        "rating": 8.4,
        "gambar": "game_images/ac_III.jpg",
    },
    "Assassin's Creed IV: Black Flag": {
        "genre": "Action-Adventure, Stealth, Open World",
        "deskripsi": "Petualangan bajak laut bersama Edward Kenway di Karibia, gameplay kapal laut dan eksplorasi pulau.",
        "rating": 9.1,
        "gambar": "game_images/ac_black_flag.jpg",
    },
    "Assassin's Creed Origins": {
        "genre": "Action RPG, Open World",
        "deskripsi": "Kisah asal mula Brotherhood di Mesir kuno, sistem RPG dan dunia terbuka yang sangat luas.",
        "rating": 8.7,
        "gambar": "game_images/ac_origins.jpg",
    },
    "Assassin's Creed Revelations": {
        "genre": "Action-Adventure, Stealth, Opeen World",
        "deskripsi": "Ezio mencari rahasia Altair di Konstantinopel, memperkenalkan hookblade dan bomb crafting.",
        "rating": 8.6,
        "gambar": "game_images/ac_rev.jpg",
    },
    "Assassin's Creed Valhalla": {
        "genre": "Action RPG, Open World",
        "deskripsi": "Bermain sebagai Eivor, seorang Viking yang menjelajah Inggris abad ke-9, membangun permukiman, dan terlibat dalam pertempuran epik serta politik kerajaan.",
        "rating": 8.2,
        "gambar": "game_images/assassins_creed_valhalla.jpg",
    },
    "Battlefield 1": {
        "genre": "FPS, Action, World War",
        "deskripsi": "FPS berlatar Perang Dunia I, menampilkan pertempuran besar, kendaraan, senjata klasik, dan mode multiplayer epik dengan map dinamis dan cerita perang yang emosional.",
        "rating": 8.6,
        "gambar": "game_images/battlefield_1.jpg",
    },
    "Call of Duty: Advanced Warfare": {
        "genre": "FPS, Action, Sci-Fi",
        "deskripsi": "Teknologi futuristik, exoskeleton, dan gameplay cepat dengan grafis next-gen.",
        "rating": 8.0,
        "gambar": "game_images/cod_advanced.jpg",
    },
    "Call of Duty: Black Ops 2": {
        "genre": "FPS, Action",
        "deskripsi": "Sekuel Black Ops dengan latar masa depan dan masa lalu, memperkenalkan sistem pilihan cerita, mode zombie yang lebih kompleks, dan multiplayer inovatif.",
        "rating": 8.9,
        "gambar": "game_images/call_of_duty_black_ops_2.jpg",
    },
    "Call of Duty: Black Ops Cold War": {
        "genre": "FPS, Action",
        "deskripsi": "Kembali ke era Perang Dingin dengan campaign penuh intrik, mode multiplayer, dan zombie yang semakin seru. Pemain terlibat dalam operasi rahasia dan konspirasi global.",
        "rating": 8.5,
        "gambar": "game_images/call_of_duty_black_ops_cold_war.jpg",
    },
    "Call of Duty: Ghosts": {
        "genre": "FPS, Action",
        "deskripsi": "Konflik global baru dengan pasukan elit Ghosts, campaign sinematik dan multiplayer inovatif.",
        "rating": 7.8,
        "gambar": "game_images/cod_ghosts.jpg",
    },
    "Call of Duty: Infinite Warfare": {
        "genre": "FPS, Action, Sci-Fi",
        "deskripsi": "Pertempuran luar angkasa, campaign sci-fi, dan mode multiplayer serta zombie.",
        "rating": 7.5,
        "gambar": "game_images/cod_infinite.jpg",
    },
    "Call of Duty: Modern Warfare": {
        "genre": "FPS, Action",
        "deskripsi": "FPS dengan campaign intens, karakter ikonik seperti Captain Price, dan mode multiplayer modern yang sangat kompetitif. Fokus pada konflik militer kontemporer dan operasi rahasia.",
        "rating": 8.8,
        "gambar": "game_images/call_of_duty_modern_warfare.jpg",
    },
    "Call of Duty: World at War": {
        "genre": "FPS, Action, World War",
        "deskripsi": "Kembali ke Perang Dunia II, memperkenalkan mode zombie dan pertempuran brutal di front Pasifik dan Eropa.",
        "rating": 8.1,
        "gambar": "game_images/cod_wow.jpg",
    },
    "Far Cry 3": {
        "genre": "FPS, Open World",
        "deskripsi": "Petualangan di pulau tropis melawan bajak laut gila Vaas, gameplay open world dan crafting.",
        "rating": 9.0,
        "gambar": "game_images/far_cry_3.jpg",
    },
    "Far Cry 4": {
        "genre": "FPS, Open World",
        "deskripsi": "Berlatar Himalaya, pemain melawan diktator Pagan Min dengan gameplay open world dan co-op.",
        "rating": 8.5,
        "gambar": "game_images/far_cry_4.jpg",
    },
    "Far Cry 5": {
        "genre": "FPS, Open World",
        "deskripsi": "Melawan sekte fanatik di Montana, Amerika, dengan dunia terbuka dan sistem companion.",
        "rating": 8.3,
        "gambar": "game_images/far_cry_5.jpg",
    },
    "Resident Evil 2 Remake": {
        "genre": "Survival Horror",
        "deskripsi": "Remake dari RE2 klasik, dengan grafis modern, gameplay survival horror, dan cerita Leon & Claire bertahan hidup di Raccoon City dari serangan zombie dan monster.",
        "rating": 9.0,
        "gambar": "game_images/resident_evil_2_remake.jpg",
    },
    "Resident Evil 4 Remake": {
        "genre": "Survival Horror, Action",
        "deskripsi": "Remake dari Resident Evil 4 klasik dengan grafis modern, gameplay yang diperbarui, dan atmosfer horor yang lebih intens. Leon S. Kennedy kembali menyelamatkan putri presiden di desa Spanyol.",
        "rating": 9.6,
        "gambar": "game_images/re4r.jpg",
    },
    "Resident Evil 4": {
        "genre": "Survival Horror, Action",
        "deskripsi": "Leon S. Kennedy menyelamatkan putri presiden dari sekte misterius di desa Spanyol. Gameplay third-person action-horror revolusioner dengan musuh Ganados dan boss menegangkan.",
        "rating": 9.5,
        "gambar": "game_images/resident_evil_4.jpg",
    },
    "Resident Evil Village": {
        "genre": "Survival Horror, FPS",
        "deskripsi": "Petualangan Ethan Winters di desa misterius penuh monster, Lady Dimitrescu, dan atmosfer horor Eropa Timur yang menegangkan. Grafis dan cerita sangat memukau.",
        "rating": 8.9,
        "gambar": "game_images/resident_evil_village.jpg",
    },
    "Sniper Elite": {
        "genre": "Tactical Shooter",
        "deskripsi": "Game sniper berlatar Perang Dunia II, menonjolkan mekanik slow-motion X-Ray kill cam dan stealth.",
        "rating": 8.0,
        "gambar": "game_images/sniper_elite.jpg",
    },
    "Sniper Elite 3": {
        "genre": "Tactical Shooter, Stealth, Action",
        "deskripsi": "Petualangan di Afrika Utara saat Perang Dunia II, gameplay open-ended dengan banyak pilihan taktik dan X-Ray kill cam.",
        "rating": 8.2,
        "gambar": "game_images/sniper_elite_3.jpg",
    },
    "Sniper Elite 4": {
        "genre": "Tactical Shooter, Stealth, Action",
        "deskripsi": "Berlatar Italia, menawarkan map luas, stealth, dan X-Ray kill cam yang lebih detail.",
        "rating": 8.4,
        "gambar": "game_images/sniper_elite_4.jpg",
    },
    "Devil May Cry 5": {
        "genre": "Action, Hack and Slash",
        "deskripsi": "Aksi stylish dengan tiga karakter utama yaitu Dante, Nero, dan V.Pertarungan cepat, dan cerita epik melawan iblis.",
        "rating": 9.0,
        "gambar": "game_images/dmc5.jpg",
    },
    "Dying Light": {
        "genre": "Action, Survival Horror, Open World, FPS, Parkour",
        "deskripsi": "Game survival horror open world dengan parkour dan pertarungan melawan zombie di kota Harran.",
        "rating": 8.5,
        "gambar": "game_images/dl1.jpg",
    },
    "Forza Horizon 4": {
        "genre": "Racing, Open World",
        "deskripsi": "Game balap open world di Inggris dengan perubahan musim dinamis dan ratusan mobil.",
        "rating": 9.2,
        "gambar": "game_images/fh4.jpg",
    },
    "Need for Speed Heat": {
        "genre": "Racing, Open World",
        "deskripsi": "Game balap jalanan dengan siang-malam dinamis di kota Palm City, kustomisasi mobil, dan aksi kejar-kejaran polisi.",
        "rating": 8.0,
        "gambar": "game_images/nfsheat.jpg",
    },
    "Zombie Army Trilogy": {
        "genre": "Tactical Shooter, Survival Horror, Action",
        "deskripsi": "Spin-off dari Sniper Elite, menghadirkan pertempuran melawan pasukan zombie Nazi dengan mode co-op hingga 4 pemain dan atmosfer horor yang menegangkan.",
        "rating": 8.0,
        "gambar": "game_images/zat.jpg",
    },
}.items()))

GENRE_LIST = [
    "Action",
    "Action-Adventure",
    "Action RPG",
    "Hack and Slash",
    "Stealth",
    "Open World",
    "FPS",
    "Survival Horror",
    "Tactical Shooter",
    "Racing",
    "World War",
    "Sci-Fi",
    "Parkour"
]