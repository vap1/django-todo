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
        return Todo.objects.filter(user=self.request.user).order_by('-created_at').values('id','title', 'deadline')


def add(request):
    title = request.POST['title']
    deadline = request.POST['deadline']
    print(deadline)
    deadline_date = datetime.datetime.strptime(deadline, '%Y-%m-%dT%H:%M')
    deadline_date = timezone.make_aware(deadline_date, timezone.get_default_timezone())
    if deadline_date < timezone.now():
        return redirect('todos:index')
    Todo.objects.create(title=title, deadline=deadline_date, user=request.user)

    return redirect('todos:index')


def delete(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id, user=request.user)
    todo.delete()

    return redirect('todos:index')


def update(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id, user=request.user)
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
