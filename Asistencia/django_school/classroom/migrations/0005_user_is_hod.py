# Generated by Django 2.0.1 on 2019-03-27 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0004_auto_20190322_1700'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_hod',
            field=models.BooleanField(default=False),
        ),
    ]
