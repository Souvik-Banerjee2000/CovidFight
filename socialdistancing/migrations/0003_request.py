# Generated by Django 2.2 on 2020-04-08 08:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement', '0001_initial'),
        ('socialdistancing', '0002_shop_shop_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expected_going_time', models.TimeField()),
                ('expected_leaving_time', models.TimeField()),
                ('placer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usermanagement.UserProfile')),
                ('shop_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Shop', to='socialdistancing.Shop')),
            ],
        ),
    ]
