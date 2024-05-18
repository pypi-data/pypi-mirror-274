# Generated by Django 5.0.4 on 2024-05-05 19:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('nets_core', '0009_userdevice_ip'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Name')),
                ('codename', models.CharField(max_length=150, verbose_name='Codename')),
                ('description', models.CharField(blank=True, max_length=250, null=True, verbose_name='Description')),
                ('project_id', models.PositiveIntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Permission',
                'verbose_name_plural': 'Permissions',
                'db_table': 'nets_core_permission',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Name')),
                ('codename', models.CharField(max_length=150, verbose_name='Codename')),
                ('description', models.CharField(max_length=250, verbose_name='Description')),
                ('project_id', models.PositiveIntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Role',
                'verbose_name_plural': 'Roles',
                'db_table': 'nets_core_role',
            },
        ),
        migrations.CreateModel(
            name='UserRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_id', models.PositiveIntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'User Role',
                'verbose_name_plural': 'User Roles',
                'db_table': 'nets_core_user_role',
            },
        ),
        migrations.AlterModelOptions(
            name='emailnotification',
            options={'verbose_name': 'Email Notification', 'verbose_name_plural': 'Email Notifications'},
        ),
        migrations.AlterModelOptions(
            name='emailtemplate',
            options={'verbose_name': 'Email Template', 'verbose_name_plural': 'Email Templates'},
        ),
        migrations.AddField(
            model_name='customemail',
            name='project_content_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
        migrations.AddField(
            model_name='customemail',
            name='project_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='emailnotification',
            name='project_content_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
        migrations.AddField(
            model_name='emailnotification',
            name='project_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='emailtemplate',
            name='project_content_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
        migrations.AddField(
            model_name='emailtemplate',
            name='project_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddIndex(
            model_name='customemail',
            index=models.Index(fields=['project_content_type', 'project_id'], name='custom_email_index'),
        ),
        migrations.AddIndex(
            model_name='emailnotification',
            index=models.Index(fields=['project_content_type', 'project_id'], name='email_notification_index'),
        ),
        migrations.AddIndex(
            model_name='emailtemplate',
            index=models.Index(fields=['project_content_type', 'project_id'], name='email_template_index'),
        ),
        migrations.AlterModelTable(
            name='customemail',
            table='nets_core_custom_email',
        ),
        migrations.AlterModelTable(
            name='emailnotification',
            table='nets_core_email_notification',
        ),
        migrations.AlterModelTable(
            name='emailtemplate',
            table='nets_core_email_template',
        ),
        migrations.AddField(
            model_name='permission',
            name='project_content_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='nets_core_permissions', to='contenttypes.contenttype'),
        ),
        migrations.AddField(
            model_name='role',
            name='permissions',
            field=models.ManyToManyField(related_name='roles', to='nets_core.permission'),
        ),
        migrations.AddField(
            model_name='role',
            name='project_content_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
        migrations.AddField(
            model_name='userrole',
            name='project_content_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
        migrations.AddField(
            model_name='userrole',
            name='role',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nets_core.role'),
        ),
        migrations.AddField(
            model_name='userrole',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddIndex(
            model_name='permission',
            index=models.Index(fields=['project_content_type', 'project_id'], name='permission_index'),
        ),
        migrations.AddIndex(
            model_name='role',
            index=models.Index(fields=['project_content_type', 'project_id'], name='role_index'),
        ),
    ]
