# Generated by Django 5.0.6 on 2024-07-31 04:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_usermaster_is_active_usermaster_is_admin_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserActivityTracking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField(blank=True, editable=False, null=True)),
                ('url', models.CharField(blank=True, editable=False, max_length=255, null=True)),
                ('request_type', models.CharField(blank=True, editable=False, max_length=10, null=True)),
                ('request_data', models.JSONField(blank=True, editable=False, null=True)),
                ('user_agent', models.CharField(blank=True, max_length=255, null=True)),
                ('referer', models.URLField(blank=True, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('state', models.CharField(blank=True, max_length=100, null=True)),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
                ('pincode', models.CharField(blank=True, max_length=20, null=True)),
                ('status_code', models.IntegerField(blank=True, editable=False, null=True)),
                ('response_time', models.FloatField(blank=True, editable=False, null=True)),
                ('response', models.JSONField(blank=True, editable=False, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_activity', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User Activity Tracking',
                'verbose_name_plural': 'User Activity Tracking',
                'db_table': 'user_activity_tracking',
                'ordering': ['-id'],
            },
        ),
    ]
