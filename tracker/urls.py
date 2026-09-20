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
    path('site-status/', views.site_status_view, name='site-status'),
    path('subscribe/', views.subscribe_view, name='subscribe'),
    path('admin/subscribers/', views.subscribers_list_view, name='admin-subscribers'),
    path('', include(router.urls)),
]