# Generated by Django 5.0.6 on 2024-05-29 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to='posts/')),
                ('post_date', models.DateTimeField(auto_now_add=True)),
                ('schedule_date', models.DateTimeField(blank=True, null=True)),
                ('processed_date', models.DateTimeField(blank=True, null=True)),
                ('is_promoted', models.BooleanField(default=False)),
            ],
        ),
    ]
