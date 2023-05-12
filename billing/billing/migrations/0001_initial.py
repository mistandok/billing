# Generated by Django 4.2.1 on 2023-05-11 14:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Consumer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('user_id', models.UUIDField(null=True, verbose_name='ID пользователя')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('subscribe_type', models.CharField(choices=[('OU', 'Наш кинотеатр'), ('AM', 'Амедиатека')], max_length=2, null=True, verbose_name='Тип подписки')),
                ('active', models.BooleanField(default=False, verbose_name='Активная')),
                ('consumer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='billing.consumer', verbose_name='Пользователь')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Payments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('sum', models.FloatField(null=True, verbose_name='Сумма покупки')),
                ('consumer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='billing.consumer', verbose_name='Пользователь')),
                ('subscription', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='billing.subscription', verbose_name='Подписка')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]