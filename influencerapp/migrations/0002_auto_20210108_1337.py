# Generated by Django 3.1.4 on 2021-01-08 08:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('influencerapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shop_data',
            old_name='shop_id',
            new_name='id',
        ),
    ]
