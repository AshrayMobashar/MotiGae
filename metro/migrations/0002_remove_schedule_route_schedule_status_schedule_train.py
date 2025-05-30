# Generated by Django 4.2 on 2025-05-06 10:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('metro', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedule',
            name='route',
        ),
        migrations.AddField(
            model_name='schedule',
            name='status',
            field=models.CharField(choices=[('scheduled', 'Scheduled'), ('delayed', 'Delayed'), ('cancelled', 'Cancelled')], default='Scheduled', max_length=20),
        ),
        migrations.AddField(
            model_name='schedule',
            name='train',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='metro.train'),
        ),
    ]
