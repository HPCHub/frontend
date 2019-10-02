from django.contrib import admin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import ConfigRequest, Formula, CloudProvider, ConfigRequestResult, LaunchHistory



# Register your models here.

def start_configuration(modeladmin, request, queryset):
    queryset.update(status='starting')
    modeladmin.message_user(request, "Starting configuration")
start_configuration.short_description = "Start selected configs"


class ConfigRequestResultInline(admin.StackedInline):
    model = ConfigRequestResult
    extra = 0
    readonly_fields = ['config_type', 'cores', 'ram_memory', 'storage_type', 'storage_size', 'price_per_hour', 'provider']
    show_change_link = True
    actions = [start_configuration, ]

    fieldsets = (
        ('General', {
            'classes': ('wide', 'extrapretty'),
            'fields': ('config_type', 'price_per_hour', 'provider', )
        }),
        ('Hardware info', {
            'classes': ('wide', 'extrapretty'),
            'fields': (('storage_type', 'storage_size'), 'cores', 'ram_memory', ),
        }),
    )



"""
<QueryDict: 
{
'csrfmiddlewaretoken': ['FbKcOKdmggj0QZjKdirjHg4IbFvOyMuVuHNSPcnMirLfO5NfQCrGpIFqyM0OJeul'], 
'name': [''], 
'configrequestresult_set-TOTAL_FORMS': ['1'], 
'configrequestresult_set-INITIAL_FORMS': ['1'], 
'configrequestresult_set-MIN_NUM_FORMS': ['0'], 
'configrequestresult_set-MAX_NUM_FORMS': ['1000'], 
'configrequestresult_set-0-hashed_id': ['e4ab3840-1d2f-4e21-919a-2a2460f9d1c8'], 
'configrequestresult_set-0-config_request': ['d982711b-c044-41ae-a2a0-dd996e35feca'], 
'_run-configuration': ['Run Configuration'], 
'configrequestresult_set-__prefix__-hashed_id': [''], 
'configrequestresult_set-__prefix__-config_request': ['d982711b-c044-41ae-a2a0-dd996e35feca']
}
>

<QueryDict: {
'csrfmiddlewaretoken': ['PJDhlGnH7XtTu6LCrln1QAipTiTWQ3uIEfGXm8x798V8scf74Fnoy2T7gpoW1vu8'], 
'name': [''], 
'configrequestresult_set-TOTAL_FORMS': ['2'], 
'configrequestresult_set-INITIAL_FORMS': ['2'], 
'configrequestresult_set-MIN_NUM_FORMS': ['0'], 
'configrequestresult_set-MAX_NUM_FORMS': ['1000'], 
'configrequestresult_set-0-hashed_id': ['7e190047-b7fb-4ba7-9908-d2eeac08dd24'], 
'configrequestresult_set-0-config_request': ['d982711b-c044-41ae-a2a0-dd996e35feca'], 
'_run-configuration': ['Run Configuration'], 
'configrequestresult_set-1-hashed_id': ['e4ab3840-1d2f-4e21-919a-2a2460f9d1c8'], 
'configrequestresult_set-1-config_request': ['d982711b-c044-41ae-a2a0-dd996e35feca'], 
'configrequestresult_set-__prefix__-hashed_id': [''], 
'configrequestresult_set-__prefix__-config_request': ['d982711b-c044-41ae-a2a0-dd996e35feca']
}>

<QueryDict: {
'csrfmiddlewaretoken': ['ndmTfqErHMORbmKENDimkJQSQtQr0acdcJpzgSORJXg69se9qXiJ2brAdAlrbCcD'], 
'name': [''], 
'configrequestresult_set-TOTAL_FORMS': ['2'], 
'configrequestresult_set-INITIAL_FORMS': ['2'], 
'configrequestresult_set-MIN_NUM_FORMS': ['0'], 
'configrequestresult_set-MAX_NUM_FORMS': ['1000'],
'configrequestresult_set-0-hashed_id': ['7e190047-b7fb-4ba7-9908-d2eeac08dd24'],
'configrequestresult_set-0-config_request': ['d982711b-c044-41ae-a2a0-dd996e35feca'], 
'_run-configuration': ['Run Configuration'], 
'configrequestresult_set-1-hashed_id': ['e4ab3840-1d2f-4e21-919a-2a2460f9d1c8'], 
'configrequestresult_set-1-config_request': ['d982711b-c044-41ae-a2a0-dd996e35feca'], 
'configrequestresult_set-__prefix__-hashed_id': [''], 
'configrequestresult_set-__prefix__-config_request': ['d982711b-c044-41ae-a2a0-dd996e35feca']
}>
"""


class ConfigRequestAdmin(admin.ModelAdmin):
    model = ConfigRequest
    inlines = [ConfigRequestResultInline, ]
    list_display = [
        'user',
        'created_at',
        'software_type',
        'solver_type',
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
        'software_type',
        'solver_type',
    ]
    exclude = [
        'data',
    ]

    actions = [start_configuration, ]

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


class FormulaAdmin(admin.ModelAdmin):
    model = Formula



class ConfigRequestResultAdmin(admin.ModelAdmin):
    model = ConfigRequestResult

    readonly_fields = [
        'provider',
        'user',
        'config_request',
        'config_type',
        'cores',
        'ram_memory',
        'storage_type',
        'storage_size',
        'price_per_hour',
    ]
    exclude = [
        'data',
    ]

    change_form_template = 'cloudconfig/run_configs.html'

    def get_start_url(self, request, obj):
        return 'cloudconfig/start_config/{}/'.format(obj.pk)

    def response_change(self, request, obj):
        if "_run-configuration" in request.POST:
            self.message_user(request, "Starting configuration")
            launch = LaunchHistory.objects.create(
                user=request.user,
                provider=obj.provider,
                config_request=obj.config_request,
                started_at=timezone.now(),
                config_request_result=obj,
                status='starting'
            )
            return HttpResponseRedirect(launch.get_admin_url())
        return super().response_change(request, obj)

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super(ConfigRequestResultAdmin, self).get_queryset(request)
        else:
            qs = super(ConfigRequestResultAdmin, self).get_queryset(request)
            return qs.filter(user=request.user)


class LaunchHistoryAdmin(admin.ModelAdmin):
    model = LaunchHistory
    list_display = [
        'user',
        'config_request',
        'colored_status',
        'current_price',
        'started_at',
        'finished_at',
    ]
    readonly_fields = [
        'provider',
        'total_price',
        'colored_status',
        'current_price',
        'config_request',
        'config_request_result',
        'started_at',
        'finished_at',
    ]
    exclude = [
        'user',
        'status',
    ]
    list_filter = [
        'status',
    ]
    search_fields = [
        'user',
    ]
    list_display_links = [
        'user',
        'colored_status',
        'config_request'
    ]

    change_form_template = 'cloudconfig/kill_instance.html'

    def response_change(self, request, obj):
        if "_kill-instance" in request.POST:
            self.message_user(request, "Killing instance")
            obj.status = 'killed'
            obj.save()
            return HttpResponseRedirect(obj.get_admin_url())
        return super().response_change(request, obj)


    def get_queryset(self, request):
        if request.user.is_superuser:
            return super(LaunchHistoryAdmin, self).get_queryset(request)
        else:
            qs = super(LaunchHistoryAdmin, self).get_queryset(request)
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
        return super(LaunchHistoryAdmin, self).changelist_view(request)



admin.site.register(ConfigRequest, ConfigRequestAdmin)
admin.site.register(Formula, FormulaAdmin)
admin.site.register(CloudProvider)
admin.site.register(LaunchHistory, LaunchHistoryAdmin)
admin.site.register(ConfigRequestResult, ConfigRequestResultAdmin)