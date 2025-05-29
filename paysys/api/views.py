import logging
from django.shortcuts import get_object_or_404
from rest_framework import status, serializers
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Organization
from .serializers import BankWebhookSerializer, OrganizationBalanceSerializer
from .schemas import bank_webhook_schema

logger = logging.getLogger(__name__)


@bank_webhook_schema
class BankWebhookView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = BankWebhookSerializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            payment = serializer.save()
            message = f"Payment {payment.amount} for payer_inn {payment.payer_inn} is accepted"
            return Response(message, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            if hasattr(e, 'get_codes') and e.get_codes().get('detail') == ['exists']:
                logger.info(f"Duplicate payment detected: {data.get('operation_id')}")
                return Response(status=status.HTTP_200_OK)
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)


class OrganizationBalanceView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, inn, *args, **kwargs):
        organization = get_object_or_404(Organization, inn=inn)
        serializer = OrganizationBalanceSerializer(organization)
        return Response(serializer.data)
