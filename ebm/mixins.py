import csv
import random
import string

from django.http import HttpResponse
from django.utils.text import slugify


class ExportCsvMixin:
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"


def random_string_generator(size=4, char=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(char) for _ in range(size))


def create_slug(instance, name=None, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(name)
    model = instance.__class__
    if model.objects.filter(slug=slug).exists():
        new_slug = "{slug}-{randstr}".format(
            slug=slug,
            randstr=random_string_generator(4)
        )
        return create_slug(instance, new_slug=new_slug)
    return slug
