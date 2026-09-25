from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views, payments

router = DefaultRouter()
router.register('budgets', views.BudgetSetupViewSet, basename='budgets')
router.register('entries', views.DailyEntryViewSet, basename='entries')
router.register('articles', views.ArticleViewSet, basename='articles')
router.register('quotes', views.DailyQuoteViewSet, basename='quotes')


urlpatterns = [
    # JWT auth
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Custom auth
    path('auth/register/', views.register_view, name='register'),
    path('auth/me/', views.me_view, name='me'),

    # Public
    path('site-status/', views.site_status_view, name='site-status'),
    path('subscribe/', views.subscribe_view, name='subscribe'),

    # Admin-only
    path('admin/subscribers/', views.subscribers_list_view, name='admin-subscribers'),
    path('admin/budgets/', views.admin_budgets_view, name='admin-budgets'),
    path('payments/create-checkout-session/', payments.create_checkout_session, name='create-checkout'),
    path('payments/status/', payments.payment_status, name='payment-status'),
    path('payments/create-checkout-session/', payments.create_checkout_session, name='create-checkout'),
    path('payments/webhook/', payments.paystack_webhook, name='paystack-webhook'),

    # Router
    path('', include(router.urls)),
]