from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    UserProfile, BudgetSetup, DailyEntry,
    Article, DailyQuote, Subscriber, SiteStatus,
)


class UserSerializer(serializers.ModelSerializer):
    display_name = serializers.CharField(source='profile.display_name', required=False)
    bio = serializers.CharField(source='profile.bio', required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'is_staff', 'email', 'display_name', 'bio']
        read_only_fields = ['id', 'is_staff']

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
        fields = ['id', 'day', 'date', 'essentials', 'wants', 'notes', 'daily_total']


class BudgetSetupSerializer(serializers.ModelSerializer):
    entries = DailyEntrySerializer(many=True, read_only=True)
    savings_pct = serializers.ReadOnlyField()

    class Meta:
        model = BudgetSetup
        fields = [
            'id', 'month', 'monthly_income', 'savings_goal',
            'savings_pct', 'entries', 'created_at', 'updated_at',
        ]

    def validate(self, data):
        income = float(data.get('monthly_income', 0) or 0)
        savings = float(data.get('savings_goal', 0) or 0)
        if savings <= 0:
            raise serializers.ValidationError("Please enter a savings amount greater than 0.")
        if income and savings >= income:
            raise serializers.ValidationError("Savings goal must be less than your income.")
        return data


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'


class DailyQuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyQuote
        fields = '__all__'


class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = ['id', 'email', 'created_at']


class SiteStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteStatus
        fields = ['is_live', 'updated_at']