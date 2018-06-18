# Generated by Django 2.0.5 on 2018-06-18 14:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_product_interested'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImagesTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('picture', models.ImageField(upload_to='myapp/images')),
            ],
        ),
        migrations.AddField(
            model_name='client',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='myapp/images'),
        ),
        migrations.AddField(
            model_name='imagestable',
            name='client',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='myapp.Client'),
        ),
    ]