# Generated by Django 3.2.9 on 2021-12-01 21:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('not_before', models.DateTimeField(null=True)),
                ('not_after', models.DateTimeField(null=True)),
                ('serial_number', models.CharField(max_length=50, unique=True)),
                ('cert_content', models.TextField(null=True)),
                ('ca_chain', models.TextField(null=True)),
                ('issuer', models.CharField(max_length=200, null=True)),
                ('subject', models.CharField(max_length=200, null=True)),
                ('extension', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('name', models.CharField(max_length=100, primary_key=True, serialize=False, unique=True)),
                ('cert', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='hosts', to='cert_import.certificate')),
            ],
        ),
        migrations.CreateModel(
            name='DNS',
            fields=[
                ('name', models.CharField(max_length=100, primary_key=True, serialize=False, unique=True)),
                ('certs', models.ManyToManyField(null=True, related_name='dns', to='cert_import.Certificate')),
            ],
        ),
    ]
