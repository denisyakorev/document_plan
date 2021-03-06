# Generated by Django 2.0.1 on 2018-02-13 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doc_plan', '0004_auto_20180213_1531'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='auditory_profile',
        ),
        migrations.AddField(
            model_name='project',
            name='auditory_demography',
            field=models.TextField(blank=True, verbose_name='auditory_demography'),
        ),
        migrations.AddField(
            model_name='project',
            name='auditory_duty',
            field=models.TextField(blank=True, verbose_name='auditory_duty'),
        ),
        migrations.AddField(
            model_name='project',
            name='auditory_environment',
            field=models.TextField(blank=True, verbose_name='auditory_environment'),
        ),
        migrations.AddField(
            model_name='project',
            name='auditory_knowledge',
            field=models.TextField(blank=True, verbose_name='auditory_knowledge'),
        ),
        migrations.AddField(
            model_name='project',
            name='auditory_relations',
            field=models.TextField(blank=True, verbose_name='auditory_relations'),
        ),
        migrations.AddField(
            model_name='project',
            name='auditory_resume',
            field=models.TextField(blank=True, verbose_name='auditory_resume'),
        ),
        migrations.DeleteModel(
            name='AuditoryProfile',
        ),
    ]
