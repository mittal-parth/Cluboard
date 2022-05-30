from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse
from base.models import Club, Request, Item
from accounts.models import Permission_Assignment, Role
from django.contrib.auth.models import User
from django.db.models import Count

from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings

from base.forms import *
from accounts.forms import *

from math import ceil

# Functions to check user type and authorisation thereby

# Function to check if user can access a view method
def can_user_access(user_id, action, club_id=None):
    user_permissions = ''
    if club_id:
        try:
            user_permissions = Permission_Assignment.objects.get(
                club=club_id, user=user_id).role.permissions.all()
        except:
            Permission_Assignment.DoesNotExist
    else:
        try:
            user_permissions = Permission_Assignment.objects.get(
                user=user_id).role.permissions.all()
        except:
            Permission_Assignment.DoesNotExist
    
    # Find permission in the permissions string of the
    # associated role
    if user_permissions:
        permissions_string = ""
        for permission in user_permissions:
            permissions_string += permission.actions + ","

        permissions_array = permissions_string.split(",")[:-1]
        if action in permissions_array:
            return True
    return False

# Function to check if a request is AJAX
def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


@login_required(login_url='login')
# login_url is the page to be redirected to in case the function evaluates to false
def index(request):
    clubs = request.user.club_set.all()

    if request.user.is_superuser:
        clubs = Club.objects.all()

    context = {'clubs': clubs}
    return render(request, 'index.html', context)


@login_required(login_url='login')
def user_add(request, club_id):
    if can_user_access(request.user.id, 'user_add', club_id):
        club = Club.objects.get(id=club_id)
        user_form = CreateUserForm()
        info_form = InfoForm()

        initial = {'club': club}
        permission_assignment_form = PermissionAssignmentForm(initial=initial)

        # Only current club should be displayed
        permission_assignment_form.fields['club'].queryset = Club.objects.filter(
            id=club_id)

        # Only non existing members should be displayed
        existing_club_users = club.users.all()
        permission_assignment_form.fields['user'].queryset = User.objects.exclude(
            id__in=[o.id for o in existing_club_users])

        context = {
            'user_form': user_form,
            'info_form': info_form,
            'club': club,
            'permission_assignment_form': permission_assignment_form
        }

        if request.method == 'POST':
            user_form = CreateUserForm(request.POST)
            info_form = InfoForm(request.POST)
            permission_assignment_form = PermissionAssignmentForm(request.POST)
            if user_form.is_valid():
                user_form.save()

                # Getting required data to display message
                first_name = user_form.cleaned_data.get('first_name')
                last_name = user_form.cleaned_data.get('last_name')
                username = user_form.cleaned_data.get('username')

                # Getting required data from info_form
                roll_no = request.POST['roll_no']
                user = User.objects.get(username=username)

                # Creating an Info object linked to this user
                user_info = Info(user=user, roll_no=roll_no)
                user_info.save()

                # Adding user to club
                club.users.add(user)

                # Assigning role to the user
                role_id = request.POST['role']
                role = Role.objects.get(id=role_id)
                permission_assignment = Permission_Assignment(
                    club=club, user=user, role=role)
                permission_assignment.save()

                messages.success(
                    request, f'Account was successfully created for {first_name} {last_name} and added to {club.club_name}!')
                return redirect(reverse('club_view', args=[club_id]))
            else:
                messages.info(request, 'Error creating user')

        return render(request, 'user_add.html', context)
    else:
        return render(request, 'error_page.html')


@login_required(login_url='login')
def existing_user_add(request, club_id):
    if can_user_access(request.user.id, 'user_add', club_id):
        club = Club.objects.get(id=club_id)
        form = PermissionAssignmentForm(request.POST)

        data = {}

        if is_ajax(request=request):
            if form.is_valid():
                form.save()
                user_id = request.POST['user']

                user = User.objects.get(id=user_id)
                club.users.add(user)
                name = user.first_name + " " + user.last_name
                data['name'] = name
                data['club'] = club.club_name
                data['status'] = 'ok'
                return JsonResponse(data)
            else:
                messages.info(request, 'Error adding user!')

        return render(request, 'error_page.html')


@login_required(login_url='login')
def user_delete(request, user_id):
    if can_user_access(request.user.id, 'user_delete'):
        user = User.objects.get(id=user_id)
        club = user.club_set.first()
        user.delete()
        messages.info(request, 'User deleted successfully!')
        return redirect(reverse('club_view', args=[club.id]))


@login_required(login_url='login')
def club_add(request):
    # Adding a new club
    form = ClubForm()
    if request.method == 'POST':
        form = ClubForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Club added successfully!')
            return redirect('/')
    context = {'form': form}
    return render(request, 'club_add.html', context)


@login_required(login_url='login')
def club_view(request, club_id):
    if can_user_access(request.user.id, "club_view", club_id):
        club = Club.objects.get(id=club_id)
        members = club.users.all()
        context = {'club': club, 'members': members}

        return render(request, 'club_view.html', context)
    else:
        return redirect('error_page')


@login_required(login_url='login')
def item_add(request, club_id):
    if can_user_access(request.user.id, 'item_add', club_id):
        club = Club.objects.get(id=club_id)
        initial = {'club': club}

        # Adding a new item
        form = ItemForm(initial=initial)
        form.fields['club'].queryset = Club.objects.filter(id=club_id)
        if request.method == 'POST':
            form = ItemForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, 'Item added successfully!')
                return redirect(reverse('items_view', args=[club_id]))
        context = {'club': club, 'form': form}
        return render(request, 'item_add.html', context)
    else:
        return redirect('error_page')


def view_all_requests(club):
    return club.request_set.all().order_by('-date_created')


@login_required(login_url='login')
def items_view(request, club_id):
    if can_user_access(request.user.id, 'items_view', club_id):
        # Display all items belonging to that club as a carousel of cards
        club = Club.objects.get(id=club_id)
        items = club.item_set.all()
        all_items = []
        n = len(items)
        nSlides = n//4 + ceil(n/4-n//4)  # logic for displaying slides
        all_items.append([items, range(1, nSlides), nSlides])

        # Display all requests pertaining to that club
        reqs = view_all_requests(club)

        if can_user_access(request.user.id, 'view_all_requests', club_id) == False:
            reqs = reqs.filter(requested_by=request.user.id)

        context = {'club': club, 'all_items': all_items, 'reqs': reqs}
        return render(request, 'items_view.html', context)
    else:
        return redirect('error_page')


@login_required(login_url='login')

def item_update(request, club_id, item_id):
    # Update an existing item
    if can_user_access(request.user.id, 'item_update', club_id):
        item = Item.objects.get(id=item_id)
        club = Club.objects.get(id=club_id)
        form = ItemForm(instance=item)
        form.fields['club'].queryset = Club.objects.filter(id=item.club.id)
        if request.method == 'POST':
            form = ItemForm(request.POST, request.FILES, instance=item)
            if form.is_valid():
                item.save()
                messages.success(request, 'Item updated successfully!')
                return redirect(reverse('items_view', args=[item.club.id]))

        context = {'club': club, 'form': form, 'item': item}
        return render(request, 'item_update.html', context)
    else:
        return redirect('error_page')


@login_required(login_url='login')
def item_delete(request, item_id):
    item = Item.objects.get(id=item_id)
    club_id = item.club.id
    if can_user_access(request.user.id, 'item_delete', club_id):
        item.delete()
        messages.info(request, 'Item deleted successfully!')
        return redirect(reverse('items_view', args=[club_id]))
    else:
        return redirect('error_page')


@login_required(login_url='login')
def request_approve(request, request_id):
    # Approve the request if there is sufficient quantity available
    req = Request.objects.get(id=request_id)
    club_id = req.item.club.id
    if can_user_access(request.user.id, 'request_approve', club_id):
        if req.item.qty - req.qty >= 0:
            req.item.qty -= req.qty
            req.status = 'Approved'
            req.item.save()
            req.save()

            # Email the user about the approval
            try:
                send_mail(
                    'InvManage',
                    f'Yay! Your request for {req.qty} {req.item.item_name} has been approved by the Convenor of {req.item.club.club_name}!',
                    settings.EMAIL_HOST_USER,
                    req.requested_by.email.split(),
                    fail_silently=False,
                )
            except:
                messages.info(
                    request, 'The mail has not been sent. Please check your host connection.')
            messages.success(request, 'Request approved successfully!')
            return redirect(reverse('items_view', args=[club_id]))
        else:
            messages.info(
                request, 'Request cannot be approved - Insufficient Quantity')
            return redirect(reverse('items_view', args=[club_id]))
    else:
        return redirect('error_page')


@login_required(login_url='login')
def request_reject(request, request_id):
    req = Request.objects.get(id=request_id)
    club_id = req.item.club.id
    if can_user_access(request.user.id, 'request_reject', club_id):
        req.status = 'Rejected'
        req.save()

        # Email the user about the denial
        try:
            send_mail(
                'InvManage',
                f'Sorry! Your request for {req.qty} {req.item.item_name} has been rejected by the Conevnor of {req.item.club.club_name}.',
                settings.EMAIL_HOST_USER,
                req.requested_by.email.split(),
                fail_silently=False,
            )
        except:
            messages.info(
                request, 'The mail has not been sent. Please check your host connection.')
        messages.info(request, 'Request rejected successfully!')
        return redirect(reverse('items_view', args=[club_id]))
    else:
        return redirect('error_page')


@login_required(login_url='login')
def request_add(request, club_id):
    if can_user_access(request.user.id, 'request_add', club_id):
        club = Club.objects.get(id=club_id)

        # Pre-filling a form with required values
        initial = {'requested_by': request.user,
                   'club': club, 'status': 'Pending'}
        form = RequestForm(initial=initial)

        # Restrict what a member can choose from
        # Only see items pertaining to member's club
        form.fields['item'].queryset = Item.objects.filter(club=club_id)
        form.fields['club'].queryset = Club.objects.filter(id=club_id)
        form.fields['requested_by'].queryset = User.objects.filter(
            username=request.user)

        if request.method == 'POST':
            form = RequestForm(request.POST)

            # Data required to send mail
            requested_by = request.user.first_name + ' ' + request.user.last_name

            # Email of the convenor of the respective club
            convenors = Permission_Assignment.objects.filter(
                club=club_id, role__name='convenor')
            convenors_emails = convenors.values_list('user__email', flat=True)

            if form.is_valid():
                form.save()
                # Send email to the convenor about a new request
                try:
                    send_mail(
                        'InvManage',
                        f'There is a new request for an item by {requested_by}, member at {club.club_name}.',
                        settings.EMAIL_HOST_USER,
                        convenors_emails,
                        fail_silently=False,
                    )
                except:
                    messages.info(
                        request, 'The mail has not been sent. Please check your host connection.')
                messages.success(request, 'Request created successfully!')
                return redirect(reverse('items_view', args=[club_id]))
        context = {'club': club, 'form': form}
        return render(request, 'request_add.html', context)
    else:
        return redirect('error_page')


@login_required(login_url='login')
def club_statistics(request, club_id):
    if can_user_access(request.user.id, 'club_statistics',club_id):
        club = Club.objects.get(id=club_id)

        items_list = club.item_set.all()
        club_requests = club.request_set.all()

        # Requests count grouped by item
        requests_count_by_item = list(club_requests.values('item').annotate(
            dcount=Count('item')).order_by().values_list('dcount', flat=True))

        status_choices = list(club_requests.values('status').annotate(
            dcount=Count('status')).order_by().values_list('status', flat=True))

        # Requests count grouped by status
        requests_count_by_status = list(club_requests.values('status').annotate(
            dcount=Count('status')).order_by().values_list('dcount', flat=True))

        context = {
            'items_list': items_list,
            'requests_count_by_item': requests_count_by_item,
            'status_choices': status_choices, 
            'requests_count_by_status': requests_count_by_status,
            'club':club,           
        }
        return render(request, 'club_statistics.html', context)
    else:
        return render(request, 'error_page.html')

@login_required(login_url='login')
def error_page(request):
    return render(request, 'error_page.html')
