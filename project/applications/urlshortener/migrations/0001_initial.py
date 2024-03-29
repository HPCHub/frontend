# Generated by Django 2.2.4 on 2019-10-02 11:36

from django.db import migrations, models
import django.db.models.deletion
import urlshortener.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ShortUrl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_id', models.SlugField(max_length=10, null=True, verbose_name='Short ID')),
                ('description', models.CharField(max_length=80, null=True, verbose_name='Description')),
                ('basic_url', urlshortener.models.ExtendedUrlField(verbose_name='Main url')),
                ('pub_date', models.DateTimeField(null=True, verbose_name='Created')),
                ('last_click', models.DateTimeField(null=True, verbose_name='Last click')),
                ('count', models.IntegerField(default=0, verbose_name='Clicks count')),
            ],
            options={
                'verbose_name': 'Short url',
                'verbose_name_plural': 'Short urls',
            },
        ),
        migrations.CreateModel(
            name='UserData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('click_time', models.DateTimeField(null=True, verbose_name='Click')),
                ('user_data', models.TextField(default='[]', null=True, verbose_name='User agent')),
                ('user_ip', models.CharField(default='', max_length=15, null=True, verbose_name='IP')),
                ('short_url', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='urlshortener.ShortUrl', verbose_name='Short url')),
            ],
            options={
                'verbose_name': 'Useragent',
                'verbose_name_plural': 'Useragents',
            },
        ),
    ]
