from django.test import TestCase
from datetime import datetime
from django.urls import reverse
from .models import Todo, CustomUser


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

    def test_index_view(self):
        response = self.client.get(reverse('todos:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Todo List')
        self.assertQuerysetEqual(response.context['todo_list'], Todo.objects.all(), transform=lambda x: x)
        self.assertContains(response, 'deadline')

    def test_register_view(self):
        response = self.client.post(reverse('todos:register'), {'email': 'test@example.com', 'phone_number': '1234567890', 'password': 'test123', 'date_of_birth': '2000-01-01'})
        self.assertEqual(response.status_code, 200)
        self.assertRegex(response.content.decode(), r'^[a-zA-Z0-9]{10}$')
        self.assertEqual(CustomUser.objects.count(), 1)

    def test_register_view_invalid_data(self):
        response = self.client.post(reverse('todos:register'), {'email': 'test@example.com', 'phone_number': '1234567890', 'password': 'test123'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required.')
        self.assertEqual(CustomUser.objects.count(), 0)

    def test_register_view_unique_userId(self):
        response1 = self.client.post(reverse('todos:register'), {'email': 'test1@example.com', 'phone_number': '1234567890', 'password': 'test123', 'date_of_birth': '2000-01-01'})
        response2 = self.client.post(reverse('todos:register'), {'email': 'test2@example.com', 'phone_number': '1234567890', 'password': 'test123', 'date_of_birth': '2000-01-01'})
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)
        self.assertNotEqual(response1.content.decode(), response2.content.decode())
        self.assertEqual(CustomUser.objects.count(), 2)
