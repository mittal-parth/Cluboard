from django import template
register = template.Library()
    
from accounts.models import Permission_Assignment

@register.simple_tag
def user_role(user_id, club_id):
    return Permission_Assignment.objects.get(
            club=club_id, user=user_id).role.name.capitalize()