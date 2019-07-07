# Generated by Django 2.2.1 on 2019-05-26 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainings', '0008_auto_20190524_2018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='musclegroup',
            name='name',
            field=models.CharField(help_text='Name of a muscle group', max_length=50, unique=True, verbose_name='Name'),
        ),
    ]
