from django.urls import path
from notes import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('note/', views.notes_list_view, name='notes'),
    path('read/', views.read_note, name='read_note'),
    path('create/', views.create_note, name='create_note'),
    path('delete/<int:note_id>', views.delete_note, name='delete_note'),
    path('update/<int:note_id>', views.update_note, name='update_note'),
    path('notes/<int:pk>/', views.note_detail, name='note_detail'),
]

