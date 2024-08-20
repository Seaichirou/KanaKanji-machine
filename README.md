# KanaKanji-machine
「仮名漢字」という漢字の代替え文字に変換するアプリケーションです。
WEBアプリとしては下記サイトで公開しています。  
https://kanakanji-machine-3cd804a8be3e.herokuapp.com/

## このリポジトリをアプリとして動作させるのに必要な事。
「jia-ming-han-zi-nojia-ming-mini-saizu.ttf」と言うフォントを使っていますが、規約により二次配布できません。下記URLのサイトからダウンロードして「converter/static/fonts」フォルダの中に入れて下さい。  
https://fontstruct.com/fontstructions/show/2442607/jia-ming-han-zi-nojia-ming-mini-saizu  

また、「KleeOne-SemiBold.ttf」というフォントも下記URLからダウンロードし、converter/static/fonts」フォルダの中に入れて下さい。  
https://fonts.google.com/specimen/Klee+One?subset=japanese&script=Hira  
「KleeOne-SemiBold.ttf」のライセンスはSIL Open Font License 1.1に基づいており、商用利用を含む幅広い用途で使用可能です。  

## このリポジトリの可能性。
約3000字の漢字とその部首をハッシュとした「converter/static/jsons/kanji_radicals.json」はあなたのアプリに役に立つファイルかもしれません。ただし間違えなどがあるかも知れないのでこ了承ください。

例えば文字制限をなくしてもっと長い文書を仮名漢字に変換させる事もできます。
また、他のフォントを設定したりレイアウトを整えたりして、様々なアイデアを試したりもできます。

#KanaKanji-machine

This application converts kanji characters into "仮名漢字," a proposed alternative script for kanji.
You can access the web version of the app at the following link:
https://kanakanji-machine-3cd804a8be3e.herokuapp.com/
Requirements for running this repository as an application:

This repository uses the font jia-ming-han-zi-nojia-ming-mini-saizu.ttf, but due to licensing restrictions, redistribution is not allowed. Please download the font from the following URL and place it in the converter/static/fonts folder.
https://fontstruct.com/fontstructions/show/2442607/jia-ming-han-zi-nojia-ming-mini-saizu

Additionally, please download the KleeOne-SemiBold.ttf font from the following URL and place it in the converter/static/fonts folder.
https://fonts.google.com/specimen/Klee+One?subset=japanese&script=Hira
The license for KleeOne-SemiBold.ttf is the SIL Open Font License 1.1, which allows broad usage, including commercial use.
Possibilities of this repository:

The file converter/static/jsons/kanji_radicals.json contains around 3000 kanji characters and their radicals hashed. It might be useful for your application, but please note that there could be errors.

For example, you could remove the character limit to convert longer texts into 仮名漢字.
You can also experiment with different fonts or adjust the layout to test various ideas.
