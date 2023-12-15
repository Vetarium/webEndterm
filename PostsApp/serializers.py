from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

from PostsApp.models import User, Post, ReviewPost





class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name'] #чтобы возвращать данные




class PostSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault()) #кто дернул вьюшку тот пользователь и есть
    author_data = AuthorSerializer(read_only=True, source='author') # чтобы данные возвращались для поста
    has_liked = serializers.SerializerMethodField()

    def get_has_liked(self, obj) -> bool:
        user = self.context['request'].user
        if user.is_anonymous:
            return None

        like = ReviewPost.objects.filter(author=user, post=obj).first()
        return getattr(like, 'like', None)



    def create(self, validated_data):
        post = super().create(validated_data)
        return(post)

    def update(self, instance, validated_data):
        post = super().update(instance, validated_data)

        return(post)

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['likes', 'dislikes']



class ReviewPostSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    def create(self, validated_data):
        like = super().create(validated_data)
        like.post.updateLikes()
        return (like)

    def update(self, instance, validated_data):
        reviewpost = super().update(instance, validated_data)
        like = super().create(validated_data)
        like.post.updateLikes()
        return (like)



    def validate_review(self, review):
        user = self.context['request'].user
        if review.author == user:
            raise ValidationError('You cannot like yourself')

        return review

    class Meta:
        model = Post
        fields = '__all__'
        validators = [serializers.UniqueTogetherValidator(queryset=Post.objects.all(), fields= ['author', 'post'])]




class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField( # валидация имейла чтобы не дубилкаты и чтобы регистр не ломал
        validators=[
            UniqueValidator(
                queryset= User.objects.all(), lookup='iexact')
        ]
    )


    password = serializers.CharField(write_only=True) # валидации на пароль писать тут и чтоб не возвращало пароль после создания
    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return(user)
    class Meta:
        model = User
        fields = [ 'first_name', 'last_name', "email", 'password', 'username']


