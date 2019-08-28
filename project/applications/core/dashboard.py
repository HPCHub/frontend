from jet.dashboard import modules
from jet.dashboard.dashboard import Dashboard

from .dashboard_modules import RecentRequests, NewRequest


class CustomIndexDashboard(Dashboard):
    columns = 3

    def init_with_context(self, context):
        self.children.append(
            NewRequest(
                'New Request',
                column=0,
                order=0,
            )
        )
        self.children.append(modules.AppList(
            'Administration',
            exclude=('authtoken.*',),
            column=1,
            order=0
        ))

        self.children.append(
            RecentRequests(
                'Recent requests',
                column=2,
                order=0
            )
        )
