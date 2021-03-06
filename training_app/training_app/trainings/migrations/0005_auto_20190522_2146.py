# Generated by Django 2.2.1 on 2019-05-22 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainings', '0004_auto_20190521_2231'),
    ]

    operations = [
        migrations.RenameField(
            model_name='exercise',
            old_name='timestamp',
            new_name='created',
        ),
        migrations.RemoveField(
            model_name='exercise',
            name='primary_muscles',
        ),
        migrations.RemoveField(
            model_name='exercise',
            name='secondary_muscles',
        ),
        migrations.AddField(
            model_name='exercise',
            name='muscles_involved',
            field=models.ManyToManyField(related_name='exercises', to='trainings.MuscleGroup', verbose_name='Muscles involved'),
        ),
    ]
