# Generated by Django 3.2.6 on 2021-09-17 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20210917_1220'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='barcode_id',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]