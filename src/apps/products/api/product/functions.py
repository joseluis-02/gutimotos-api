from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Q
from django.db import ProgrammingError
import logging

logger = logging.getLogger(__name__)

def safe_trigram_product_tabulator_search(queryset, search):
    if not search:
        return queryset
    return queryset.filter(
        Q(code__icontains=search) |
        Q(description__icontains=search) |
        Q(brand__name__icontains=search) |
        Q(category__description_sin__icontains=search)
    )
