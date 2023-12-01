from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from .models import Todo
from django.http import HttpResponseRedirect
from django.utils import timezone
import datetime

class IndexView(generic.ListView):
    template_name = 'todos/index.html'
    context_object_name = 'todo_list'

    def get_queryset(self):
        return Todo.objects.order_by('-created_at')


def add(request):
    title = request.POST['title']
    deadline = request.POST['deadline']
    try:
        deadline_date = datetime.datetime.strptime(deadline, '%Y-%m-%d')
    except ValueError:
        return redirect('todos:index')
    if deadline_date < timezone.now():
        return redirect('todos:index')
    Todo.objects.create(title=title, deadline=deadline_date)

    return redirect('todos:index')

def delete(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id)
    todo.delete()

    return redirect('todos:index')

def update(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id)
    isCompleted = request.POST.get('isCompleted', False)
    if isCompleted == 'on':
        isCompleted = True
    todo.isCompleted = isCompleted
    deadline = request.POST['deadline']
    try:
        deadline_date = datetime.datetime.strptime(deadline, '%Y-%m-%d')
    except ValueError:
        return redirect('todos:index')
    if deadline_date < timezone.now():
        return redirect('todos:index')
    todo.deadline = deadline_date

    todo.save()
    return redirect('todos:index')