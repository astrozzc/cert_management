from django.db import models

# Create your models here.
class Certificate(models.Model):
    "The object of certificate"

    not_before = models.DateTimeField(auto_now=False, auto_now_add=False, null=True)
    not_after = models.DateTimeField(auto_now=False, auto_now_add=False, null=True)
    serial_number = models.CharField(max_length=50, unique=True)
    cert_content = models.TextField(null=True)
    issuer = models.CharField(max_length=200, null=True)
    subject = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=50, null=True)

class Host(models.Model):
    """A host object."""

    name = models.CharField(max_length=100, unique=True, primary_key=True)
    cert_in_use = models.ForeignKey(Certificate, on_delete=models.SET_NULL, null=True, related_name="hosts")
    certs = models.ManyToManyField(Certificate, related_name="dns_list")