from django.urls import path
from notes import views
from .views import NoteListCreateView, NoteRetrieveUpdateDeleteView

urlpatterns = [
    path('notes/', views.NoteListCreateView.as_view(), name='note-list-create'),
    path('notes/<int:pk>/', views.NoteRetrieveUpdateDeleteView.as_view(), name='note-detail-update-delete')    
]