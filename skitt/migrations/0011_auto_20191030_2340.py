# Generated by Django 2.2.6 on 2019-10-30 20:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('skitt', '0010_auto_20191029_2212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='authon',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL),
        ),
    ]
