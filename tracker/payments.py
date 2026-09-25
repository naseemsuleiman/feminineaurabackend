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
    user = request.user
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
            # Grab the reference Paystack created
            reference = res_data['data']['reference']
            # Return both the URL and reference to the frontend
            return Response({
                'url': res_data['data']['authorization_url'],
                'reference': reference,
            })
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

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_payment(request):
    """Verify a Paystack transaction by reference and unlock the user."""
    reference = request.data.get('reference')
    if not reference:
        return Response({'error': 'Reference required'}, status=400)

    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
    }

    try:
        r = requests.get(
            f"{PAYSTACK_API_URL}/transaction/verify/{reference}",
            headers=headers,
            timeout=15,
        )
        r.raise_for_status()
        data = r.json()
    except requests.exceptions.RequestException as e:
        return Response({'error': str(e)}, status=400)

    if not data.get('status'):
        return Response(
            {'error': data.get('message', 'Verification failed')},
            status=400,
        )

    txn = data.get('data', {})
    if txn.get('status') != 'success':
        return Response(
            {'has_paid': False, 'status': txn.get('status')},
            status=400,
        )

    # Double-check that this transaction belongs to THIS user
    meta = txn.get('metadata') or {}
    if str(meta.get('user_id')) != str(request.user.id):
        return Response({'error': 'Transaction does not belong to you'}, status=403)

    # Unlock
    profile = request.user.profile
    if not profile.has_paid:
        profile.has_paid = True
        profile.paid_at = timezone.now()
        profile.save()

    return Response({
        'has_paid': True,
        'reference': reference,
        'amount': txn.get('amount'),
        'paid_at': txn.get('paid_at'),
    })