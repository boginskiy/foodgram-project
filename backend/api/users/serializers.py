from rest_framework import serializers
from users.models import User, UserFollowing
from recipes.models import Recipe


class UserMultiSerializer(serializers.ModelSerializer):
    """Базовый сериализатор для модели User."""

    is_subscribed = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()

    def get_first_name(self, obj):
        """Имя пишется с большой буквы."""

        return obj.first_name.title()

    def get_last_name(self, obj):
        """Фамилия пишется с большой буквы."""

        return obj.last_name.title()

    def get_is_subscribed(self, obj):
        """Поле is_subscribed для отображения статуса подписки."""

        request_user = self.context['request'].user.id
        queryset = UserFollowing.objects.filter(
            user=obj.id, subscriber=request_user).exists()
        return queryset

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed')


class UserSignupSerializer(serializers.ModelSerializer):
    """Сериализатор регистрации пользователя для модели User."""

    username = serializers.CharField(
        error_messages={'required': 'Обязательное поле.'})
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name', 'password')

    def create(self, validated_data):
        """Шифрование пользовательского пароля и сохранение в базе user."""

        user = super(UserSignupSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class ChangePasswordSerializer(serializers.Serializer):
    """Сериализатор обновления текущ. пароля для модели User."""

    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def update(self, instance, validated_data):
        """Обновление текущего пароля."""

        if not instance.check_password(validated_data['current_password']):
            raise serializers.ValidationError(
                {'message': 'Текущий пароль неверный'})
        if validated_data['current_password'] == \
                validated_data['new_password']:
            raise serializers.ValidationError(
                {'message': 'Новый пароль соответствует текущему'})

        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance


class UserRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для демонстрации рецептов пользователя."""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FollowingUserSerializer(serializers.ModelSerializer):
    """Сериализатор подписчиков и подписок для модели UserFollowing."""

    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    def get_recipes(self, obj):
        """Определение объектов внутри поля recipes."""

        recipes_limit = self.context['request'].query_params.get(
            'recipes_limit')

        if recipes_limit:
            queryset = Recipe.objects.filter(
                author=obj.id).order_by('id')[:int(recipes_limit)]
        else:
            queryset = obj.recipes
        serializer = UserRecipeSerializer(instance=queryset, many=True)
        return serializer.data

    def get_first_name(self, obj):
        """Имя с большой буквы."""

        return obj.first_name.title()

    def get_last_name(self, obj):
        """Фамилия с большой буквы."""

        return obj.last_name.title()

    def get_is_subscribed(self, obj):
        """Поле is_subscribed для отображения статуса подписки."""

        request_user = self.context['request'].user.id
        queryset = UserFollowing.objects.filter(
            user=obj.id, subscriber=request_user).exists()
        return queryset

    def get_recipes_count(self, obj):
        """Поле счетчика рецептов."""

        return obj.recipes.count()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed', 'recipes', 'recipes_count')
