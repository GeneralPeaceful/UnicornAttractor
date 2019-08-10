import stripe

from decimal import Decimal
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render, redirect, reverse, get_object_or_404
from issuetracker.models import Contribution
from issuetracker.views import Ticket

stripe_api_key = settings.STRIPE_SECRET

@login_required()
def view_cart(request):
    """
    View all the contributions saved up
    """
    num_contributions = Contribution.objects.filter(contributor_id=request.user.id).count()
    context = {
        'key': settings.STRIPE_PUBLISHABLE,
        'num_contributions': num_contributions
    }
    return render(request, "cart.html", context)

@login_required
def add_to_cart(request, featureid):
    """
    Add an amount to the cart for contributions to check out at a later time
    """
    if not request.POST['contribution_amount'] or request.POST['contribution_amount'] == '' or int(request.POST['contribution_amount']) < 1:
        messages.error(
            request, 'You must submit a valid contribution amount.')
        return redirect('feature'+featureid)

    cart = request.session.get('cart', {})
    if featureid not in cart:

        cart[featureid] = {
            'id': featureid,
            'contrib_amount': request.POST['contribution_amount']
        }

    else:

        messages.error(
            request, 'You\'re already contributing to this feature.')
        return redirect('feature'+featureid)

    request.session['cart'] = cart

    return redirect("cart")

@login_required
def remove_from_cart(request, featureid):
    """
    Delete a contribution from the cart
    """
    cart = request.session.get('cart', {})

    if featureid in cart:

        del cart[featureid]
        messages.success(request, "Feature contribution removed.")

    request.session['cart'] = cart

    return redirect(reverse('cart'))


@login_required
def charge(request):
    """
    Handle payment processing when user submits card details
    """
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        total_charge = 0

        for item in cart.keys():
            amount = cart[item]['contribution_amount']
            total_charge += Decimal(amount)

        try:
            payment = stripe.Charge.create(
                amount=int(total_charge * 100),
                currency='gbp',
                description='UA Feature Contribution',
                source=request.POST['stripeToken']
            )
        except stripe.error.CardError:
            messages.error(request, 'There was an error processing your payment.')

        if payment.paid:
            messages.error(request, "You have successfully paid. Please check the features page regularly to see when development begins.")
            request.session['cart'] = {}
            return redirect(reverse('features'))
        else:
            messages.error(request, 'Unable to take payment, please try again.')
    return redirect('features')


@login_required
def update_cart(request, featureid):
    """
    Update a a feature development contribution amount
    """
    cart = request.session.get('cart', {})

    if not request.POST['contribution_amount'] \
        or request.POST['contribution_amount'] == '' \
        or int(request.POST['contribution_amount']) < 1 \
        or float(request.POST['contribution_amount']) > 999.99:

        messages.error(request, 'You must submit a valid contribution amount, not exceeding £999.99')
        return redirect(reverse('cart'))

    if featureid in cart:
        cart[featureid]['contribution_amount'] = request.POST['contribution_amount']
        messages.success(request, "Cart updated successfully.")

    request.session['cart'] = cart
    return redirect(reverse('cart'))