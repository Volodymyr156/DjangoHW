import os
import django

os.environ.setdefault("DJANGO.SETTINGS.MODULE", "core.settings")
django.setup()



from django.db.models import(
    Count,
    Min,
    Max,
    Sum,
    Avg
)


books_count = Book