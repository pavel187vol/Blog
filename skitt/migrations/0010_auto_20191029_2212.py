# Generated by Django 2.2.6 on 2019-10-29 19:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('skitt', '0009_auto_20191029_2117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='accounts.UserProfile'),
        ),
        migrations.AlterField(
            model_name='post',
            name='authon',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='accounts.UserProfile'),
        ),
    ]
