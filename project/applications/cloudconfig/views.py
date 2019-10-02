from django.http import HttpResponseRedirect
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
        messages.add_message(request, messages.INFO, 'Initializing cloud...')
        return HttpResponseRedirect(launch.get_admin_url())