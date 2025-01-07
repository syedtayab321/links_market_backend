import random
from django.db import models


class PublisherSingUp(models.Model):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    website = models.URLField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6, blank=True, null=True)

    def generate_verification_code(self):
        self.verification_code = str(random.randint(100000, 999999))
        self.save()


class WebsiteListing(models.Model):
    user = models.ForeignKey(PublisherSingUp, on_delete=models.CASCADE)
    url = models.URLField()
    meta_tag_verified = models.BooleanField(default=False)
    txt_file_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class PerformanceAnalytics(models.Model):
    user = models.OneToOneField(PublisherSingUp, on_delete=models.CASCADE)
    impressions = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    orders = models.IntegerField(default=0)
    sales_percentage = models.FloatField(default=0.0)
    ranking = models.IntegerField(default=0)


class Task(models.Model):
    STATUS_CHOICES = [
        ('received', 'Received'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
    ]
    user = models.ForeignKey(PublisherSingUp, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    updated_at = models.DateTimeField(auto_now=True)


class BulkUpload(models.Model):
    user = models.ForeignKey(PublisherSingUp, on_delete=models.CASCADE)
    file = models.FileField(upload_to="bulk_uploads/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
