from django.apps import AppConfig
from django.core.cache import cache
import json
import os
from django.conf import settings

class ConverterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'converter'

    def ready(self):
        # 開発環境では STATICFILES_DIRS から静的ファイルを読み込む
        static_dir = settings.STATICFILES_DIRS[0] if settings.STATICFILES_DIRS else settings.STATIC_ROOT

        # JSONファイルのパスを設定
        kanji_radicals_path = os.path.join(static_dir, 'jsons', 'kanji_radicals.json')
        replacement_map_path = os.path.join(static_dir, 'jsons', 'replacement_map.json')

        # JSONファイルを読み込んでキャッシュに保存
        try:
            with open(kanji_radicals_path, 'r', encoding='utf-8') as f:
                kanji_radicals = json.load(f)
                cache.set('kanji_radicals', kanji_radicals)
        except FileNotFoundError:
            print(f"Error: {kanji_radicals_path} not found.")
        
        try:
            with open(replacement_map_path, 'r', encoding='utf-8') as f:
                replacement_map = json.load(f)
                cache.set('replacement_map', replacement_map)
        except FileNotFoundError:
            print(f"Error: {replacement_map_path} not found.")
