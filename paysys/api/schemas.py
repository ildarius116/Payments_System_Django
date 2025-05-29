from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse

from .serializers import BankWebhookSerializer

bank_webhook_schema = extend_schema(
        request=BankWebhookSerializer,
        examples=[
            OpenApiExample(
                "Example request",
                value={
                    "operation_id": "ccf0a86d-041b-4991-bcf7-e2352f7b8a4a",
                    "amount": 145000,
                    "payer_inn": "1234567890",
                    "document_number": "PAY-328",
                    "document_date": "2024-04-27T21:00:00Z"
                },
                request_only=True
            )
        ],
        responses={
            201: OpenApiResponse(description="Payment processed"),
            200: OpenApiResponse(description="Payment already exists"),
            400: OpenApiResponse(description="Invalid data")
        }
    )