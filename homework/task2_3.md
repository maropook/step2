## Task3
https://docs.google.com/presentation/d/16V4bfiWJeum9ocwKph1ua5zlsJ3lUZ1gwBDeaCMK9Mo/edit?slide=id.g2374b16a205_1_222#slide=id.g2374b16a205_1_222
目標：「もっとも直近にアクセスされた上位 X 個の <URL, Web ページ> の組が保存できるデータ構造」を作ればよい

以下の操作がほぼ O(1) で実現できるようなデータ構造を考える
与えられた <URL, Web ページ> があるかないかを検索
もしない場合、キャッシュ内で一番古い <URL, Web ページ> を捨てて、代わりに与えられた <URL, Web ページ> を追加する


## Task3 回答
hashmapを使用する, page_url, webページ, newer_url, older_urlをvalueに持たせる

<URL, Web ページ> があるかないかを検索
・URLをKeyとしてhashmapから約O(1)で検索できる

もしない場合、キャッシュ内で一番古い <URL, Web ページ> を捨てて代わりに与えられた <URL, Web ページ> を追加する
・globalに定義したoldest_urlから検索し, hashmapから削除する ほぼ O(1)。新しいpage情報をhashmapに格納,globalのnewestをそれに更新する O(1)。

今持っているキャッシュ一覧を新しい順にとりだす
・globalに定義したnewest_urlからnewer_urlをたどっていくことで実現、今見ているpage情報がoldest_urlになったら終了