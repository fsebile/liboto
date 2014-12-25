from django.core.management.base import BaseCommand, CommandError
from main.models import Media, Author, Publisher
import tablib
from optparse import make_option


class Command(BaseCommand):
    help = 'Helper to import csv files\n' \
           'example usage:\n' \
           '$ python manage.py import_csv --filename ~/Workbook1.csv'

    option_list = BaseCommand.option_list + (
        make_option('-f', '--filename', nargs=1, type=str,
                    help='Give a csv file to import'),
    )

    def handle(self, *args, **options):
        if options.get('filename', False):
            t = tablib.Dataset()

            try:
                t.csv = open(options['filename']).read().decode(
                    errors="ignore")
            except IOError:
                self.stderr.write("File is missing", ending='\n')
                return

            hid = lambda x: t.headers.index(x)

            for row in t:
                a, a_new = Author.objects.get_or_create(
                    name=row[hid("author__name")])
                if a_new:
                    self.stdout.write("Saving Author: {}".format(a.name),
                                      ending='\n')
                else:
                    self.stdout.write("Author Exists: {}".format(a.name),
                                      ending='\n')

                p, p_new = Publisher.objects.get_or_create(
                    name=row[hid("publisher__name")])
                if p_new:
                    self.stdout.write("Saving Publisher: {}".format(p.name),
                                      ending='\n')
                else:
                    self.stdout.write("Publisher Exists: {}".format(p.name),
                                      ending='\n')

                if not Media.objects.filter(isbn=row[hid("isbn")]).exists():

                    m = Media(
                        author=a,
                        publisher=p,
                        isbn=row[hid("isbn")],
                        title=row[hid("title")],
                        year=row[hid("year")],
                        cover_image=row[hid("cover_image")],
                        description=row[hid("description")],
                    )
                    m.save()
                    self.stdout.write("Saving Media: {}".format(
                        m.title), ending='\n')
                else:
                    self.stdout.write("Media Exists: {}".format(
                        row[hid("title")]), ending='\n')

        else:
            raise CommandError("Please specify a csv file to import!\n"
                               "You can get help from this command\n"
                               "$ python manage.py import_csv --help")