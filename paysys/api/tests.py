import uuid
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import status

from .models import Organization, Payment


class PaymentSystemTests(APITestCase):
    def setUp(self):
        self.org_inn = '1234567890'
        self.org = Organization.objects.create(inn=self.org_inn, balance=0)
        self.webhook_url = reverse('bank-webhook')
        self.valid_payload = {
            "operation_id": str(uuid.uuid4()),
            "amount": "145000.00",
            "payer_inn": self.org_inn,
            "document_number": "PAY-328",
            "document_date": timezone.now().isoformat()
        }

    def test_create_payment(self):
        """Тест успешного создания платежа"""
        response = self.client.post(
            self.webhook_url,
            data=self.valid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Payment.objects.filter(operation_id=self.valid_payload['operation_id']).exists())

        org = Organization.objects.get(inn=self.org_inn)
        self.assertEqual(org.balance, float(self.valid_payload['amount']))

    def test_duplicate_payment(self):
        """Тест обработки дубликата платежа"""
        response1 = self.client.post(
            self.webhook_url,
            data=self.valid_payload,
            format='json',
        )
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)

        response = self.client.post(
            self.webhook_url,
            data=self.valid_payload,
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_payload(self):
        """Тест невалидных данных"""
        invalid_payload = self.valid_payload.copy()
        invalid_payload['amount'] = "invalid_amount"

        response = self.client.post(
            self.webhook_url,
            data=invalid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('amount', response.data)

    def test_get_organization_balance(self):
        """Тест получения баланса организации"""
        self.client.post(
            self.webhook_url,
            data=self.valid_payload,
            format='json',
        )

        url = reverse('organization-balance', kwargs={'inn': self.org_inn})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['inn'], self.org_inn)
        self.assertEqual(float(response.data['balance']), float(self.valid_payload['amount']))

    def test_get_nonexistent_organization(self):
        """Тест запроса баланса несуществующей организации"""
        url = reverse('organization-balance', kwargs={'inn': '0000000000'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_missing_required_fields(self):
        """Тест отсутствия обязательных полей"""
        for field in ['operation_id', 'amount', 'payer_inn', 'document_number', 'document_date']:
            invalid_payload = self.valid_payload.copy()
            del invalid_payload[field]

            response = self.client.post(
                self.webhook_url,
                data=invalid_payload,
                format='json'
            )
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn(field, response.data)

    def test_invalid_inn_format(self):
        """Тест невалидного формата ИНН (не цифры)"""
        invalid_payload = self.valid_payload.copy()
        invalid_payload['payer_inn'] = '123abc4567'

        response = self.client.post(
            self.webhook_url,
            data=invalid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('payer_inn', response.data)
        self.assertIn('ИНН должен содержать только цифры', str(response.data['payer_inn'][0]))
