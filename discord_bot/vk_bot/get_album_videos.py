from vk_api import VkApi
from vk_api.utils import get_random_id


def main():
    vk_session = VkApi(
        token='vk1.a.qOyeTWq6q4NkdkKOStASFzWcFTIT_GFTgQP9rjqTWQ1zN3pTB-0dYhiRnxKSnthr_5543lXfcxvQmRhc0zH9w6PiZYWMUAAaSxtVKlXX2m4EsmCMH3FsRwzaOLKHGIf-YHJQFO_D_dBoZ5M3MvzWtzeONCKrjRNZ_IvMWTjLj46BcrbvzkIRQpOJi2QopX1yWUaZ_Cy__5wHWsYW_BpRLg')
    vk = vk_session.get_api()

    public_id = "-187263168"

    # Получите идентификатор паблика (owner_id) по короткому имени
    # Вызываем метод wall.get для получения первого поста со стены паблика
    response = vk.video.getAlbumById(owner_id=public_id, album_id="-1")

    # Проверяем, что запрос был успешным и есть посты на стене

    print(response)
    # if response['count'] > 0:
    #     # Получаем первый пост
    #     first_post = response['items'][0]
    #     print("Первый пост на стене паблика:")
    #     for i,j in first_post.items():
    #         print(i, j)
    #     print(type(first_post))
    # else:
    #     print("На стене нет постов.")


if __name__ == '__main__':
    main()
