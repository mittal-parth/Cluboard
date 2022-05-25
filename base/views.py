from django.shortcuts import render, redirect
from django.urls import reverse
from base.models import Club, Request, Item
from accounts.models import Permission_Assignment, Permission
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings

from base.forms import *
from accounts.forms import *

from math import ceil

# Functions to check user type and authorisation thereby


def can_user_access(user_id, club_id, action):
    user_permissions = ''
    try:
        user_permissions = Permission_Assignment.objects.get(
            club=club_id, user=user_id).role.permissions.all()
    except:
        Permission_Assignment.DoesNotExist
  
    if user_permissions:
        permissions_string = ""
        for permission in user_permissions:
            permissions_string += permission.actions + ","

        permissions_array = permissions_string.split(",")[:-1]
        if action in permissions_array:
            return True
    return False


def admin_check(user):
    return user.info.designation == 'Admin'


def convenor_check(user):
    return user.info.designation == 'Convenor'


def member_check(user):
    return user.info.designation == 'Member'


def admin_or_convenor_check(user):
    return (user.info.designation == 'Convenor' or user.info.designation == 'Admin')


@login_required(login_url='login')
# login_url is the page to be redirected to in case the function evaluates to false
def index(request):
    clubs = request.user.club_set.all()

    if request.user.is_superuser:
        clubs = Club.objects.all()

    context = {'clubs': clubs}
    return render(request, 'index.html', context)


@login_required(login_url='login')
@user_passes_test(member_check, login_url='error_page')
def index_member(request, pk):

    # Member should be able to view only their own club's items
    if request.user.club_set.first().id == pk:
        # Display all items belonging to that club as a carousel of cards
        club = Club.objects.get(id=pk)
        items = club.item_set.all()
        all_items = []
        n = len(items)
        nSlides = n//4 + ceil(n/4-n//4)  # logic for displaying slides
        all_items.append([items, range(1, nSlides), nSlides])

        # Display all requests made by that user
        reqs = request.user.request_set.all().order_by('-date_created')

        context = {'club': club, 'all_items': all_items, 'reqs': reqs}
        return render(request, 'index_member.html', context)
    else:
        return redirect('error_page')


@login_required(login_url='login')
@user_passes_test(admin_check, login_url='error_page')
def user_add(request, pk):
    club = Club.objects.get(id=pk)
    user_form = CreateUserForm()
    info_form = InfoForm()
    context = {'user_form': user_form, 'info_form': info_form, 'club': club}

    if request.method == 'POST':
        user_form = CreateUserForm(request.POST)
        info_form = InfoForm(request.POST)

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

            messages.success(
                request, f'Account was successfully created for {first_name} {last_name} and added to {club.club_name}!')
            return redirect(reverse('club_view', args=[pk]))
        else:
            messages.info(request, 'Error creating user')

    return render(request, 'user_add.html', context)


@login_required(login_url='login')
@user_passes_test(admin_check, login_url='error_page')
def user_delete(request, user_id):
    user = User.objects.get(id=user_id)
    club = user.club_set.first()
    user.delete()
    messages.info(request, 'User deleted successfully!')
    return redirect(reverse('club_view', args=[club.id]))


@login_required(login_url='login')
@user_passes_test(admin_check, login_url='error_page')
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
@user_passes_test(admin_or_convenor_check, login_url='error_page')
def club_view(request, pk):
    if can_user_access(request.user.id, pk, "club_view"):
        # Display all users belonging to that club
        club = Club.objects.get(id=pk)
        members = club.users.all()
        context = {'club': club, 'members': members}

        return render(request, 'club_view.html', context)
    else:
        return redirect('error_page')


@login_required(login_url='login')
# @user_passes_test(admin_or_convenor_check, login_url='error_page')
def item_add(request, pk):
    if can_user_access(request.user.id, pk,'item_add'):
        club = Club.objects.get(id=pk)
        initial = {'club': club}

        # Adding a new item
        form = ItemForm(initial=initial)
        form.fields['club'].queryset = Club.objects.filter(id=pk)
        if request.method == 'POST':
            form = ItemForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, 'Item added successfully!')
                return redirect(reverse('items_view', args=[pk]))
        context = {'club': club, 'form': form}
        return render(request, 'item_add.html', context)
    else:
        return redirect('error_page')


@login_required(login_url='login')
# @user_passes_test(admin_or_convenor_check, login_url='error_page')
def items_view(request, pk):
    if can_user_access(request.user.id, pk, 'items_view'):
        # Display all items belonging to that club as a carousel of cards
        club = Club.objects.get(id=pk)
        items = club.item_set.all()
        all_items = []
        n = len(items)
        nSlides = n//4 + ceil(n/4-n//4)  # logic for displaying slides
        all_items.append([items, range(1, nSlides), nSlides])

        # Display all requests pertaining to that club
        reqs = request.user.request_set.all().order_by('-date_created')

        if can_user_access(request.user.id, pk, 'request_approve'):
            reqs = club.request_set.all().order_by('-date_created')

        context = {'club': club, 'all_items': all_items, 'reqs': reqs}
        return render(request, 'items_view.html', context)
    else:
        return redirect('error_page')


@login_required(login_url='login')
# @user_passes_test(admin_or_convenor_check, login_url='error_page')
def item_update(request, pk, item_id):
    # Update an existing item
    if can_user_access(request.user.id, pk,'item_update'):
        item = Item.objects.get(id=item_id)
        club = Club.objects.get(id=pk)
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
# @user_passes_test(admin_or_convenor_check, login_url='error_page')
def item_delete(request, item_id):
    item = Item.objects.get(id=item_id)
    club_id = item.club.id
    if can_user_access(request.user.id, club_id,'item_delete'):
        item.delete()
        messages.info(request, 'Item deleted successfully!')
        return redirect(reverse('items_view', args=[club_id]))
    else:
        return redirect('error_page')

@login_required(login_url='login')
@user_passes_test(convenor_check, login_url='error_page')
def request_approve(request, request_id):
    # Approve the request if there is sufficient quantity available
    req = Request.objects.get(id=request_id)
    club_id = req.item.club.id
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


@login_required(login_url='login')
@user_passes_test(convenor_check, login_url='error_page')
def request_reject(request, request_id):
    req = Request.objects.get(id=request_id)
    club_id = req.item.club.id
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


@login_required(login_url='login')
@user_passes_test(member_check, login_url='error_page')
def request_add(request, pk):
    if request.user.club_set.first().id == pk:
        club = Club.objects.get(id=pk)

        # Pre-filling a form with required values
        initial = {'requested_by': request.user,
                   'club': club, 'status': 'Pending'}
        form = RequestForm(initial=initial)

        # Restrict what a member can choose from
        # Only see items pertaining to member's club
        form.fields['item'].queryset = Item.objects.filter(club=pk)
        form.fields['club'].queryset = Club.objects.filter(id=pk)
        form.fields['requested_by'].queryset = User.objects.filter(
            username=request.user)

        if request.method == 'POST':
            form = RequestForm(request.POST)

            # Data required to send mail
            requested_by = request.user.first_name + ' ' + request.user.last_name

            # Email of the convenor of the respective club
            convenors = User.objects.filter(
                info__designation='Convenor').filter(club__id=pk)
            emails_convenors = convenors.values_list('email')

            if form.is_valid():
                form.save()
                # Send email to the convenor about a new request
                try:
                    send_mail(
                        'InvManage',
                        f'There is a new request for an item by {requested_by}, member at {club.club_name}.',
                        settings.EMAIL_HOST_USER,
                        emails_convenors[0],
                        fail_silently=False,
                    )
                except:
                    messages.info(
                        request, 'The mail has not been sent. Please check your host connection.')
                return redirect(reverse('index_member', args=[pk]))
        context = {'club': club, 'form': form}
        return render(request, 'request_add.html', context)
    else:
        return redirect('error_page')


@login_required(login_url='login')
def error_page(request):
    return render(request, 'error_page.html')
