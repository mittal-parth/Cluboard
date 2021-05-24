from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render, redirect
from django.urls import reverse
# from django.contrib.auth.models import User
from accounts.models import Info

class MiddleWare(MiddlewareMixin):

    def process_view(self, request, view_func, view_args, view_kwargs):
        modulename = view_func.__module__
        user = request.user

        if user.is_authenticated:
            if user.info.designation == 'Admin':
                if modulename == 'base.views_admin':
                    pass
                elif modulename == 'base.views':
                    pass
                elif modulename == 'accounts.views':
                    pass
                else:
                    return redirect('/')
            elif user.info.designation == 'Convenor':
                if modulename == 'base.views_convenor':
                    pass
                elif modulename == 'base.views':
                    pass
                elif modulename == 'accounts.views':
                    pass
                else:
                    return redirect(reverse('items_view', args = [user.club_set.first().id]))
            elif user.info.designation == 'Member':
                if modulename == 'base.views_member':
                    pass
                elif modulename == 'accounts.views':
                    pass
                else:
                    return redirect(reverse('index_member', args = [user.club_set.first().id]))

        else:
            if request.path == reverse('login') or request.path == reverse('signup') or request.path == reverse('logout'):
                pass
            else:
                return redirect(reverse('login'))