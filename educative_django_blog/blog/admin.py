import csv
from datetime import datetime, timedelta

from django.contrib import admin
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from django.utils.html import format_html

from blog.models import Post


class BlogStatusListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'Blog status'
    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('Published', ('Published blog')),
            ('Unpublished', ('Unpublished blog')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value() == 'Published':
            return queryset.filter(status='published')
        if self.value() == 'Unpublished':
            return queryset.filter(status='draft')


class PostAdmin(admin.ModelAdmin):
    @admin.display(description='Name', empty_value='N/A')
    def author_full_name(self, obj):
        return "%s %s" % (obj.author.first_name, obj.author.last_name)

    def is_recently_created(self, obj):
        return abs((datetime.now().date() - obj.created.date()).days) >= 7

    @admin.action(permissions=['change'])
    def publish_blog(modeladmin, request, queryset):
        queryset.update(publish=timezone.now() - timedelta(days=1), status='published')

    def export_to_csv(modeladmin, request, queryset):
        opts = modeladmin.model._meta
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; \
            filename={}.csv'.format(opts.verbose_name)
        writer = csv.writer(response)
        fields = [field for field in opts.get_fields()
                  if not field.many_to_many and not field.one_to_many]
        # Write a first row with header information
        writer.writerow([field.verbose_name for field in fields])
        # Write data rows
        for obj in queryset:
            data_row = []
            for field in fields:
                value = getattr(obj, field.name)
                if isinstance(value, datetime):
                    value = value.strftime('%d/%m/%Y %H:%M:%S')
                data_row.append(value)
            writer.writerow(data_row)
        return response

    def make_draft_using_secondary_page(self, request, queryset):
        if 'apply' in request.POST:
            # # Perform our update action:
            queryset.update(status='draft')
            # Redirect to our admin view after our update has
            # completed with a nice little info message saying
            # our models have been updated:
            self.message_user(request,
                              "Changed to DRAFT on {} post".format(queryset.count()))
            return HttpResponseRedirect(request.get_full_path())

        return render(request, 'admin/make_draft.html', context={'posts': queryset})

    def marked_blog_status(self, obj):
        if obj.status == "draft":
            return format_html('<span style="color: #{};">{}</span>', "F6CC0A", obj.status.title(), )
        return format_html('<span style="color: #{};">{}</span>', "12B873", obj.status.title(), )

    fieldsets = [
        ("Basic", {'fields': ['title', 'body', 'status', ]}),
        ("Author", {'fields': ['author', 'published_by', ]}),
        ("Date", {
            'classes': ('collapse',),
            'fields': ['publish', ]
        }),
    ]
    list_display = (
        'id', 'title', 'marked_blog_status', 'author', 'author_full_name', 'created', 'publish', 'views_count',
        'is_recently_created',
    )
    list_display_links = ('id', 'author',)
    list_editable = ('title',)
    ordering = ('-created', 'publish',)
    date_hierarchy = 'publish'
    admin.site.empty_value_display = 'Not available'
    save_on_top = True
    list_filter = (BlogStatusListFilter, 'author',)
    search_fields = ('title', 'author__username', 'status',)
    list_select_related = ('author',)
    autocomplete_fields = ['author', ]
    raw_id_fields = ['published_by', ]
    radio_fields = {"status": admin.VERTICAL}
    readonly_fields = ('author',)
    actions = [publish_blog, export_to_csv, make_draft_using_secondary_page]

    is_recently_created.boolean = True
    publish_blog.short_description = "Mark selected blog as published"
    export_to_csv.short_description = 'Export to CSV'


admin.site.register(Post, PostAdmin)
