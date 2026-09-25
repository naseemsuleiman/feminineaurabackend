import requests
import hmac
import hashlib
import json

from django.conf import settings
from django.utils import timezone
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response


PAYSTACK_API_URL = "https://api.paystack.co"


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_checkout_session(request):
    """Create a Paystack Payment Page redirect for the budget tracker."""
    user = request.user
    # Paystack amounts are in kobo/cents. 1 KES = 100 subunits.
    # Example: 1000 KES = 100000
    amount_in_subunit = 1 * 100 

    frontend_url = request.data.get('frontend_url', 'https://www.feminine-aura.com')

    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "email": user.email or f"{user.username}@feminine-aura.com",
        "amount": amount_in_subunit,
        "currency": "KES",
        "callback_url": f"{frontend_url}/budget-tracker?payment=success",
        "metadata": {
            "user_id": user.id,
            "username": user.username,
        },
    }

    try:
        response = requests.post(
            f"{PAYSTACK_API_URL}/transaction/initialize",
            json=data,
            headers=headers,
            timeout=15,
        )
        response.raise_for_status()
        res_data = response.json()

        if res_data and res_data.get('status'):
            return Response({'url': res_data['data']['authorization_url']})
        return Response(
            {'error': res_data.get('message', 'Initialization failed')},
            status=400,
        )
    except requests.exceptions.RequestException as e:
        return Response({'error': str(e)}, status=400)


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def paystack_webhook(request):
    """Paystack sends events here. Verify signature, then unlock access."""
    payload = request.body
    signature = request.META.get('HTTP_X_PAYSTACK_SIGNATURE', '')

    # Verify the signature
    computed_signature = hmac.new(
        settings.PAYSTACK_SECRET_KEY.encode('utf-8'),
        payload,
        hashlib.sha512,
    ).hexdigest()

    if computed_signature != signature:
        return HttpResponse(status=400)

    try:
        event = json.loads(payload)
    except json.JSONDecodeError:
        return HttpResponse(status=400)

    if event.get('event') == 'charge.success':
        data = event.get('data', {})
        user_id = data.get('metadata', {}).get('user_id')

        if user_id:
            try:
                user = User.objects.get(id=user_id)
                user.profile.has_paid = True
                user.profile.paid_at = timezone.now()
                user.profile.save()
            except User.DoesNotExist:
                pass

    return HttpResponse(status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def payment_status(request):
    """Return whether the current user has paid."""
    return Response({
        'has_paid': request.user.profile.has_paid,
        'is_staff': request.user.is_staff,
    })