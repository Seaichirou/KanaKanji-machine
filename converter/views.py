import os
import json
import re
from django.shortcuts import render
from django.conf import settings
from PIL import Image, ImageDraw, ImageFont
from django.core.cache import cache
from .forms import KanaKanjiForm
from django.utils import timezone

KANA_KANJI_PATTERN = re.compile(r'([一-龠々ヶ]{1,2})([ｦ-ﾟヰヱヽヾ･]+)')

def load_kanji_radicals(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_kanji_radicals():
    kanji_radicals = cache.get('kanji_radicals')
    # 開発環境では STATICFILES_DIRS から静的ファイルを読み込む
    static_dir = settings.STATICFILES_DIRS[0] if settings.STATICFILES_DIRS else settings.STATIC_ROOT
    if kanji_radicals is None:
        KANJI_RADICALS_PATH = os.path.join(static_dir, 'jsons', 'kanji_radicals.json')
        try:
            kanji_radicals = load_kanji_radicals(KANJI_RADICALS_PATH)
            cache.set('kanji_radicals', kanji_radicals)
        except Exception as e:
            raise ValueError("kanji_radicals cache is empty and failed to load from file")
    return kanji_radicals

kanji_to_radical = get_kanji_radicals()

def get_replacement_map():
    replacement_map = cache.get('replacement_map')
    static_dir = settings.STATICFILES_DIRS[0] if settings.STATICFILES_DIRS else settings.STATIC_ROOT
    if replacement_map is None:
        REPLACEMENT_MAP_PATH = os.path.join(static_dir, 'jsons', 'replacement_map.json')
        try:
            replacement_map = load_replacement_map(REPLACEMENT_MAP_PATH)
            cache.set('replacement_map', replacement_map)
        except Exception as e:
            raise ValueError("replacement_map cache is empty and failed to load from file")
    return replacement_map

def hankaku_to_zenkaku(text):
    conversion_map = {
        'ｳﾞ': 'ヴ', 'ｶﾞ': 'ガ', 'ｷﾞ': 'ギ', 'ｸﾞ': 'グ', 'ｹﾞ': 'ゲ', 'ｺﾞ': 'ゴ',
        'ｻﾞ': 'ザ', 'ｼﾞ': 'ジ', 'ｽﾞ': 'ズ', 'ｾﾞ': 'ゼ', 'ｿﾞ': 'ゾ', 'ﾀﾞ': 'ダ',
        'ﾁﾞ': 'ヂ', 'ﾂﾞ': 'ヅ', 'ﾃﾞ': 'デ', 'ﾄﾞ': 'ド', 'ﾊﾞ': 'バ', 'ﾋﾞ': 'ビ',
        'ﾌﾞ': 'ブ', 'ﾍﾞ': 'ベ', 'ﾎﾞ': 'ボ', 'ﾊﾟ': 'パ', 'ﾋﾟ': 'ピ', 'ﾌﾟ': 'プ',
        'ﾍﾟ': 'ペ', 'ﾎﾟ': 'ポ'
    }
    basic_map = str.maketrans(
        'ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜｦﾝ'
        'ｧｨｩｪｫｬｭｮｯｰ･'
        'ヰヱヽヾ',
        'アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン'
        'ァィゥェォャュョッー・'
        'ヰヱヽヾ'
    )

    result = []
    i = 0
    while i < len(text):
        if i + 1 < len(text) and text[i:i+2] in conversion_map:
            result.append(conversion_map[text[i:i+2]])
            i += 2
        else:
            char = text[i]
            if char == '･':
                result.append('・')
            else:
                result.append(char.translate(basic_map))
            i += 1

    return ''.join(result)

def extract_unique_matches(text):
    matches = KANA_KANJI_PATTERN.findall(text)
    
    unique_matches = []
    remaining_text = text
    
    for match in matches:
        combined_text = ''.join(match)
        if combined_text not in unique_matches:
            unique_matches.append(combined_text)
            remaining_text = remaining_text.replace(combined_text, '', 1)
    
    return unique_matches, remaining_text

def generate_kana_kanji_image(text, default_font_path, output_image_path, background_image_path=None):
    
        # 縦書き用にテキストを置き換え
        text = replace_for_vertical_writing(text)

        image = Image.new('RGBA', (615, 1150), (255, 255, 255, 0))

        # 背景画像の指定(画像サイズは「image」と合わせる)
        static_dir = settings.STATICFILES_DIRS[0] if settings.STATICFILES_DIRS else settings.STATIC_ROOT
        background_image_path = os.path.join(static_dir, 'images', 'kana_kanji_kana.png')

        if background_image_path:
            background_image = Image.open(background_image_path).resize((615, 1150))
            image.paste(background_image, (0, 0))

        draw = ImageDraw.Draw(image)
            
        try:
            default_font = ImageFont.truetype(default_font_path, 30)
        except IOError:
            print("Error loading default_font")
            return None  # フォントのロードに失敗した場合はここで処理を終了
        busyu_size = ImageFont.truetype(default_font_path, 25)
        # 開発環境では STATICFILES_DIRS から静的ファイルを読み込む
        static_dir = settings.STATICFILES_DIRS[0] if settings.STATICFILES_DIRS else settings.STATIC_ROOT
        kana_size_3counts = ImageFont.truetype(os.path.join(static_dir, 'fonts', 'jia-ming-han-zi-nojia-ming-mini-saizu.ttf'), 30)
        kana_size_6counts = ImageFont.truetype(os.path.join(static_dir, 'fonts', 'jia-ming-han-zi-nojia-ming-mini-saizu.ttf'), 26)

        x_offset = 550  # 右から左に描画するための開始位置
        y_offset = 10  # 開始する垂直位置
        line_height = 40  # 部首間の垂直距離
        max_line_height = 780  # 行送りのための最大高さ

        lines = text.splitlines()
        current_x_offset = x_offset
        current_y_offset = y_offset

        for line in lines:
            while line:
                match = KANA_KANJI_PATTERN.search(line)
                if match:
                    start, end = match.span()
                    for char in line[:start]:
                        draw.text((current_x_offset, current_y_offset), char, font=default_font, fill='black')
                        current_y_offset += line_height
                        if current_y_offset > max_line_height:
                            current_x_offset -= 70
                            current_y_offset = 10

                    radical_compound, kana = match.groups()
                    kana = hankaku_to_zenkaku(kana)
                    radicals = [kanji_to_radical.get(kanji, kanji) for kanji in radical_compound]
                    radical_compound_converted = ''.join(radicals)
                    
                    # 部首の設定
                    for radical in radical_compound_converted:
                        draw.text((current_x_offset - 9, current_y_offset + 10), radical, font=busyu_size, fill='black')
                        current_y_offset += line_height - 10
                    current_y_offset += 10

                    # 仮名の設定
                    kana_x_offset = current_x_offset + 25
                    kana_y_offset = current_y_offset - line_height - 30
                    if len(radical_compound_converted) == 1 and len(kana) > 3:
                        kana_y_offset -= -30  # 部首が1つで仮名が3つ以上の場合の位置調整
                        for i in range(0, len(kana), 3):
                            line_segment = kana[i:i + 3]
                            for j, k in enumerate(line_segment):
                                draw.text((kana_x_offset - 9 + (j * 13), kana_y_offset + 12), k, font=kana_size_6counts, fill='black')
                            kana_y_offset += 30  # 2段目の部首の間隔
                        current_y_offset = kana_y_offset + 10  # Adjust the current_y_offset after processing kana
                    else:
                        if len(kana) <= 3:
                            for i, k in enumerate(kana):
                                draw.text((kana_x_offset - 9 + (i * 15), kana_y_offset + 40), k, font=kana_size_3counts, fill='black')
                            current_y_offset += 5  # Adjust the current_y_offset for kana less than or equal to 3
                        else:
                            for i in range(0, len(kana), 3):
                                line_segment = kana[i:i + 3]
                                for j, k in enumerate(line_segment):
                                    draw.text((kana_x_offset - 9 + (j * 13), kana_y_offset + 12), k, font=kana_size_6counts, fill='black')
                                kana_y_offset += 30  # 2段目の部首の間隔
                            current_y_offset = kana_y_offset + 10  # Adjust the current_y_offset after processing kana

                    if current_y_offset > max_line_height:
                        current_x_offset -= 70
                        current_y_offset = 10

                    line = line[end:]
                else:
                    for char in line:
                        draw.text((current_x_offset, current_y_offset), char, font=default_font, fill='black')
                        current_y_offset += line_height
                        if current_y_offset > max_line_height:
                            current_x_offset -= 70
                            current_y_offset = 10
                    line = ""

            # 改行処理
            current_x_offset -= 70
            current_y_offset = 10


        image.save(output_image_path)
        
        # タイムスタンプを追加してキャッシュを回避
        timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
        return os.path.join(settings.MEDIA_URL, 'output.png') + f'?{timestamp}'
    

def replace_for_vertical_writing(text):
    replacement_map = get_replacement_map()
    for original, replacement in replacement_map.items():
        text = text.replace(original, replacement)

    vertical_text = ""
    for char in text:
        if 'A' <= char <= 'Z' or 'a' <= char <= 'z' or '0' <= char <= '9':
            vertical_text += char + '\u030A'  # Combining Ring Aboveを使用して縦中横にする
        else:
            vertical_text += char
    
    return vertical_text

def convert_to_kana_kanji(text):                  
    converted_text = text
    for kanji_compound, kana in KANA_KANJI_PATTERN.findall(text):
        radicals = [kanji_to_radical.get(kanji, kanji) for kanji in kanji_compound]
        radical_compound = ''.join(radicals)
        kana_without_markers = kana.replace('･', '')
        converted_text = converted_text.replace(f'{kanji_compound}{kana}', f'{radical_compound}{kana_without_markers}', 1)
    return converted_text

def load_replacement_map(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def kana_kanji_converter(request):
    form = KanaKanjiForm()
    converted_text = None
    image_path = None

    # キャッシュからデータを取得
    replacement_map = cache.get('replacement_map')
    kanji_to_radical = cache.get('kanji_radicals')

    # キャッシュがない場合の再読み込み処理
        
    if replacement_map is None or kanji_to_radical is None:

        # ファイルパスの設定
        # 開発環境では STATICFILES_DIRS から静的ファイルを読み込む
        static_dir = settings.STATICFILES_DIRS[0] if settings.STATICFILES_DIRS else settings.STATIC_ROOT
        KANJI_RADICALS_PATH = os.path.join(static_dir, 'jsons', 'kanji_radicals.json')
        REPLACEMENT_MAP_PATH = os.path.join(static_dir, 'jsons', 'replacement_map.json')

        try:
            replacement_map = load_replacement_map(REPLACEMENT_MAP_PATH)
            cache.set('replacement_map', replacement_map)
        except Exception as e:
            print(f"Error reloading replacement_map: {e}")
        
        try:
            kanji_to_radical = load_kanji_radicals(KANJI_RADICALS_PATH)
            cache.set('kanji_radicals', kanji_to_radical)
        except Exception as e:
            print(f"Error reloading kanji_radicals: {e}")

    if request.method == 'POST':
        form = KanaKanjiForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']

            # ゼロ幅スペースを取り除く
            text_for_image = text.replace('\u200B', '')

            background_image_name = request.POST.get('background_image')

            # 開発環境では STATICFILES_DIRS から静的ファイルを読み込む
            static_dir = settings.STATICFILES_DIRS[0] if settings.STATICFILES_DIRS else settings.STATIC_ROOT
            if background_image_name and background_image_name != 'none':
                background_image_path = os.path.join(static_dir, 'images', background_image_name)
            else:
                background_image_path = None

            converted_text = convert_to_kana_kanji(text)

            default_font_path = os.path.join(static_dir, 'fonts','KleeOne-SemiBold.ttf')
            output_image_path = os.path.join(settings.MEDIA_ROOT,'output.png')

            image_path = generate_kana_kanji_image(text_for_image, default_font_path, output_image_path, background_image_path)

            
            # フォームを再表示する際にゼロ幅スペースを取り除く
            cleaned_text = text.lstrip('\u200B')
            form = KanaKanjiForm(initial={'text': cleaned_text})

    return render(request, 'converter/index.html', {'form': form, 'converted_text': converted_text, 'image_path': image_path})
