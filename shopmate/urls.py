from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),

    # ✅ Auth reset views
    path('reset-password/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reset-password-sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset-complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

# ✅ Serve user files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)