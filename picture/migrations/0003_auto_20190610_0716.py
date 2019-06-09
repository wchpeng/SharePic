# Generated by Django 2.1.7 on 2019-06-10 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picture', '0002_auto_20190607_1716'),
    ]

    operations = [
        migrations.CreateModel(
            name='FavoriteAlbum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('album_id', models.IntegerField(default=0, verbose_name='相册id')),
                ('creater_id', models.IntegerField(default=0, verbose_name='点赞人id')),
                ('creater_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '点赞',
                'verbose_name_plural': '点赞',
            },
        ),
        migrations.RemoveField(
            model_name='album',
            name='category',
        ),
    ]
