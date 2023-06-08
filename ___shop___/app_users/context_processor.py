from django.http import HttpRequest


def users_context(request: HttpRequest):
    response = dict()
    # if request.user.is_authenticated:
    #     try:
    #         profile, is_create = Profile.objects.get_or_create(user=request.user)
    #     except OperationalError:
    #         pass
    #     else:
    #         response['profile'] = profile
    #
    return response
