# dbindexes.py:

from inventory.models import Item
from dbindexer.lookups import StandardLookup
from dbindexer.api import register_index

register_index(Item, {'user__username': (StandardLookup(), 'iexact'),
})