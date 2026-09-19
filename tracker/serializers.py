from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, BudgetSetup, DailyEntry, Article, DailyQuote


class UserSerializer(serializers.ModelSerializer):
    display_name = serializers.CharField(source='profile.display_name', required=False)
    bio = serializers.CharField(source='profile.bio', required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'display_name', 'bio']

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        profile = instance.profile
        profile.display_name = profile_data.get('display_name', profile.display_name)
        profile.bio = profile_data.get('bio', profile.bio)
        profile.save()
        return instance


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
        )
        return user


class DailyEntrySerializer(serializers.ModelSerializer):
    daily_total = serializers.ReadOnlyField()

    class Meta:
        model = DailyEntry
        fields = ['id', 'day', 'date', 'essentials', 'wants', 'savings', 'notes', 'daily_total']


class BudgetSetupSerializer(serializers.ModelSerializer):
    entries = DailyEntrySerializer(many=True, read_only=True)
    essentials_limit = serializers.ReadOnlyField()
    wants_limit = serializers.ReadOnlyField()
    savings_limit = serializers.ReadOnlyField()

    class Meta:
        model = BudgetSetup
        fields = [
            'id', 'month', 'monthly_income',
            'essentials_pct', 'wants_pct', 'savings_pct',
            'essentials_limit', 'wants_limit', 'savings_limit',
            'entries', 'created_at', 'updated_at',
        ]

    def validate(self, data):
        total = (
            data.get('essentials_pct', getattr(self.instance, 'essentials_pct', 0)) +
            data.get('wants_pct', getattr(self.instance, 'wants_pct', 0)) +
            data.get('savings_pct', getattr(self.instance, 'savings_pct', 0))
        )
        if abs(float(total) - 100.0) > 0.01:
            raise serializers.ValidationError("Percentages must add up to 100.")
        return data


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'


class DailyQuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyQuote
        fields = '__all__'