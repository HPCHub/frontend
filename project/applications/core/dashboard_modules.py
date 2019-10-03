from jet.dashboard.modules import DashboardModule

from cloudconfig.models import ConfigRequest
from finances.models import Wallet, Transaction


class RecentRequests(DashboardModule):


    title = 'Recent requests'
    deletable = False
    template = 'core/recent_requests.html'
    limit = 10
    column = 2
    order = 2


    def init_with_context(self, context):
        self.children = ConfigRequest.objects.filter(user=context.request.user).order_by('-created_at')[:self.limit]
        if context.request.user.is_superuser:
            self.children = ConfigRequest.objects.order_by('-created_at')[:self.limit]


class WalletBalance(DashboardModule):


    title = 'Wallet'
    deletable = False
    template = 'core/wallet_balance.html'
    limit = 10
    column = 2
    order = 2


    def init_with_context(self, context):
        wallet = Wallet.objects.get(user=context.request.user)
        self.children = Transaction.objects.filter(from_wallet=wallet).union(Transaction.objects.filter(to_wallet=wallet))
        if context.request.user.is_superuser:
            wallet = Wallet.objects.get(user__username='admin')
            self.children = Transaction.objects.filter(from_wallet=wallet).union(Transaction.objects.filter(to_wallet=wallet))
        self.context.update({"wallet": wallet})


class NewRequest(DashboardModule):

    title = 'New request'
    deletable = False
    template = 'core/new_config.html'
    limit = 10
    column = 0
    order = 0
