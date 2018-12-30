## redpen

### [redpen](http://redpen.cc/docs/latest/index_ja.html)とは

RedPen はオープンソースの校正ツールです。
RedPen はは技術文書がが文書規約に従って書かれているかを自動検査します。
``
https://github.com/redpen-cc/redpen

### install redpen

```bash
brew cask install java
brew install redpen
```

### execute

```bash
redpen -c [config file] -r [result format] target_file
```

### 参考

https://qiita.com/m_mizutani/items/c48f67f871d1d41ff4b9

https://qiita.com/takahi-i/items/f16fd93e2e5061851320

https://qiita.com/m_mizutani/items/c48f67f871d1d41ff4b9

https://qiita.com/int_main_void/items/c456d06312817f3bc78d

https://qiita.com/ymdymd/items/83aca4134c59b0228659

https://kamiya555.github.io/2015/09/26/argparse-args/

https://www.lifewithpython.com/2016/06/python-ternary-operator.html

#### 設計

1. コマンドラインで引数を取得する。
1. ファイルの存在チェック
1. ファイルを読み込む
1. redpenでチェックする
1. 結果を表示する
1. 投稿を確認する
1. 投稿する
