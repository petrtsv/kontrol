# Generated by Django 3.0.7 on 2020-06-19 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kontrol_panel', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='plot',
            name='title',
            field=models.CharField(default='test plot', max_length=64),
            preserve_default=False,
        ),
    ]