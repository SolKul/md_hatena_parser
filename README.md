# mdをはてな記法にパースする
markdownをはてなブログのはてな記法にパースするプログラムです。`md_parser`フォルダ内の`md_parser.py`を次のようにインポートして使います。

```python
from md_parser import md_parser
md_parser.parse_md_to_hatena(pathlib.Pathオブジェクト)
```
## 動機
はてなブログのmarkdownは数式をうまく扱えないし、Markdownはカスタマイズ性が低い。例えばMathJaxは重いので、将来的にはサーバーサイドで処理もしたい。将来はてなブログから移住するかもしれないし。でも一方プレビューしながら文章や数式を書きたいという欲望もある。そしてはてなブログのMarkdownプレビューは少し使いにくい。

そこで、VSCodeのMarkdown Preview EnhancedでMarkdownをプレビューしながら文章や数式を書き、それをパースすることにしました。

## 注意
うまくパースできなくても責任は取れないです。あくまでこういう事ができるという例です。

## 必要環境
python3.8以上。`pathilib`、`markdown`モジュールを使います。

## 例
main.pyを実行すると`Sample.md`がパースされ、パースされた`Sample_hatena.html`というファイルができるはずです。

## 対応しているもの、していないもの

`$$`で囲まれたブロック数式、`$`で囲まれたインライン数式、表、`#`が2つか3つのヘッダーには対応しています。
基本的に`markdown`モジュールがパースできるものはパースできるはずです。githubと同様、適度に改行しないとパースできないので注意(そのため`markdown-preview-enhanced.breakOnSingleNewLine`はオフ推奨)

また画像には対応していません。はてなブログに対応した方法で画像を貼り付けたほうがいいと思われるので。

## 実装

もとの`md`ファイルをリスト化し、文章全体を標準ブロック、数式ブロックとブロックごとのリストに分けてます。そして、標準ブロックはインライン数式を一旦退避させて、`markdown`モジュールで変換した後、退避させていたインライン数式を(はてな記法に変換した上で)変換後の文字列に戻しています。数式ブロックもはてなブログ用の数式フォーマットになるようにパースしています。そして最後に`"".join()`で全部ドッキングしてます。

## 感想

標準ブロック中のインライン数式に手間取りました😅。インライン数式中の不等号は`markdown`モジュールで解釈され勝手に変換されてしまうので、インライン数式を置換した後`markdown`モジュールで変換しても、`markdown`モジュールで変換した後インライン数式を置換してもダメなので、一度退避するという大掛かりなことをしなければなりませんでした。(`markdown`モジュールの使い方次第でもっとシンプルにできそう。`python-markdown-math`とかインストールすれば良いのか？ただ英語のレファレンスしか無く辛い。)

`python-markdown`便利ですね。 いろいろできそう。


あとめっちゃ`re`モジュール(正規表現)使った。`re`モジュールの使い方でこのサイトにはめちゃくちゃお世話になった。

https://note.nkmk.me/python-re-match-search-findall-etc/

(というかnote.nkmkは公式リファレンスよりわかりやすいよね)

## 参考にしたサイト

https://7shi.hateblo.jp/entry/2018/07/27/185311

https://ano3.hatenablog.com/entry/2020/04/15/034609

http://ichitcltk.hustle.ne.jp/gudon2/index.php?pageType=file&id=python_markdown_library_reference.md