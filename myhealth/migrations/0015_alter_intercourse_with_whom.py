# Generated by Django 5.0 on 2024-01-11 02:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myhealth', '0014_contact_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='intercourse',
            name='with_whom',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='myhealth.contact'),
        ),
    ]
