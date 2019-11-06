from django.contrib.auth.models import Group
from vacations_app import STAFF_GROUP


def add_user_to_group(is_new, user, *args, **kwargs):
    if is_new and user.email in STAFF_GROUP:
        staff_group = Group.objects.get(name='staff')
        user.groups.add(staff_group)

    return {
        'is_new': is_new,
        'user': user
    }

