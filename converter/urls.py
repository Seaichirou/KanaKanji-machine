from django.urls import path
from .views import kana_kanji_converter

urlpatterns = [
    path('', kana_kanji_converter, name='kana_kanji_converter'),
    
]
