from rest_framework import serializers
from Users.models import User
from .models import Course


class BaseCourseSerializer(serializers.ModelSerializer):
    """
    Base serializer for course with common validation.
    """

    def validate_instructor(self, value):
        """
        Validate that the instructor is a professor.

        Args:
            value (int): The ID of the instructor.

        Returns:
            User: The validated instructor.

        Raises:
            serializers.ValidationError: If the instructor does not exist or is not a professor.
        """
        try:
            user = User.objects.get(pk=value)
            if user.rol != "Profesor":
                raise serializers.ValidationError('Only professors can create courses.')
        except User.DoesNotExist:
            raise serializers.ValidationError('User does not exist.')
        return value


class CourseCreateSerializer(BaseCourseSerializer):
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
        return Course.objects.create(**validated_data)


class CourseUpdateSerializer(BaseCourseSerializer):
    """
    Serializer for updating a course.
    """
    class Meta:
        model = Course
        fields = ["name", "description", "context", "active"]


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
