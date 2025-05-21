from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
import core.views as core_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__reload__/', include('django_browser_reload.urls')),
    path('', include('core.urls')),
    path('connexion/', auth_views.LoginView.as_view(template_name='core/connexion.html'), name='login'),
    path('deconnexion/', auth_views.LogoutView.as_view(), name='logout'),
    path('inscription/', core_views.inscription, name='inscription'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)