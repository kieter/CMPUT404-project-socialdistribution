from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User, Post, Comment, Category
import base64


class UserSerializer(serializers.HyperlinkedModelSerializer):
    firstName = serializers.CharField(source='first_name')
    lastName = serializers.CharField(source='last_name')
    displayName = serializers.CharField(source='username')
    password1 = serializers.CharField(write_only=True, required=False)
    password2 = serializers.CharField(write_only=True, required=False)
    github = serializers.URLField(allow_blank=True, required=False)
    email = serializers.EmailField()

    class Meta:
        model = User
        write_only_fields = ('password1', 'password2')
        fields = ('id', 'displayName', 'github', 'firstName', 'lastName', 'bio', 'email', 'password1', 'password2')

    def validate(self, data):
        if self.context['create'] and ('password1' not in data.keys() or 'password2' not in data.keys()):
            raise serializers.ValidationError("Please enter a password")
        if self.context['create'] and (len(data['password1']) < 1 or len(data['password2']) < 1):
            raise serializers.ValidationError("Please enter a password")
        if self.context['create'] and data['password1'] != data['password2']:
            raise serializers.ValidationError('Passwords do not match.')
        return super(UserSerializer, self).validate(data)

    def create(self, validated_data):
        if 'github' in validated_data.keys():
            github = validated_data['github']
        else:
            github=""
        if 'bio' in validated_data.keys():
            bio = validated_data['bio']
        else:
            bio = ""
        user = User(
            username=validated_data['username'],
            github=github,
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            bio=bio,
            email=validated_data['email'],
        )
        user.set_password(validated_data['password1'])
        user.save()
        return user

# handle binary content of post
# not sure if this will work with all data types yet but works with strings
class BinaryContent(serializers.Field):
    def to_representation(self, value):
        return base64.decodestring(value.content)

    def to_internal_value(self, data):
        return {"content" : base64.encodestring(data.encode())}


class CommentSerializer(serializers.HyperlinkedModelSerializer):

    # maybe also many=False
    author = UserSerializer()

    class Meta:
        model = Comment
        fields = ("author", "comment", "contentType", "published", "id")

    def create(self, validated_data):
        # print(validated_data)
        user_data = validated_data.pop('author')
        post_id = self.context['post_id']
        post = Post.objects.get(pk=post_id)
        user = User.objects.get(username=user_data['username'])
        comment = Comment.objects.create(parent_post=post, author=user, **validated_data)
        return comment




class PostSerializer(serializers.HyperlinkedModelSerializer):
    # # TODO: dont forget to re-add this, caused errors --> content = BinaryContent(source='*')
    # TODO: add next field to post (points to first page of comments)
    author = UserSerializer()
    comments = CommentSerializer(many=True)
    categories = serializers.SlugRelatedField(
        many=True,
        queryset=Category.objects.all(),
        slug_field='category'
    )

    class Meta:
        model = Post
        fields = ('id', 'title', 'source', 'origin', 'description', 'author', 'categories', 'contentType', 'content', 'published', 'visibility', 'unlisted', 'comments')

    def create(self, validated_data):
        user_data = validated_data.pop('author')
        category_data = validated_data.pop('categories')
        comment_data = validated_data.pop('comments')
        user = User.objects.get(username=user_data['username'])
        post = Post.objects.create(author=user, **validated_data)
        return post




























# anchor
