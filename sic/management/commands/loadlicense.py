from django.core.management.base import BaseCommand
from ...models import License


class Command(BaseCommand):
    help = 'load a license'

    def handle(self, name, file, *args, **options):
        with open(file, 'r') as fd:
            text = fd.read()
            license = License(name=name, text=text,
                              under_discussion=False)
        license.save()
        print("Saved {name} as {hash}".format(
            name=license.name,
            hash=license.hash,
        ))
