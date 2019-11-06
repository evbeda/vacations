from django.contrib.auth.models import Group
from vacations_app import STAFF_GROUP
from vacations_app.models import Team


def add_user_to_group(is_new, user, *args, **kwargs):
    if is_new and user.email in STAFF_GROUP:
        staff_group = Group.objects.get(name='staff')
        user.groups.add(staff_group)

    manager_group = Group.objects.get(name='manager')
    try:
        if (user.managed_team):
            user.groups.add(manager_group)
    except Team.DoesNotExist:
        manager_group.user_set.remove(user)

    return {
        'is_new': is_new,
        'user': user
    }
