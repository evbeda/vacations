from django.contrib.auth.models import Group


def add_user_to_group(is_new, user, *args, **kwargs):
    manager_group = Group.objects.get(name='manager')
    if user.managed_teams.exists():
        user.groups.add(manager_group)
    else:
        manager_group.user_set.remove(user)

    return {
        'is_new': is_new,
        'user': user
    }
