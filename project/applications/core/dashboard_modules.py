from jet.dashboard.modules import DashboardModule

from hpcconfig.models import ConfigRequest


class RecentRequests(DashboardModule):

    title = 'Recent requests'
    template = 'core/recent_requests.html'
    limit = 10

    def init_with_context(self, context):
        self.column = 2
        self.children = ConfigRequest.objects.filter(user=context.request.user).order_by('-created_at')[:self.limit]
        if context.request.user.is_superuser:
            self.children = ConfigRequest.objects.order_by('-created_at')[:self.limit]