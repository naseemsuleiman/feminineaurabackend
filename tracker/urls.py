from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('budgets', views.BudgetSetupViewSet, basename='budgets')
router.register('entries', views.DailyEntryViewSet, basename='entries')
router.register('articles', views.ArticleViewSet, basename='articles')
router.register('quotes', views.DailyQuoteViewSet, basename='quotes')

urlpatterns = [
    path('auth/register/', views.register_view, name='register'),
    path('auth/me/', views.me_view, name='me'),
    path('', include(router.urls)),
]