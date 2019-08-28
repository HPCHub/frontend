from jet.dashboard import modules
from jet.dashboard.dashboard import Dashboard

from .dashboard_modules import RecentRequests
class CustomIndexDashboard(Dashboard):
    columns = 3

    def init_with_context(self, context):
        if isinstance(context, dict):
            user_id = context.get('request').user.id
        else:
            user_id = context.request.user.id

        self.children.append(modules.LinkList(
            'Quick links',
            children=[
                {
                    'title': 'Request new configuration',
                    'url': 'https://ptchk.typeform.com/to/To9Fp9?id={}'.format(user_id),
                    'external': True,
                },
            ],
            column=0,
            order=0,
        ))

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
