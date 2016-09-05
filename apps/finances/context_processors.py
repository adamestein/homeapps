from .models import Bill


# noinspection PyUnusedLocal
def bill_states(request):
    return {
        'UNFUNDED': Bill.STATE_UNFUNDED,
        'UNPAID': Bill.STATE_UNPAID,
        'PAID': Bill.STATE_PAID
    }
