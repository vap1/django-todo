from django.test import TestCase
from datetime import datetime
from django.urls import reverse
from .models import Todo
from django.contrib.auth.models import User

class TodoTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_login(self.user)

    def test_deadline_not_in_past(self):
        todo = Todo.objects.create(title='Test Todo', deadline=datetime.now(), user=self.user)
        self.assertGreaterEqual(todo.deadline, datetime.now())

    def test_add_view(self):
        response = self.client.post(reverse('todos:add'), {'title': 'Test Todo', 'deadline': datetime.now()}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Todo.objects.count(), 1)

    def test_update_view(self):
        todo = Todo.objects.create(title='Test Todo', user=self.user)
        response = self.client.post(reverse('todos:update', args=[todo.id]), {'isCompleted': 'on', 'deadline': datetime.now()}, follow=True)
        self.assertEqual(response.status_code, 200)
        updated_todo = Todo.objects.get(id=todo.id)
        self.assertTrue(updated_todo.isCompleted)
        self.assertGreaterEqual(updated_todo.deadline, datetime.now())

    def test_index_view(self):
        response = self.client.get(reverse('todos:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Todo List')
        self.assertQuerysetEqual(response.context['todo_list'], Todo.objects.filter(user=self.user), transform=lambda x: x)
        self.assertContains(response, 'deadline')
