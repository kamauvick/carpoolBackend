# Generated by Django 2.2.5 on 2019-12-13 10:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Demand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('available_seats', models.IntegerField()),
                ('departure_time', models.TimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'demand',
                'verbose_name_plural': 'demands',
                'db_table': 'demand',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('distance', models.IntegerField()),
            ],
            options={
                'db_table': 'location',
            },
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seats_needed', models.IntegerField()),
                ('departure_time', models.TimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_full', models.BooleanField(default=False)),
                ('is_ended', models.BooleanField(default=False)),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='offer_destination', to='WBBackend.Location')),
            ],
            options={
                'verbose_name': 'offer',
                'verbose_name_plural': 'offers',
                'db_table': 'offer',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=200, null=True)),
                ('last_name', models.CharField(max_length=200, null=True)),
                ('phone_number', models.CharField(max_length=100, null=True)),
                ('profile_pic', models.ImageField(blank=True, default='sample.jpg', null=True, upload_to='profile_pics/')),
                ('device_id', models.CharField(max_length=255)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'profile',
                'verbose_name_plural': 'profile',
                'db_table': 'profile',
            },
        ),
        migrations.CreateModel(
            name='RequestBoard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('PE', 'Pending'), ('AC', 'Accepted'), ('DE', 'Denied')], max_length=2)),
                ('demand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_request', to='WBBackend.Demand')),
                ('offer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requests', to='WBBackend.Offer')),
            ],
            options={
                'db_table': 'board_request',
            },
        ),
        migrations.CreateModel(
            name='UserData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=200, null=True)),
                ('last_name', models.CharField(max_length=200, null=True)),
                ('username', models.CharField(max_length=200)),
                ('phone_number', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'userdata',
            },
        ),
        migrations.CreateModel(
            name='TripDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('demand', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='WBBackend.Demand')),
                ('offer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='WBBackend.Offer')),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='WBBackend.RequestBoard')),
            ],
            options={
                'db_table': 'trip_details',
                'ordering': ['offer'],
            },
        ),
        migrations.CreateModel(
            name='TripChat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('time', models.DateTimeField(auto_now=True)),
                ('offer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='WBBackend.Offer')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='WBBackend.Profile')),
            ],
            options={
                'verbose_name': 'tripchat',
                'verbose_name_plural': 'tripchat',
                'db_table': 'tripchat',
            },
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField(null=True)),
                ('stop_time', models.TimeField(null=True)),
                ('offer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='WBBackend.Offer')),
            ],
            options={
                'db_table': 'trip',
                'ordering': ['offer'],
            },
        ),
        migrations.AddField(
            model_name='offer',
            name='driver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='driver_profile', to='WBBackend.Profile'),
        ),
        migrations.AddField(
            model_name='offer',
            name='origin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='offer_origin', to='WBBackend.Location'),
        ),
        migrations.AddField(
            model_name='demand',
            name='destination',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='demand_destination', to='WBBackend.Location'),
        ),
        migrations.AddField(
            model_name='demand',
            name='origin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='demand_origin', to='WBBackend.Location'),
        ),
        migrations.AddField(
            model_name='demand',
            name='passenger',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='trip_passenger', to='WBBackend.Profile'),
        ),
    ]
