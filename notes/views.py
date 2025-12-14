from .models import Note
from.serializers import NoteSerializer
from .permissions import IsOwner
from rest_framework import generics, permissions, filters
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend


# List all notes & create note

class NoteListCreateView(generics.ListCreateAPIView):
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['title']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at, updated_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)
    
    def post_create(self, serializer):
        serializer.save(user=self.request.user)
        

class NoteRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    
    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)   
    