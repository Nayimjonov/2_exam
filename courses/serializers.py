from sqlite3 import register_adapter

from rest_framework import serializers
from .models import Category, Course, Module, Lesson
from enrollments.models import Enrollment
from reviews.models import Review

# CATEGORY
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'description', 'icon', 'created_at')


class CourseTeacherSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)


class CourseCategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('id', 'title', 'content', 'video_url', 'duration', 'order')


class CourseModuleSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True)

    class Meta:
        model = Module
        fields = ('id', 'title', 'description', 'order', 'lessons')


class ReviewUserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)


class ReviewSerializer(serializers.ModelSerializer):
    user = ReviewUserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'user', 'rating', 'comment', 'created_at')

# COURSE
class BaseCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = (
            'id',
            'title',
            'description',
            'teacher',
            'category',
            'price',
            'discount_price',
            'image',
            'is_published',
            'created_at',
            'updated_at',
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category'] = CourseCategorySerializer(instance.category).data
        representation['teacher'] = CourseTeacherSerializer(instance.teacher).data
        return representation


class CourseListSerializer(BaseCourseSerializer):
    modules = CourseModuleSerializer(many=True, required=False)

    class Meta(BaseCourseSerializer.Meta):
        fields = BaseCourseSerializer.Meta.fields + ('modules',)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['modules'] = CourseModuleSerializer(instance.modules.all(), many=True).data
        return representation

    def create(self, validated_data):
        modules_data = validated_data.pop('modules', [])
        course = Course.objects.create(**validated_data)

        for module_data in modules_data:
            lessons_data = module_data.pop('lessons', [])
            module = Module.objects.create(course=course, **module_data)
            for lesson_data in lessons_data:
                Lesson.objects.create(module=module, **lesson_data)
        return course


class CourseDetailSerializer(BaseCourseSerializer):
    modules = CourseModuleSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    students_count = serializers.SerializerMethodField()

    class Meta(BaseCourseSerializer.Meta):
        fields = BaseCourseSerializer.Meta.fields + ('modules', 'reviews', 'average_rating', 'students_count')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['modules'] = CourseModuleSerializer(instance.modules.all().order_by('order'), many=True).data
        return representation

    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews.exists():
            total = sum(review.rating for review in reviews)
            return round(total / reviews.count(), 1)
        return 0.0

    def get_students_count(self, obj):
        return Enrollment.objects.filter(course=obj).count()

# MODULE
class ModuleCourseSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(read_only=True)


class ModuleListSerializer(serializers.ModelSerializer):
    course = ModuleCourseSerializer(read_only=True)

    class Meta:
        model = Module
        fields = ('id', 'title', 'description', 'order', 'course', 'created_at')


class ModuleCreateSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True)
    course = ModuleCourseSerializer(read_only=True)

    class Meta:
        model = Module
        fields = ('id', 'title', 'description', 'order', 'course', 'created_at', 'lessons')

    def create(self, validated_data):
        lessons_data = validated_data.pop('lessons')
        course = validated_data.get('course')
        module = Module.objects.create(**validated_data)
        for lesson_data in lessons_data:
            Lesson.objects.create(module=module, **lesson_data)
        return module

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['course'] = ModuleCourseSerializer(instance.course).data
        return representation


class ModuleDetailSerializer(ModuleCreateSerializer):
    lessons = LessonSerializer(many=True, read_only=True)


class ModuleByCourseListSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    order = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    lessons_count = serializers.IntegerField(read_only=True)

# LESSON
class CourseSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(read_only=True)


class LessonModuleSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(read_only=True)


class LessonModuleDetailSerializer(LessonModuleSerializer):
    course = CourseSerializer(read_only=True)


class BaseLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = (
            'id',
            'title',
            'content',
            'video_url',
            'duration',
            'order',
            'created_at',
            'updated_at'
        )


class LessonsSerializer(BaseLessonSerializer):
    class Meta(BaseLessonSerializer.Meta):
        fields = BaseLessonSerializer.Meta.fields + ('module',)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['module'] = LessonModuleSerializer(instance.module).data
        return representation


class LessonDetailSerializer(LessonsSerializer):
    def to_representation(self, instance):
        representation = super(BaseLessonSerializer, self).to_representation(instance)
        representation['module'] = LessonModuleDetailSerializer(instance.module).data
        return representation



