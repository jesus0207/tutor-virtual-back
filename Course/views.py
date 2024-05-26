import json

from Users.permissions import IsOwnerPermission
import openai
from django.shortcuts import redirect, render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Course, User
from .serializers import CourseCreateSerializer, CourseListSerializer, QuestionSerializer


def validate_context(value):
    """
    Validate the context of a question.

    Args:
        value (str): The context to validate.

    Returns:
        bool: True if the context is valid, False otherwise.
    """
    words = value.split()
    return len(words) <= 40


def get_secret_key():
    """
    Get the OpenAI API key from secrets.json.

    Returns:
        str: The OpenAI API key.
    """
    with open('secrets.json') as f:
        secrets = json.load(f)
    return secrets.get('OPENAI_KEY')


api_key = 'get_secret_key()'
if api_key:
    openai.api_key = api_key


def ask_open_ai(context, question, model="gpt-3.5-turbo-16k"):
    """
    Ask a question to the OpenAI model.

    Args:
        context (str): The context to use for the question.
        question (str): The question to ask.
        model (str, optional): The OpenAI model to use. Defaults to "gpt-3.5-turbo-16k".

    Returns:
        str: The model's response to the question.
    """
    prompt = f'''using the context: {context}
answer the next question: {question} in maximum 150 words. 
If the answer is not related to the context, 
give the following answer: "The question is not related to the course". 
Provide your answer using the language used in the question.'''

    chat_messages = [{"role": "user", "content": prompt}]
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=chat_messages,
            temperature=0,
            max_tokens=300,
            n=1
        )
        answer = response.choices[0].message if response and response.choices else None
    except Exception as e:
        answer = None
        # Handle exceptions, such as logging errors or returning an error response to the user
    return answer if answer else "No response"


class List(generics.ListAPIView):
    """
    List all courses. (for students)
    """
    queryset = Course.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CourseListSerializer


class ListOwnCourse(generics.ListAPIView):
    """
    List courses owned by the authenticated user. (for instructors)
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CourseListSerializer

    def get_queryset(self):
        instructor_pk = self.request.user.id
        return Course.objects.filter(instructor__id=instructor_pk)


class Create(generics.CreateAPIView):
    """
    Create a new course. (for instructors)
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CourseCreateSerializer


class Chat(APIView):
    """
    Chat with the OpenAI model. (for students)
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = QuestionSerializer

    def post(self, request, pk):
        """
        Handle POST requests to chat with the OpenAI model.

        Args:
            request: The HTTP request object.
            pk (int): The primary key of the course.

        Returns:
            Response: The model's response to the question.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            question = serializer.validated_data.get('content')
            if validate_context(question):
                context = Course.get_context(pk)
                answer = ask_open_ai(context, question)
                return Response({'answer': answer})
            else:
                return Response({'error': 'Invalid question'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
