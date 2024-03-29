from django.contrib import admin
from django.http import HttpResponseRedirect
from django.utils import timezone

from .models import ConfigRequest, Formula, CloudProvider, ConfigRequestResult, LaunchHistory



# Register your models here.

def start_configuration(modeladmin, request, queryset):
    queryset.update(status='starting')
    modeladmin.message_user(request, "Initializing cloud... Estimated time ~ 2 minutes")
start_configuration.short_description = "Start selected configs"


class ConfigRequestResultInline(admin.StackedInline):
    model = ConfigRequestResult
    extra = 0
    readonly_fields = ['config_type', 'cores', 'ram_memory', 'storage_type', 'storage_size', 'per_hour_price', 'show_provider_icon']
    show_change_link = True

    fieldsets = (
        ('General', {
            'classes': ('wide', 'extrapretty'),
            'fields': ('show_provider_icon', 'config_type', 'per_hour_price',  )
        }),
        ('Hardware info', {
            'classes': ('wide', 'extrapretty'),
            'fields': ('storage_type', 'storage_size', 'cores', 'ram_memory', ),
        }),
    )


class ConfigRequestAdmin(admin.ModelAdmin):
    model = ConfigRequest
    inlines = [ConfigRequestResultInline, ]
    ordering = ['-created_at',]

    list_display = [
        'name',
        'user',
        'submitted',
        'software_type',
        'solver_type',
        'optimisation_target',
    ]
    list_filter = [
        'user',
    ]
    search_fields = [
        'user',
        'name',
    ]
    readonly_fields = [
        'user',
        'submitted',
        'software_type',
        'solver_type',
        'params',
        'optimisation_target'
    ]
    exclude = [
        'data',
        'created_at',
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


class FormulaAdmin(admin.ModelAdmin):
    model = Formula



class ConfigRequestResultAdmin(admin.ModelAdmin):
    model = ConfigRequestResult
    list_display = [
        'user',
        'request_name',
        'name',
        'config_type',
        'show_provider_icon'
    ]
    list_display_links = [
        'request_name',
        'name',
        'config_type',
        #'show_provider_icon'
    ]

    readonly_fields = [
        'show_provider_icon',
        'user',
        'config_request',
        'config_type',
        'cores',
        'ram_memory',
        'storage_type',
        'storage_size',
        'per_hour_price',
    ]
    exclude = [
        'data',
        'price_per_hour',
        'provider'
    ]

    change_form_template = 'cloudconfig/run_configs.html'

    actions = [start_configuration, ]

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
        'current_uptime',
        'current_price',
        'started_at',
        'finished_at',
    ]
    readonly_fields = [
        'provider',
        'get_machine_ip',
        'get_keyfile_url',
        'current_uptime',
        'current_price',
        'price_per_hour',
        'colored_status',
        'config_request',
        'config_request_result',
        'started_at',
        'finished_at',
    ]
    exclude = [
        'user',
        'total_price',
        'status',
        'jenkins_single_id',
        'machine_key',
        'machine_ip'
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

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['status'] = LaunchHistory.objects.get(pk=object_id).status
        return super().change_view(
            request, object_id, form_url, extra_context=extra_context,
        )


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