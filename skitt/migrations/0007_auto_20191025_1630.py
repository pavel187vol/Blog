# Generated by Django 2.2.6 on 2019-10-25 13:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('skitt', '0006_auto_20191021_1845'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='authon',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL),
        ),
    ]
