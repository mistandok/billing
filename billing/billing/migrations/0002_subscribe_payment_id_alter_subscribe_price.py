# Generated by Django 4.2.1 on 2023-05-14 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscribe',
            name='payment_id',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='ID продукта в платежной системе'),
        ),
        migrations.AlterField(
            model_name='subscribe',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='Цена подписки USD'),
        ),
    ]