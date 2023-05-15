# Generated by Django 4.2.1 on 2023-05-15 10:11

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0002_subscribe_payment_id_alter_subscribe_price'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='consumer',
            options={'verbose_name': 'Покупатель', 'verbose_name_plural': 'Покупатели'},
        ),
        migrations.AlterModelOptions(
            name='filmwork',
            options={'verbose_name': 'Фильм', 'verbose_name_plural': 'Фильмы'},
        ),
        migrations.AlterModelOptions(
            name='filmworksubscribe',
            options={'verbose_name': 'Фильм в подписке', 'verbose_name_plural': 'Фильмы в подписке'},
        ),
        migrations.AlterModelOptions(
            name='payment',
            options={'verbose_name': 'Платеж', 'verbose_name_plural': 'Платежи'},
        ),
        migrations.AlterModelOptions(
            name='subscribe',
            options={'verbose_name': 'Подписка', 'verbose_name_plural': 'Подписки'},
        ),
        migrations.AddField(
            model_name='payment',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Дата добавления'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='payment',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата обновления'),
        ),
        migrations.AlterField(
            model_name='consumer',
            name='subscribe',
            field=models.ManyToManyField(blank=True, to='billing.subscribe', verbose_name='Подписки пользователя'),
        ),
        migrations.AlterField(
            model_name='subscribe',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Описание'),
        ),
    ]
