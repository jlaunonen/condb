# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_person_allow_work_history_sharing'),
        ('auth', '0001_initial'),
        ('access', '0006_group_grant_active_until'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccessOrganizationMeta',
            fields=[
                ('organization', models.OneToOneField(primary_key=True, serialize=False, to='core.Organization', verbose_name='Organisaatio')),
                ('admin_group', models.ForeignKey(verbose_name='Yll\xe4pit\xe4j\xe4ryhm\xe4', to='auth.Group')),
            ],
            options={
                'verbose_name': 'P\xe4\xe4synvalvonnan asetukset',
            },
            bases=(models.Model, core.models.GroupManagementMixin),
        ),
    ]
