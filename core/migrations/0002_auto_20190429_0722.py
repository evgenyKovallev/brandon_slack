# Generated by Django 2.2 on 2019-04-29 04:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='code',
            field=models.CharField(default='', max_length=255),
        ),
    ]
