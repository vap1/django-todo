from django.test import TestCase
from datetime import datetime
from django.urls import reverse
from .models import Todo


class TodoTests(TestCase):
    def test_deadline_not_in_past(self):
        todo = Todo.objects.create(title='Test Todo', deadline=datetime.now())
        self.assertGreaterEqual(todo.deadline, datetime.now())

    def test_add_view(self):
        response = self.client.post(reverse('todos:add'), {'title': 'Test Todo', 'deadline': datetime.now()})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Todo.objects.count(), 1)

    def test_update_view(self):
        todo = Todo.objects.create(title='Test Todo')
        response = self.client.post(reverse('todos:update', args=[todo.id]), {'isCompleted': 'on', 'deadline': datetime.now()})
        self.assertEqual(response.status_code, 302)
        updated_todo = Todo.objects.get(id=todo.id)
        self.assertTrue(updated_todo.isCompleted)
        self.assertGreaterEqual(updated_todo.deadline, datetime.now())
