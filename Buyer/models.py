from django.db import models


class BuyerSignUp(models.Model):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    password = models.CharField(max_length=128)  # Store hashed passwords

    def __str__(self):
        return self.username


class TaskCreation(models.Model):
    buyer = models.ForeignKey(BuyerSignUp, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    deadline = models.DateField()
    status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed')
    ], default='Pending')

    def __str__(self):
        return self.title


