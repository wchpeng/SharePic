# Generated by Django 2.2.1 on 2019-06-10 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picture', '0005_album_first_picture_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='tags',
            field=models.ManyToManyField(null=True, to='picture.AlbumTag', verbose_name='标签'),
        ),
    ]
