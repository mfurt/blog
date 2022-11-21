from rest_framework import serializers
from taggit_serializer.serializers import (TagListSerializerField,)
from .models import Post, Comment
import six


class NewTagListSerializerField(TagListSerializerField):
    def to_internal_value(self, value):
        if isinstance(value, six.string_types):
            value = value.split(',')

        if not isinstance(value, list):
            self.fail('not_a_list', input_type=type(value).__name__)

        for s in value:
            if not isinstance(s, six.string_types):
                self.fail('not_a_str')

            self.child.run_validation(s)
        return value


class CommentSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    author = serializers.CharField(max_length=45)
    comment = serializers.CharField(max_length=255)
    date = serializers.DateTimeField()
    post_id = serializers.SerializerMethodField()

    def get_post_id(self, obj):
        return obj.post_id

    class Meta:
        model = Comment
        fields = ('id', 'date', 'author', 'comment', 'post_id', )

class PostSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    title = serializers.CharField(max_length=350)
    date = serializers.DateTimeField(format="%H:%M %d.%m.%Y",required=False, read_only=True)
    anons = serializers.CharField(max_length=500)
    text = serializers.CharField()
    tags = NewTagListSerializerField()
    image = serializers.ImageField(required=False)
    comments = CommentSerializer(source='comment_set', many=True, required=False)

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        instance = super().create(validated_data)
        instance.tags.set(*tags)
        return instance

    def update(self, instance, validated_data, *args, **kwargs):
        title = validated_data.pop('title')
        instance.anons = validated_data.get('anons', instance.anons)
        instance.text = validated_data.get('text', instance.text)
        tags = validated_data.pop('tags')
        instance.title = title
        instance.tags.set(*tags)
        instance.save()
        return instance

    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)
        request = self.context.get('request')
        if request is not None and not request.parser_context.get('kwargs'):
            fields.pop('comments', None)
        return fields
    class Meta:
        model = Post
        fields = ('id', 'title', 'date', 'anons', 'text' , 'tags', 'image', 'comments',)





class TagSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(format="%H:%M %d.%m.%Y", required=False)
    tags = NewTagListSerializerField()
    class Meta:
        model = Post
        fields = ('id','date', 'title', 'anons', 'text' , 'tags', 'image')