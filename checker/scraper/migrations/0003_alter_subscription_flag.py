# Generated by Django 4.0.5 on 2022-06-12 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0002_subscription_flag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='flag',
            field=models.IntegerField(default=0),
        ),
    ]