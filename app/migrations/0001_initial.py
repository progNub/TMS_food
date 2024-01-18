# Generated by Django 5.0.1 on 2024-01-10 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('preview_image', models.ImageField(upload_to='images/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('time_minutes', models.IntegerField()),
                ('category', models.CharField(choices=[('B', 'Завтрак'), ('D', 'Обед'), ('S', 'Ужин')], max_length=1)),
                ('ingredients', models.ManyToManyField(to='app.ingredient')),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
    ]
