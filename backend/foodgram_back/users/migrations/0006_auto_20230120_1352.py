# Generated by Django 3.2.16 on 2023-01-20 13:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20230120_1320'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscribe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscribing', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriber', to=settings.AUTH_USER_MODEL, verbose_name='Подписчик')),
            ],
            options={
                'verbose_name': 'Подпиcка',
                'verbose_name_plural': 'Подписки',
            },
        ),
        migrations.DeleteModel(
            name='Subscriber',
        ),
        migrations.AddConstraint(
            model_name='subscribe',
            constraint=models.UniqueConstraint(fields=('user', 'author'), name='unique_user_subscribing'),
        ),
    ]
