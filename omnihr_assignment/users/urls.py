from django.urls import path

from omnihr_assignment.users.views import (
    user_detail_view,
    user_redirect_view,
    user_update_view,
)
from omnihr_assignment.users.api.views import MyTokenObtainPairView

app_name = "users"
urlpatterns = [
    path('login/', MyTokenObtainPairView.as_view()),
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<int:pk>/", view=user_detail_view, name="detail"),
]
