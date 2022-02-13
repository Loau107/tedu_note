from django.urls import path
from note import views

urlpatterns = [
    path('list/', views.list_note),
    path('add/', views.add_note),
    path('update/', views.update_note),
    path('delete/', views.delete_note),
    path('list_delete/', views.list_delete_note),
    path('retrieve/', views.retrieve_note),
    path('view/', views.view_note)
]