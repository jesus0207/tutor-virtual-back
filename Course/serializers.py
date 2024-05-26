from rest_framework import serializers
from Users.models import User
from .models import Course


class CourseCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new course.
    """
    class Meta:
        model = Course
        fields = '__all__'
        extra_kwargs = {
            "name": {"required": True},
            "instructor": {"required": True},
            "description": {"required": True},
            "context": {"required": True},
            "creation_date": {"required": False}
        }

    def create(self, validated_data):
        """
        Create a new course instance.

        Args:
            validated_data (dict): Validated data for the new course.

        Returns:
            Course: The created course instance.
        """
        course = Course.objects.create(**validated_data)
        return course

    def is_valid(self, raise_exception=False):
        """
        Validate the serializer.

        Args:
            raise_exception (bool): Whether to raise a validation error if validation fails.

        Returns:
            bool: True if the serializer is valid, False otherwise.
        """
        if 'instructor' in self.initial_data:
            try:
                user = User.objects.get(pk=self.initial_data['instructor'])
                if user.rol != "Profesor":
                    self._errors = {'instructor': 'Only professors can create courses.'}
                    if raise_exception:
                        raise serializers.ValidationError(self.errors)
                    return False
            except User.DoesNotExist:
                self._errors = {'instructor': 'User does not exist.'}
                if raise_exception:
                    raise serializers.ValidationError(self.errors)
                return False
        return super().is_valid(raise_exception=raise_exception)


class QuestionSerializer(serializers.Serializer):
    """
    Serializer for questions.
    """
    content = serializers.CharField(max_length=200)


class CourseListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing courses.
    """
    instructor = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'
    
    def get_instructor(self, obj):
        """
        Get the full name of the course instructor.

        Args:
            obj (Course): The course instance.

        Returns:
            str: The full name of the instructor.
        """
        return f"{obj.instructor.first_name} {obj.instructor.last_name}"
