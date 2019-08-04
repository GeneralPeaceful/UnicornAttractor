from decimal import Decimal
from django.db.models import Count, Sum
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Ticket, Contribution, Vote
from .forms import ReportBugForm, RequestFeatureForm, StaffReportBugForm, StaffRequestFeatureForm

def bugs(request):
    """
    List of all bug reports
    """
    all_bugs = Ticket.objects.filter(ticket_type='Bug').annotate(num_votes=Count('vote')).order_by('-num_votes')
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
    all_features = Ticket.objects.filter(ticket_type='Feature').order_by('-completion').annotate(total_contributions=Sum('contribution__amount'))
    context = {
        'features': all_features
    }
    return render(request, 'features.html', context)

def bug(request, bugid):
    """
    View the details of a specific bug
    """
    current_bug = get_object_or_404(Ticket, pk=bugid)
    votes = Vote.objects.all().filter(ticket=bugid).count()
    context = {
        'bug': current_bug,
        'votes': votes
    }
    return render(request, 'bug.html', context)


def feature(request, featureid):
    """
    View the details of a specific feature
    """
    current_feature = get_object_or_404(Ticket, pk=featureid)
    contributions = Contribution.objects.all().filter(ticket=featureid)
    contribution_amount = Decimal(0.00)
    for contribution in contributions:
        contribution_amount += contribution.amount
    current_feature.total_contributions = contribution_amount
    context = {
        'feature': current_feature,
    }
    return render(request, 'feature.html', context)

@login_required
def add_bug(request):
    """
    Report a bug
    """
    if request.method == "POST":
        form = ReportBugForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            ticket.ticket_type = "Bug"
            ticket.save()
            messages.success(request, 'Your bug has been reported successfully.')
            return redirect('bug', bugid=ticket.pk)
        return render(request, 'addbug.html', {'form': form})        
    form = ReportBugForm()
    return render(request, 'addbug.html', {'form': form})

@login_required
def add_feature(request):
    """
    Request a feature
    """
    if request.method == "POST":
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
            existing_vote = Vote.objects.all().filter(user=user, ticket=ticket).count()
            total_votes = Vote.objects.all().filter(ticket=ticket).count()
            if existing_vote > 0:
                return JsonResponse({
                    'status': 'Fail', 'msg': 'You have already upvoted this ticket!'
                })
            else:
                vote = Vote(user=user, ticket=ticket)
                vote.save()
                return JsonResponse({
                    'status': 'Success',
                    'msg': 'Upvoted!',
                    'numVotes': total_votes+1
                })
        except Ticket.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'The Ticket you are looking for does not exist.'})
    else:
        return JsonResponse({'status': 'Fail', 'msg': 'That is not a valid request.'})

@login_required
def edit_bug(request, bugid):
    """
    Edit a bug report
    """
    ticket = get_object_or_404(Ticket, pk=bugid)
    
    if request.user.is_staff:
        form = StaffReportBugForm(request.POST or None, request.FILES or None, instance=ticket)
    else:
        form = ReportBugForm(request.POST or None, request.FILES or None, instance=ticket)
        
    if form.is_valid():
        form.save()
        messages.success(request, 'Your changes have been saved.')
        return redirect('bug', bugid)
    return render(request, 'editbug.html', {'form': form, 'bugid': bugid})

@login_required
def edit_feature(request, featureid):
    """
    Edit a feature request
    """
    ticket = get_object_or_404(Ticket, pk=featureid)
    if request.user.is_staff:
        form = StaffRequestFeatureForm(request.POST or None, request.FILES or None, instance=ticket)
    else:
        form = RequestFeatureForm(request.POST or None, request.FILES or None, instance=ticket)
        
    if form.is_valid():
        form.save()
        messages.success(request, 'Your changes have been saved.')
        return redirect('feature', featureid)
    return render(request, 'editfeature.html', {'form': form, 'featureid': featureid})

def update_ticket_status(request, ticketid):
    """
    Asynchronously update the ticket status when a change is made to it
    """
    if request.method == 'POST' and request.is_ajax():
        try:
            current_bug = Ticket.objects.get(pk=ticketid)
            current_bug.status = request.POST['ticket_status']
            current_bug.save()
            return JsonResponse({'status': 'Success', 'msg': 'Status updated succesfully.'})
        except Ticket.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'The ticket you are looking for does not exist.'})
    else:
        return JsonResponse({'status': 'Fail', 'msg': 'That is not a valid request'})