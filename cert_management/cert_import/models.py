from django.db import models

# Create your models here.
class Certificate(models.Model):
    "The object of certificate"

    valid_start = models.DateField(auto_now=False, auto_now_add=False)
    valid_end = models.DateField(auto_now=False, auto_now_add=False)
    cert_id = models.CharField(max_length=50)
    cert_content = models.TextField(null=True)
    ca_chain = models.TextField(null=True)

class DNS(models.Model):
    """A DNS object."""

    name = models.CharField(max_length=100)
    certs = models.ManyToManyField(Certificate, related_name="dns")

class Host(models.Model):
    """A host object."""

    name = models.CharField(max_length=100)
    cert = models.ForeignKey(Certificate, on_delete=models.CASCADE, related_name="hosts")