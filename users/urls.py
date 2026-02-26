from django.urls import path

from users.views import CreateUserView, ManageUserView, RequestPasswordReset, ResetPassword, ChangePasswordView, CreateShelterView

app_name = "users"

urlpatterns = [
    path("register/personal/", CreateUserView.as_view(), name="create-personal"),
    path("register/shelter/", CreateShelterView.as_view(), name="create-shelter"),
    path("me/", ManageUserView.as_view(), name="manage"),
    path("password-reset/", RequestPasswordReset.as_view(), name="password-reset"),
    path("password-change/", ChangePasswordView.as_view(), name="password-change"),
    path('password-reset-confirm/<str:token>/', ResetPassword.as_view(), name='password-reset-confirm'),
]
