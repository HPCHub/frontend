import re
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone
from django.views.generic import View
from .models import ConfigRequestResult, LaunchHistory
from django.contrib import messages

class StartConfig(View):
    def get(self, request, *args, **kwargs):
        pk = kwargs['pk']
        result = ConfigRequestResult.objects.get(pk=pk)
        if result.user != request.user:
            return HttpResponseRedirect('/')
        launch = LaunchHistory.objects.create(
            user=request.user,
            provider=result.provider,
            config_request=result.config_request,
            started_at=timezone.now(),
            config_request_result=result,
            status='starting'
        )
        messages.add_message(request, messages.INFO, 'Initializing cloud... Estimated time ~ 2 minutes')
        return HttpResponseRedirect(launch.get_admin_url())


class LaunchHistoryStatus(View):
    def get(self, request, *args, **kwargs):
        pk = kwargs['pk']
        result = LaunchHistory.objects.get(pk=pk)
        if result.user != request.user:
            return HttpResponseRedirect('/')
        return HttpResponse(result.status)


class GetKeyFile(View):
    def get(self, request, *args, **kwargs):
        pk = kwargs['pk']
        result = LaunchHistory.objects.get(pk=pk)
        if result.user != request.user:
            return HttpResponseRedirect('/')
        file_data = result.machine_key
        if result.config_request.name:
            cleared_name = re.sub('[^A-Za-z0-9]+', '_', result.config_request.name)
            filename = 'SSHkey_{}_{}'.format(
                cleared_name,
                (timezone.now() - timezone.timedelta(hours=7)).strftime('%Y_%m_%d_%H_%M')
            )
        else:
            filename = 'SSHkey_{}'.format(
                (timezone.now() - timezone.timedelta(hours=7)).strftime('%Y_%m_%d_%H_%M')
            )
        response = HttpResponse(file_data, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
        return response

