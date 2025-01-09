from django.db import models


class BuyerSignUp(models.Model):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    password = models.CharField(max_length=128)  # Store hashed passwords

    def __str__(self):
        return self.username


class TaskCreation(models.Model):
    buyer = models.ForeignKey('BuyerSignUp', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    deadline = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=[
            ('Pending', 'Pending'),
            ('In Progress', 'In Progress'),
            ('Completed', 'Completed')
        ],
        default='Pending'
    )

    def __str__(self):
        return self.title


class Order(models.Model):
    PENDING = 'Pending'
    IN_PROGRESS = 'In Progress'
    COMPLETED = 'Completed'

    ORDER_STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (IN_PROGRESS, 'In Progress'),
        (COMPLETED, 'Completed')
    ]

    buyer = models.ForeignKey('BuyerSignUp', on_delete=models.CASCADE)
    #product = models.ForeignKey('Publisher.Product', on_delete=models.CASCADE)  # Use string reference to avoid import issues
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default=PENDING)
    ordered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.buyer.username}"


class BuyerProfile(models.Model):
    buyer = models.OneToOneField('BuyerSignUp', on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    #profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return f"Profile of {self.buyer.username}"


class Escrow(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    buyer = models.ForeignKey('BuyerSignUp', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[
            ('Pending', 'Pending'),
            ('Released', 'Released'),
            ('Refunded', 'Refunded')
        ],
        default='Pending'
    )

    def __str__(self):
        return f"Escrow for Order #{self.order.id}"


class Dashboard(models.Model):
    buyer = models.OneToOneField('BuyerSignUp', on_delete=models.CASCADE)
    total_orders = models.IntegerField(default=0)
    total_tasks = models.IntegerField(default=0)
    total_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_pending_orders = models.IntegerField(default=0)

    def __str__(self):
        return f"Dashboard for {self.buyer.username}"
