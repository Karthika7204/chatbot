# Generated by Django 4.2.16 on 2024-09-06 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=220)),
                ('patterns', models.TextField()),
                ('responses', models.TextField()),
            ],
        ),
    ]
