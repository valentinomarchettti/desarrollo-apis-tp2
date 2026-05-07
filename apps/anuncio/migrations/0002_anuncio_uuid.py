# Generated manually for TP5.

import uuid

from django.db import migrations, models


def populate_anuncio_uuids(apps, schema_editor):
    Anuncio = apps.get_model('anuncio', 'Anuncio')
    for anuncio in Anuncio.objects.filter(uuid__isnull=True):
        anuncio.uuid = uuid.uuid4()
        anuncio.save(update_fields=['uuid'])


class Migration(migrations.Migration):

    dependencies = [
        ('anuncio', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='anuncio',
            name='uuid',
            field=models.UUIDField(editable=False, null=True),
        ),
        migrations.RunPython(populate_anuncio_uuids, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='anuncio',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
