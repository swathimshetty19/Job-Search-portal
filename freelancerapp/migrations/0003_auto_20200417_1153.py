# Generated by Django 3.0.5 on 2020-04-17 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('freelancerapp', '0002_auto_20200416_1425'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projects',
            name='mem_needed',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='projects',
            name='min_payment',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='projects',
            name='status',
            field=models.CharField(default='', max_length=100),
        ),
    ]
