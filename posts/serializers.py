from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User, Post, Comment


class UserSerializer(serializers.HyperlinkedModelSerializer):
    firstName = serializers.CharField(source='first_name')
    lastName = serializers.CharField(source='last_name')
    displayName = serializers.CharField(source='username', validators=[UniqueValidator(User.objects.all())])
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

class CommentSerializer(serializers.HyperlinkedModelSerializer):

    # maybe also many=False
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ("author", "comment", "contentType", "published", "id")


class PostSerializer(serializers.HyperlinkedModelSerializer):

    comments = CommentSerializer(read_only=True, many=True)

    class Meta:
        model = Post
        fields = ("id", "title", "source", "origin", "description", "contentType", "content", "published", "visibility", "unlisted", "comments")

























# anchor
