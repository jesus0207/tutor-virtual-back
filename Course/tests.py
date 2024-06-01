from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from Users.models import User
from .models import Course


class CourseAPITestCase(APITestCase):

    def setUp(self):
        # Crear usuarios para pruebas
        self.student_user = User.objects.create_user(
            first_name='student',
            last_name='test',
            email='student@gmail.com',
            password='password',
            rol='Estudiante'
        )
        self.instructor_user = User.objects.create_user(
            first_name='instructor',
            last_name='test',
            email='instructor@gmail.com',
            password='password',
            rol='Profesor'
        )
        self.course = Course.objects.create(
            name='Test Course',
            instructor=self.instructor_user,
            description='A test course',
            context='Test context'
        )

    def test_list_courses(self):
        self.client.login(username='student@gmail.com', password='password')
        url = reverse('student_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_list_own_courses(self):
        self.client.login(username='instructor@gmail.com', password='password')
        url = reverse('instructor_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_course(self):
        self.client.login(username='instructor@gmail.com', password='password')
        url = reverse('instructor_register')
        data = {
            'name': 'New Course',
            'instructor': self.instructor_user.id,
            'description': 'A new course description',
            'context': 'New context'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_course(self):
        self.client.login(username='instructor@gmail.com', password='password')
        url = reverse('instructor_modify', args=[self.course.pk])
        data = {
            'name': 'Updated Course',
            'description': 'Updated description',
            'context': 'Updated context',
            'active': True
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_chat_with_model(self):
        self.client.login(username='student@gmail.com', password='password')
        url = reverse('chat', args=[self.course.pk])
        data = {
            'content': 'What is the context?'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('answer', response.data)
