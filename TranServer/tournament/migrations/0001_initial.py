# Generated by Django 5.0.3 on 2024-03-15 17:34

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('players', models.ManyToManyField(related_name='tournaments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
