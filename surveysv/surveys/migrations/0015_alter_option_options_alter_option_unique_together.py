# Generated by Django 5.1 on 2024-08-16 17:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0014_question_created_question_updated_survey_created_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='option',
            options={'ordering': ['order']},
        ),
        migrations.AlterUniqueTogether(
            name='option',
            unique_together={('question', 'value')},
        ),
    ]
