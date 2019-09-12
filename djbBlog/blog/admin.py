from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """The parent class we inherited include all admin options & func for a given model,
    what we need to do is to replace/customize our own desired stuff
    """
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author')  # leftmost filter on the admin
    search_fields = ('title', 'body')
    prepopulated_fields = { 'slug': ('title',) }

    # a list of fields u wanna change into a <select-box> interface
    # for either a ForeignKey or ManyToManyField
    raw_id_fields = ('author',)

    date_hierarchy = 'publish'  # behaves like filters I'd say (below the search bar)
    ordering = ('status', 'publish')  # default ordering rule
