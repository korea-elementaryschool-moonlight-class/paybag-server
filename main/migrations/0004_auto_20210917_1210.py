# Generated by Django 3.2.6 on 2021-09-17 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_market_marketname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='name',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='card',
            name='updatedAt',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='ecobag',
            name='lastMarket',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='ecobag',
            name='market',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='ecobag',
            name='note',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='ecobag',
            name='uid',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='ecobag',
            name='updatedAt',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='history',
            name='rentMarket',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='history',
            name='returnMarket',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='history',
            name='updatedAt',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='market',
            name='count',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='market',
            name='marketName',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='market',
            name='stock',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='market',
            name='updatedAt',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='updatedAt',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
