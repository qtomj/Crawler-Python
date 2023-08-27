from jmcomic import create_option, JmcomicClient, JmcomicText

opfile = '../assets/config/option_workflow_download.yml'

option = create_option(opfile)
client: JmcomicClient = option.build_jm_client()

def get_env(name):
    import os
    value = os.getenv(name, None)
    if value is None or value == '':
        return None
    return value

def get_jm_album_ids():
    from common import str_to_set

    jm_albums = ""
    aid_set = set()
    for text in [
        jm_albums,
        (get_env('JM_ALBUM_IDS') or '').replace('-', '\n'),
    ]:
        print(text)
        aid_set.update(str_to_set(text))

    return aid_set

def download_by_url(album_id, url: str):
    photo_id = JmcomicText.parse_to_photo_id(url)  # 400222
    filename = url[url.rindex('/'):url.rindex('?')]  # 00001.webp
    default_save_dir = get_env('JM_DOWNLOAD_DIR')
    import os
    if not os.path.exists(f'{default_save_dir}{album_id}'):
        os.makedirs(f'{default_save_dir}{album_id}')
    client.download_image(
        img_url=url,
        img_save_path=f'{default_save_dir}{album_id}{filename}',
    )


if __name__ == '__main__':
    for album_id in get_jm_album_ids():
        urls = ['https://cdn-msp.jm-comic1.club/media/photos/{0}/{1}.webp?v=1692375790'.format(album_id, str(i).zfill(5)) for i in range(1, 150)]
        for url in urls:
            download_by_url(album_id, url)
