# HashTable Documentation
### calculate_hash(key) -> int
keyを一文字づつ見て数字に変換し、indexで重み付けする
indexが1増えるごとに10**iで重み付けをし、hash値が約8桁の数字(0~100万)を表せるようにした
(keyは8桁の数字になることもあるため0)

## HashTable
コリジョンが起こった場合は連結リストの頭につなげていく

### put(key, value) -> bool
updateを呼び出し、すでにbucketsに入っていればvalueで上書きしFalseを返す
bucketsにない場合は配列の先頭にItemを追加しTrueを返す

### update(key, value) -> bool
bucketsにkeyがあればvalueを更新する

### get(key) -> (value, bool)
keyから作られたindexの先頭から連結リストを探索していき、bucketsにkeyがあれば(value, True)を返す
ない場合は(None, False)を返す

### delete(key) -> bool
keyから作られたindexの先頭から連結リストを探索していき、bucketsにkeyがあれば,前後のnextをつなぎ直してTrueを返す
なかった場合はFalseを返す

### rehash_if_needed()
usage_rateが30%を下回ったらbucket_sizeを半分かつ奇数に設定し、
rehashを呼び出す
usage_rateが70%を上回ったらbucket_sizeを2倍かつ奇数に設定し, rehashを呼び出す

### rehash(size)
bucket_size = sizeとして新しい配列を定義
前のbucketsを全探索し、putを呼び出し全てのItemsを新しいbucketsに入れる
