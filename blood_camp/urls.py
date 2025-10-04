from django.urls import path
from . import views

app_name = "blood_camp"

urlpatterns = [
    # Dashboard (root of blood_camp/)
    path("", views.dashboard, name="dashboard"),

    # List all camps
    path("camps/", views.camp_list, name="camp_list"),

    # Create new camp
    path("new/", views.create_camp, name="create_camp"),

    # Edit a camp
    path("edit/<int:pk>/", views.edit_camp, name="edit_camp"),

    # Delete a camp
    path("delete/<int:pk>/", views.delete_camp, name="delete_camp"),

    # Optional: camp detail view (if you want)
    #path("<int:pk>/", views.camp_detail, name="camp_detail"),
]
