# Generated by Django 2.1.7 on 2019-03-22 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proftosubmapping',
            name='Prof',
            field=models.CharField(max_length=100),
        ),
    ]
