from django.db import models
from django.contrib.auth.models import User


class Transaction(models.Model):
    TRANSACTION_TYPE = (
        ("Income", "Income"),
        ("Expense", "Expense"),
    )

    CATEGORY_CHOICES = (
        ("Salary", "Salary"),
        ("Business", "Business"),
        ("Freelance", "Freelance"),
        ("Food", "Food"),
        ("Shopping", "Shopping"),
        ("Travel", "Travel"),
        ("Bills", "Bills"),
        ("Medical", "Medical"),
        ("Entertainment", "Entertainment"),
        ("Other", "Other"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    date = models.DateField()
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.title} - {self.amount}"