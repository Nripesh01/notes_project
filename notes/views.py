from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from notes.models import Note
from notes.forms import NoteForm
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator



def home_view(request):
    if request.user.is_authenticated:
        return redirect('notes')  # If logged in, go to notes
    return render(request, 'home.html')


# Register view
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# Login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('notes')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Logout view
def logout_view(request):
    logout(request)
    return redirect('login')

# Notes list view (main page)
@login_required
def notes_list_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    notes = Note.objects.filter(user=request.user)

    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            return redirect('notes')  # after saving, refresh the page
    else:
        form = NoteForm()
        
    query = request.GET.get('q')
    notes = Note.objects.filter(user=request.user).order_by('-created_at')
    if query:
        notes = notes.filter(Q(title__icontains=query)| Q(content__icontains=query))
    
    paginator = Paginator(notes, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    
    return render(request, 'notes_list.html', {'notes': notes, 'form': form, 'page_obj': page_obj})


@login_required
def create_note(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
          note = form.save(commit=False)
          note.user = request.user
          note.save()
          messages.success(request, 'Note created successfully')
          return redirect('notes')
        else:
            messages.error(request, "There was an erro creating the note")
    else:
        form = NoteForm()
    return render(request, 'create_note.html', {'form': form})



@login_required
def update_note(request, note_id):
    notes = Note.objects.get(id=note_id, user=request.user)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=notes)
        if form.is_valid():
            form.save()
            messages.success(request, "Note updates successfully")
            return redirect('notes')
    else:
        form = NoteForm(instance=notes)
    return render(request, 'update_note.html', {'form':form})


@login_required
def read_note(request):
    notes = Note.objects.filter(user=request.user)
    return render(request, 'read_note.html', {'notes': notes})
    


@login_required
def delete_note(request, note_id):
    notes = get_object_or_404(Note, id=note_id, user=request.user)
    if request.method == 'POST':
        notes.delete()
        messages.success(request, "Note deleted successfully")
        return redirect('notes')
    return render(request, 'delete_note.html', {'notes': notes})



def note_detail(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    return render(request, 'note_detail.html', {'note': note})