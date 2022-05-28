from django import template
register = template.Library()
    
from accounts.models import Permission_Assignment
  
@register.simple_tag
def can_user_access(user_id, action, club_id = None):
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

    if user_permissions:
        permissions_string = ""
        for permission in user_permissions:
            permissions_string += permission.actions + ","
        permissions_array = permissions_string.split(",")[:-1]
        if action in permissions_array:
            return True
    return False

