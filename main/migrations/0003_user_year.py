# Generated by Django 4.2.7 on 2023-11-19 23:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_user_center'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='year',
            field=models.CharField(blank=True, choices=[('2022', '2022'), ('2023', '2023')], max_length=20, null=True),
        ),
    ]