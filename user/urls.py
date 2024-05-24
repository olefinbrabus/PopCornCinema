from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from user.views import (UserCreateView, UserDetailView, UserUpdateView, order_pdf_download_view,
                        UserDeleteView, UserUpdatePasswordView, OrderListUserView)

app_name = "user"

urlpatterns = [
    path("<int:pk>/", UserDetailView.as_view(), name="user-account-detail"),
    path("register/", UserCreateView.as_view(), name="register"),
    path("<int:pk>/update/", UserUpdateView.as_view(), name="update"),
    path("<int:pk>/update_password/", UserUpdatePasswordView.as_view(), name="update-password"),
    path("<int:pk>/delete/", UserDeleteView.as_view(), name="delete"),
    path("<int:pk>/orders/", OrderListUserView.as_view(), name="order"),
    path("pdf/<int:pk>", order_pdf_download_view, name="pdf"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
