# Generated by Django 4.2.7 on 2023-11-19 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='center',
            field=models.CharField(blank=True, choices=[('umuahia', 'umuahia'), ('aba', 'aba'), ('ohafia', 'ohafia')], max_length=20, null=True),
        ),
    ]
