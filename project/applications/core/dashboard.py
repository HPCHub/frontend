from jet.dashboard import modules
from jet.dashboard.dashboard import Dashboard, AppIndexDashboard

from .dashboard_modules import RecentRequests, NewRequest, WalletBalance


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
                order=1
            )
        )
        self.children.append(
            WalletBalance(
                'Wallet',
                column=2,
                order=0
            )
        )






class CustomAppIndexDashboard(AppIndexDashboard):

    def init_with_context(self, context):

        self.children.append(modules.ModelList(
            title='Application models',
            models=self.models(),
            column=0,
            order=0
        ))

