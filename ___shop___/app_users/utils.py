# from app_users.models import Profile
#
#
# def save_avatar(request: HttpRequest, input_file_name: str, profile: Profile, new_file_name: str) -> None:
#     logger.debug('Сохранение аватарки...')
#     if request.FILES:
#         logger.debug('Есть файл')
#         file: InMemoryUploadedFile = request.FILES[input_file_name]
#         file_name = file.name
#         file_ext = file_name[-3::]
#         request.FILES[input_file_name].name = f'{new_file_name}.{file_ext}'
#         profile.avatar_file.delete()
#         profile.avatar_file = request.FILES[input_file_name]
#         profile.save()
