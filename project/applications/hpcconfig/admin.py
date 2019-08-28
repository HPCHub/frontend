from django.contrib import admin

from .models import ConfigRequest, Formula

# Register your models here.


class ConfigRequestAdmin(admin.ModelAdmin):
    model = ConfigRequest
    list_display = [
        'user',
        'created_at',
    ]
    list_filter = [
        'user',
    ]
    search_fields = [
        'user',
    ]
    readonly_fields = [
        'user',
        'created_at',
        'pretty_data',
    ]
    exclude = [
        'data',
    ]

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super(ConfigRequestAdmin, self).get_queryset(request)
        else:
            qs = super(ConfigRequestAdmin, self).get_queryset(request)
            return qs.filter(user=request.user)

    def preprocess_list_display(self, request):
        if 'user' not in self.list_display:
            self.list_display.insert(self.list_display.__len__(), 'user')
        if not request.user.is_superuser:
            if 'user' in self.list_display:
                self.list_display.remove('user')

    def preprocess_filter_fields(self, request):
        if 'user' not in self.list_filter:
            self.list_filter.insert(self.list_filter.__len__(), 'user')
        if not request.user.is_superuser:
            if 'user' in self.list_filter:
                self.list_filter.remove('user')

    def preprocess_search_fields(self, request):
        if 'user__username' not in self.search_fields:
            self.search_fields.insert(self.search_fields.__len__(), 'user__username')
        if not request.user.is_superuser:
            if 'user__username' in self.search_fields:
                self.search_fields.remove('user__username')

    def changelist_view(self, request, extra_context=None):
        self.preprocess_list_display(request)
        self.preprocess_search_fields(request)
        self.preprocess_filter_fields(request)
        return super(ConfigRequestAdmin, self).changelist_view(request)


admin.site.register(ConfigRequest, ConfigRequestAdmin)

admin.site.register(Formula)