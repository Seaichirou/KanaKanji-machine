import os
from django.core.asgi import get_asgi_application
from starlette.staticfiles import StaticFiles
from starlette.routing import Mount
from pathlib import Path
from starlette.applications import Starlette
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kanji_to_kana_kanji_converter.settings')

# DjangoのASGIアプリケーションを取得
django_application = get_asgi_application()

# StaticFilesの設定
static_files = StaticFiles(directory=Path(settings.BASE_DIR, 'staticfiles'))

# MediaFilesの設定
media_files = StaticFiles(directory=Path(settings.MEDIA_ROOT))

# Starletteアプリケーションとして統合
application = Starlette(
    routes=[
        Mount('/static', static_files, name="static"),
        Mount('/media', media_files, name="media"),  # Media ファイルのマウント
        Mount('/', django_application),
    ]
)
