from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import BudgetSetup, DailyEntry, Article, DailyQuote
from .serializers import (
    UserSerializer, RegisterSerializer, BudgetSetupSerializer,
    DailyEntrySerializer, ArticleSerializer, DailyQuoteSerializer
)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def me_view(request):
    if request.method == 'GET':
        return Response(UserSerializer(request.user).data)
    serializer = UserSerializer(request.user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BudgetSetupViewSet(viewsets.ModelViewSet):
    serializer_class = BudgetSetupSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return BudgetSetup.objects.filter(user=self.request.user).order_by('-month')

    def perform_create(self, serializer):
        budget = serializer.save(user=self.request.user)
        for day in range(1, 31):
            DailyEntry.objects.create(budget=budget, day=day)
        
    @action(detail=False, methods=['get'], url_path='current')
    def current(self, request):
        month = request.query_params.get('month')
        if not month:
            from datetime import date
            month = date.today().strftime('%Y-%m')
        budget = BudgetSetup.objects.filter(user=request.user, month=month).first()
        if not budget:
            return Response({'detail': 'No budget for this month.'}, status=404)
        return Response(BudgetSetupSerializer(budget).data)


class DailyEntryViewSet(viewsets.ModelViewSet):
    serializer_class = DailyEntrySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return DailyEntry.objects.filter(budget__user=self.request.user)

    def perform_update(self, serializer):
        serializer.save()


class ArticleViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ArticleSerializer
    permission_classes = [AllowAny]
    queryset = Article.objects.filter(published=True).order_by('-created_at')

    def get_queryset(self):
        qs = super().get_queryset()
        category = self.request.query_params.get('category')
        if category:
            qs = qs.filter(category=category)
        return qs


class DailyQuoteViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = DailyQuoteSerializer
    permission_classes = [AllowAny]
    queryset = DailyQuote.objects.filter(active=True).order_by('-created_at')[:10]