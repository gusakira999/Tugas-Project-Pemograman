from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),  # untuk halaman utama
    path('kontak', views.kontak, name='kontak'),
    path('game', views.game, name='game'),  # untuk halaman game
    path('game/tambah', views.tambah_game, name='tambah_game'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('game/edit/<int:pk>/', views.edit_game, name='edit_game'),
    path('game/delete/<int:pk>/', views.delete_game, name='delete_game'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)