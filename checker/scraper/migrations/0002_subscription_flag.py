# Generated by Django 4.0.5 on 2022-06-10 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='flag',
            field=models.IntegerField(default=0, verbose_name=0),
            preserve_default=False,
        ),
    ]
