# Generated by Django 3.2.9 on 2021-12-01 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cert_import', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='certificate',
            name='email',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.DeleteModel(
            name='DNS',
        ),
    ]