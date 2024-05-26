from django.db import models
from Users.models import User


def validate_context(value):
    words = value.split()
    return len(words) <= 130


class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name="Title for your course")
    instructor = models.ForeignKey(User, on_delete=models.PROTECT, related_name="courses", blank=False)
    description = models.CharField(max_length=200, verbose_name="Write a quick description of your course")
    context = models.TextField(
        verbose_name="Write the topics, context, and a large description for your course",
    )
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name="Creation date")

    class Meta:
        ordering = ['name']

    @staticmethod
    def get_by_id(course_id):
        return Course.objects.filter(pk=course_id).first()

    @staticmethod
    def get_context(course_id):
        course = Course.get_by_id(course_id)
        if course is None:
            return "Without context"
        else:
            return f'{course.name}: {course.context}'

    @staticmethod
    def create(name, description, context):
        if validate_context(context):
            course = Course.objects.create(name=name, description=description, context=context)
            return course
        return None
