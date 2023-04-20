from posts.models import Group


def groups(request):
    groups = Group.objects.all()
    return {'groups': groups}
