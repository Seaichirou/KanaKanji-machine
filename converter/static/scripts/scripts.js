function updateCharCount() {
    const input = document.getElementById('id_text');
    const charCount = document.getElementById('char-count');
    const convertButton = document.querySelector('.convert-button'); // 変換ボタンを取得


    // 入力文字列の長さを初期化
    let currentLength = input.value.length;

    // 正規表現でマッチした部分を取得
    const kanaKanjiPattern = /([一-龠々ヶ]{1,2})([ｦ-ﾟヰヱヽヾ･]+)/g;
    const matches = input.value.matchAll(kanaKanjiPattern);

    // 半角カタカナの「･」の数をカウントする
    let markerCount = 0;
    for (const match of matches) {
        const kanaPart = match[2];
        const markers = kanaPart.match(/･/g);
        if (markers) {
            markerCount += markers.length;
        }
    }

    // 現在の文字数から半角カタカナの「･」の数を引く
    currentLength -= markerCount;

    // 文字数カウンターを更新
    const maxChars = 140;
    charCount.textContent = `${currentLength}/${maxChars}`;

    // 文字数が140を超えたら変換ボタンを無効にする
    if (currentLength > maxChars) {
        charCount.style.color = 'red';
        convertButton.disabled = true;
    } else {
        charCount.style.color = 'black';
        convertButton.disabled = false;
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const textarea = document.querySelector('textarea[name="text"]');
    const initialChar = '\u200B';

    // 入力時にゼロ幅スペースを削除
    textarea.addEventListener('input', function(event) {
        const cursorPosition = textarea.selectionStart;

        // ゼロ幅スペースが存在する場合、すべて削除
        if (textarea.value.includes(initialChar)) {
            textarea.value = textarea.value.replace(new RegExp(`\\${initialChar}`, 'g'), '');
            textarea.setSelectionRange(cursorPosition, cursorPosition); // カーソル位置を維持
        }
    });

    // ペースト時にゼロ幅スペースが削除されるように監視
    textarea.addEventListener('paste', function(event) {
        setTimeout(function() {
            const cursorPosition = textarea.selectionStart;
            // ゼロ幅スペースが存在する場合、すべて削除
            if (textarea.value.includes(initialChar)) {
                textarea.value = textarea.value.replace(new RegExp(`\\${initialChar}`, 'g'), '');
                textarea.setSelectionRange(cursorPosition, cursorPosition); // カーソル位置を維持
            }
        }, 0);
    });



    

    // カウンターの初期化と更新
    textarea.addEventListener('input', updateCharCount);
    updateCharCount();  // ページロード時に初期値を設定

    // テキストコピー用のボタン
    const textCopyButton = document.getElementById("text_copy_button");
    if (textCopyButton) {
        textCopyButton.addEventListener("click", function(event) {
            const text = document.getElementById("converted_text_container").innerText;
            navigator.clipboard.writeText(text).then(function() {
                textCopyButton.textContent = "コピーしました！";
                setTimeout(() => {
                    textCopyButton.textContent = "テキストをコピーする";
                }, 2000);
            }, function(err) {
                alert("テキストのコピーに失敗しました: ", err);
            });
        });
    }

// 画像コピー用のボタン
const imageCopyButton = document.getElementById("image_copy_button");

//if (imageCopyButton) {
    imageCopyButton.addEventListener("click", function() {
        const image = document.getElementById("generated_image");

        // 画像を直接クリップボードにコピー
        fetch(image.src)
            .then(response => response.blob())
            .then(blob => {
                const item = new ClipboardItem({ "image/png": blob });
                return navigator.clipboard.write([item]);
            })
            .then(() => {
                // コピー成功メッセージ
                imageCopyButton.textContent = "コピーしました！";
                setTimeout(() => {
                    imageCopyButton.textContent = "画像をコピーする";
                }, 2000);
            });
    });
//}
});