# Generated by Django 4.0.3 on 2022-04-10 00:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parte3', '0002_alter_comics_image_alter_comics_onsaledate'),
    ]

    operations = [
        migrations.AddField(
            model_name='comics',
            name='id_comics',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]