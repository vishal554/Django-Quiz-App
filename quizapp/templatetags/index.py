from django import template
register = template.Library()

# Creating a custom ForLoop Indexer to loop through in Django Templates
@register.filter
def index(indexable, i):
    return indexable[i]