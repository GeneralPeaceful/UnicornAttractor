from decimal import Decimal
from django.shortcuts import get_object_or_404
from issuetracker.models import Ticket, Contribution


def cart(request):
    """
    Context for cross site cart rendering
    """
    cart = request.session.get('cart', {})
    cart_items = set()
    total = 0

    for ticket_id in cart.keys():
        ticket = get_object_or_404(Ticket, pk=ticket_id)
        ticket.contribution_amount = Decimal(
            cart[ticket_id]['contribution_amount'])
        total += ticket.contribution_amount
        cart_items.add(ticket)

    total_in_pence = total*100
    return {
        'cart_items': cart_items, 'total': total,
        'total_in_pence': total_in_pence}
