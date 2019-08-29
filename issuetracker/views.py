from comments.models import Comment
from decimal import Decimal
from django.db.models import Count, Sum
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Ticket, Contribution, Vote
from .forms import (
    ReportBugForm, RequestFeatureForm,
    StaffReportBugForm, StaffRequestFeatureForm)


def bugs(request):
    """
    List of all bug reports
    """
    all_bugs = Ticket.objects.filter(ticket_type='Bug').annotate(
        num_votes=Count('vote')).order_by('-num_votes')
    for bug in all_bugs:
        bug.num_votes = Vote.objects.all().filter(ticket=bug.pk).count()

    context = {
        'bugs': all_bugs
    }
    return render(request, 'bugs.html', context)


def features(request):
    """
    List of all feature requests
    """
    all_features = Ticket.objects.filter(ticket_type='Feature').order_by(
        '-completion').annotate(
            total_contributions=Sum('contribution__amount'))
    for feature in all_features:
        contributions = Contribution.objects.all().filter(ticket=feature)
        contribution_amount = Decimal(0.00)
        for contribution in contributions:
            contribution_amount += contribution.amount

        feature.total_contributions = contribution_amount
        feature.completion = feature.total_contributions/feature.price*100

    context = {
        'features': all_features
    }
    return render(request, 'features.html', context)


def bug(request, bugid):
    """
    View the details of a specific bug
    """
    user = request.user
    if user.is_authenticated:
        if request.method == "POST":
            user = request.user
            comment = request.POST['comment']
            ticket = get_object_or_404(Ticket, pk=bugid)
            if comment.strip() == '':
                messages.error(request, 'Comment message is required.')
                return redirect('bug', bugid=ticket.pk)

            comment = Comment(user=user, comment=comment, ticket=ticket)
            comment.save()
            messages.success(request, 'Thanks for your comment.')
            return redirect('bug', bugid=ticket.pk)

    current_bug = get_object_or_404(Ticket, pk=bugid)
    comments = Comment.objects.all().filter(ticket=bugid)
    votes = Vote.objects.all().filter(ticket=bugid).count()
    context = {
        'bug': current_bug,
        'comments': comments,
        'votes': votes
    }
    return render(request, 'bug.html', context)


def feature(request, featureid):
    """
    View the details of a specific feature
    """
    user = request.user
    if user.is_authenticated:
        if request.method == "POST":
            user = request.user
            comment = request.POST['comment']
            ticket = get_object_or_404(Ticket, pk=featureid)
            if comment.strip() == '':
                messages.error(request, 'Comment message is required.')
                return redirect('feature', featureid=ticket.pk)

            comment = Comment(user=user, comment=comment, ticket=ticket)
            comment.save()
            messages.success(request, 'Thanks for your comment.')
            return redirect('feature', featureid=ticket.pk)

    current_feature = get_object_or_404(Ticket, pk=featureid)
    comments = Comment.objects.all().filter(ticket=featureid)
    contributions = Contribution.objects.all().filter(ticket=featureid)
    contribution_amount = Decimal(0.00)
    unique_contributors = []
    votes = 0

    for contribution in contributions:
        contribution_amount += contribution.amount
        if contribution.user not in unique_contributors:
            unique_contributors.append(contribution.user)
            votes += 1

    current_feature.total_contributions = contribution_amount
    current_feature.completion = (
        current_feature.total_contributions /
        current_feature.price * 100)
    context = {
        'feature': current_feature,
        'comments': comments,
        'votes': votes,
    }
    return render(request, 'feature.html', context)


@login_required
def add_bug(request):
    """
    Display the correct form to allow a user to create a bug report
    """
    if request.method == "POST":
        if request.user.is_authenticated:
            form = StaffReportBugForm(request.POST)
        else:
            form = ReportBugForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            ticket.ticket_type = "Bug"
            ticket.save()
            messages.success(
                request,
                'Your bug has been reported successfully.')
            return redirect('bug', bugid=ticket.pk)

        return render(request, 'addbug.html', {'form': form})

    if request.user.is_authenticated:
        form = StaffReportBugForm()
    else:
        form = ReportBugForm()
    return render(request, 'addbug.html', {'form': form})


@login_required
def add_feature(request):
    """
    Display the correct form to allow a user to create a feature request
    """
    if request.method == "POST":
        if request.user.is_staff:
            form = StaffRequestFeatureForm(request.POST)
        else:
            form = RequestFeatureForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            ticket.ticket_type = "Feature"
            ticket.save()
            messages.success(
                request, 'Your feature has been requested successfully.')
            return redirect('feature', featureid=ticket.pk)

        return render(request, 'addfeature.html', {'form': form})

    if request.user.is_staff:
        form = StaffRequestFeatureForm()
    else:
        form = RequestFeatureForm()
    return render(request, 'addfeature.html', {'form': form})


@login_required
def add_vote(request, bugid):
    """
    Asynchronous handler for upvoting bugs
    """
    if request.method == 'POST' and request.is_ajax():
        try:
            user = request.user
            ticket = get_object_or_404(Ticket, pk=bugid)
            existing_vote = Vote.objects.all().filter(
                user=user, ticket=ticket).count()
            total_votes = Vote.objects.all().filter(ticket=ticket).count()
            if existing_vote > 0:
                return JsonResponse({
                    'status': 'Fail',
                    'msg': 'You have already voted on this ticket!'
                })
            else:
                vote = Vote(user=user, ticket=ticket)
                vote.save()
                return JsonResponse({
                    'status': 'Success',
                    'msg': 'Vote successful.',
                    'numVotes': total_votes+1
                })
        except Ticket.DoesNotExist:
            return JsonResponse({
                'status': 'Fail',
                'msg': 'The Ticket you are looking for does not exist.'})
    else:
        return JsonResponse({
            'status': 'Fail',
            'msg': 'That is not a valid request.'})


@login_required
def edit_bug(request, bugid):
    """
    Display the correct form to allow a user to edit a bug report
    """
    ticket = get_object_or_404(Ticket, pk=bugid)
    if request.user.is_staff:
        form = StaffReportBugForm(
            request.POST or None,
            request.FILES or None,
            instance=ticket)
    elif request.user == ticket.created_by:
        form = ReportBugForm(
            request.POST or None,
            request.FILES or None,
            instance=ticket)
    else:
        messages.error(
            request,
            "You cannot edit this bug as you are not its creator.")
        return redirect('bug', bugid=ticket.pk)
    if form.is_valid():
        form.save()
        messages.success(request, 'Your changes have been saved.')
        return redirect('bug', bugid)

    return render(request, 'editbug.html', {'form': form, 'bugid': bugid})


@login_required
def edit_feature(request, featureid):
    """
    Display the correct form to allow a user to edit a feature request
    """
    ticket = get_object_or_404(Ticket, pk=featureid)
    if request.user.is_staff:
        form = StaffRequestFeatureForm(
            request.POST or None,
            request.FILES or None,
            instance=ticket)
    elif request.user == ticket.created_by:
        form = RequestFeatureForm(
            request.POST or None,
            request.FILES or None,
            instance=ticket)
    else:
        messages.error(
            request,
            "You cannot edit this feature as you are not the one who " +
            "requested it.")
        return redirect('feature', featureid=ticket.pk)
    if form.is_valid():
        form.save()
        messages.success(request, 'Your changes have been saved.')
        return redirect('feature', featureid)

    return render(request, 'editfeature.html', {
        'form': form, 'featureid': featureid})
