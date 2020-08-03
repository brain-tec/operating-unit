# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from . import models
from . import report

from odoo.addons.account.models.account_payment \
    import account_payment as AccountPaymentOrig


def uninstall_hook(cr, registry):
    # If the method was patched we revert it during runtime
    if hasattr(AccountPaymentOrig._create_payment_entry, 'origin'):
        AccountPaymentOrig._revert_method('_create_payment_entry')
