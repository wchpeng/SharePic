# Generated by Django 2.1.7 on 2019-06-15 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_auto_20190607_1646'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='picture',
            field=models.ImageField(default='user/pictures/default.jpg', upload_to='user/pictures', verbose_name='头像'),
        ),
    ]
