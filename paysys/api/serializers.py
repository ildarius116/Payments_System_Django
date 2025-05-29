import logging
from django.core.validators import MinLengthValidator, RegexValidator
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Organization, Payment

logger = logging.getLogger(__name__)


class BankWebhookSerializer(serializers.ModelSerializer):
    payer_inn = serializers.CharField(
        max_length=12,
        validators=[
            MinLengthValidator(10),
            RegexValidator(
                regex='^[0-9]{10,12}$',
                message='ИНН должен содержать только цифры (10 или 12 знаков)'
            )
        ],
        help_text='ИНН плательщика (10 или 12 цифр)'
    )

    class Meta:
        model = Payment
        fields = ['operation_id', 'amount', 'payer_inn', 'document_number', 'document_date']
        extra_kwargs = {
            'operation_id': {'help_text': 'UUID операции'},
            'amount': {'help_text': 'Сумма платежа'},
            'document_number': {'help_text': 'Номер платежного документа'},
            'document_date': {'help_text': 'Дата документа в формате ISO 8601'}
        }

    def validate(self, data):
        if Payment.objects.filter(operation_id=data['operation_id']).exists():
            logger.info(f"Payment with operation_id {data['operation_id']} already exists. Skipping.")
            raise ValidationError(
                {"detail": "Payment already exists"},
                code='exists'
            )
        return data

    def create(self, validated_data):
        organization, created = Organization.objects.get_or_create(
            inn=validated_data['payer_inn'],
            defaults={'balance': 0}
        )

        payment = Payment.objects.create(**validated_data)

        organization.balance += validated_data['amount']
        organization.save()

        logger.info(
            f"Processed payment {payment.operation_id}. "
            f"Organization {organization.inn} balance updated by {validated_data['amount']}. "
            f"New balance: {organization.balance}"
        )

        return payment


class OrganizationBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['inn', 'balance']
