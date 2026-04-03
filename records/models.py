from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.
class FinancialRecord(models.Model):
    TYPE_CHOICES = [('income', 'Income'), ('expense', 'Expense')]

    amount = models.DecimalField(max_digits=12, decimal_places=2)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    category = models.CharField(max_length=100)
    date = models.DateField()
    description  = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.type} - {self.amount} ({self.category})"