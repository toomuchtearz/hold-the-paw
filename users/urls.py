from django.urls import path

from users.views import CreateUserView, ManageUserView, RequestPasswordReset, ResetPassword

app_name = "users"

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create"),
    path("me/", ManageUserView.as_view(), name="manage"),
    path("password-reset/", RequestPasswordReset.as_view(), name="password-reset"),
    path('password-reset-confirm/<str:token>/', ResetPassword.as_view(), name='password-reset-confirm')
]
