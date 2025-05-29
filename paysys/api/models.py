from django.db import models
from django.core.validators import MinLengthValidator


class Organization(models.Model):
    inn = models.CharField(
        max_length=12,
        unique=True,
        validators=[MinLengthValidator(10)],
        verbose_name="ИНН организации"
    )
    balance = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0,
        verbose_name="Баланс"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Организация"
        verbose_name_plural = "Организации"

    def __str__(self):
        return f"Организация ИНН {self.inn}"


class Payment(models.Model):
    operation_id = models.UUIDField(unique=True, verbose_name="ID операции")
    amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Сумма")
    payer_inn = models.CharField(max_length=12, verbose_name="ИНН плательщика")
    document_number = models.CharField(max_length=255, verbose_name="Номер документа")
    document_date = models.DateTimeField(verbose_name="Дата документа")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
        indexes = [
            models.Index(fields=['payer_inn']),
        ]

    def __str__(self):
        return f"Платеж {self.operation_id} на сумму {self.amount}"
