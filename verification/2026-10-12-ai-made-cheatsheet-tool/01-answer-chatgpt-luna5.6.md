もちろんです。PostgreSQL の保守担当なら、まずは **「接続 → 状態確認 → DB/テーブル確認 → SQL実行 → psql終了」** の流れを覚えるとかなり楽です。

以下では、`psql` を使った実務でよく使うものに絞って整理します。

---

# 1. PostgreSQLへ接続する

基本形はこれです。

```bash
psql -h ホスト名 -p ポート番号 -U ユーザー名 -d データベース名
```

例えば、

```bash
psql -h localhost -p 5432 -U postgres -d mydb
```

それぞれ、

| オプション | 意味                 |
| ----- | ------------------ |
| `-h`  | PostgreSQLサーバーのホスト |
| `-p`  | ポート番号。通常 `5432`    |
| `-U`  | PostgreSQLユーザー     |
| `-d`  | 接続するデータベース         |

です。

### ローカルで接続する場合

例えばサーバー上で作業していて、PostgreSQLがローカルにあるなら、

```bash
psql -U postgres
```

でも接続できます。

ユーザーと同名のDBに接続する設定になっている環境では、

```bash
psql
```

だけで接続できることもあります。

---

# 2. パスワードを求められたら

例えば、

```bash
psql -h 192.168.1.100 -U postgres -d mydb
```

とすると、

```text
Password for user postgres:
```

と聞かれるので、PostgreSQLのパスワードを入力します。

入力中は画面に文字が表示されません。

---

# 3. 接続できたか確認

接続すると、

```text
mydb=#
```

のようなプロンプトになります。

例えば、

```text
postgres=#
```

なら `postgres` DBに接続しています。

一般ユーザーの場合、

```text
mydb=>
```

のようになることもあります。

ざっくり、

* `=#` → PostgreSQLの管理者権限を持つユーザーなど
* `=>` → 一般ユーザー

と考えておけばよいです。

---

# 4. psqlでまず覚えるコマンド

ここが重要です。

`psql` には、通常のSQLとは別に **psql専用コマンド**があります。

これらは `\` から始まります。

## DB一覧

```text
\l
```

または

```text
\list
```

例えば、

```text
postgres=# \l
```

すると、

```text
Name      | Owner    | Encoding
----------+----------+----------
postgres  | postgres | UTF8
mydb      | admin    | UTF8
testdb    | admin    | UTF8
```

のように表示されます。

---

# 5. 現在接続しているDBを確認

```text
\conninfo
```

例えば、

```text
You are connected to database "mydb" as user "postgres" on host "localhost" at port "5432".
```

といった情報が出ます。

**保守作業では最初に `\conninfo` を打つ癖をつけるのがおすすめです。**

「本番DBだと思って作業していたら、実は検証DBだった」

あるいはその逆を防げます。

---

# 6. DBを切り替える

```text
\c データベース名
```

例えば、

```text
\c mydb
```

または

```text
\connect mydb
```

ユーザーも変更するなら、

```text
\c mydb admin
```

です。

---

# 7. テーブル一覧を見る

```text
\dt
```

例えば、

```text
mydb=# \dt
```

すると、

```text
 Schema |       Name       | Type  | Owner
--------+------------------+-------+--------
 public | users            | table | admin
 public | orders           | table | admin
 public | products         | table | admin
```

のように表示されます。

---

## 特定のスキーマを見る

例えば `public` スキーマなら、

```text
\dt public.*
```

---

## すべてのスキーマのテーブルを見る

```text
\dt *.*
```

ただし、かなり大量に出る環境もあります。

---

# 8. スキーマ一覧

```text
\dn
```

例えば、

```text
 Schema | Owner
--------+--------
 public | postgres
 app    | postgres
```

など。

---

# 9. テーブルの構造を見る

これは非常によく使います。

```text
\d テーブル名
```

例えば、

```text
\d users
```

すると、

```text
              Table "public.users"
 Column | Type      | Nullable | Default
--------+-----------+----------+---------
 id     | bigint    | not null | ...
 name   | text      |          |
 email  | text      |          |
```

などが表示されます。

---

## より詳しく見る

```text
\d+ users
```

インデックスやサイズなども含めて確認できます。

---

# 10. SQLを実行する

ここからは普通のSQLです。

例えば、

```sql
SELECT * FROM users;
```

**SQLは最後に `;` を付けます。**

```text
mydb=# SELECT * FROM users;
```

---

## 件数を見る

保守では非常によく使います。

```sql
SELECT COUNT(*) FROM users;
```

---

## 上位10件を見る

```sql
SELECT * FROM users LIMIT 10;
```

---

## 条件を指定する

```sql
SELECT *
FROM users
WHERE id = 100;
```

---

# 11. SQLを書くときのポイント

例えば、

```sql
SELECT *
FROM users
WHERE name = 'Taro';
```

のように、文字列は `'` で囲みます。

```sql
'Taro'
```

一方、

```sql
"users"
```

の `"` は、テーブル名・カラム名などの識別子を扱う場合に使います。

ここは混同しやすいです。

---

# 12. SQLを複数行で入力できる

例えば、

```sql
SELECT
    id,
    name,
    email
FROM
    users
WHERE
    id > 100;
```

と入力できます。

最後の

```text
;
```

を入力したところで実行されます。

途中で間違えた場合は、

```text
\cancel
```

で入力中のSQLをキャンセルできます。

---

# 13. psqlの便利なコマンド

## コマンド一覧

```text
\?
```

psqlのメタコマンド一覧です。

---

## SQLコマンドのヘルプ

```text
\h
```

例えば、

```text
\h SELECT
```

や、

```text
\h CREATE TABLE
```

など。

---

# 14. 実行したSQLの履歴

```text
\s
```

でSQL履歴を確認できます。

環境によっては、

```bash
~/.psql_history
```

にも履歴が保存されます。

---

# 15. 出力を見やすくする

大量の列があるテーブルを見ると、

```text
SELECT * FROM very_large_table;
```

が横に長くなって非常に見づらいことがあります。

そんなときは、

```text
\x
```

を使います。

例えば、

```text
mydb=# \x
Expanded display is on.
```

その状態で、

```sql
SELECT * FROM users WHERE id = 1;
```

とすると、

```text
-[ RECORD 1 ]-----
id    | 1
name  | Taro
email | taro@example.com
```

のように縦表示されます。

もう一度、

```text
\x
```

で元に戻せます。

**個人的には保守作業でかなりおすすめのコマンドです。**

---

# 16. 実行時間を表示する

```text
\timing on
```

すると、

```text
SELECT COUNT(*) FROM users;

 count
-------
 10000
(1 row)

Time: 12.345 ms
```

のように実行時間が表示されます。

OFFにするには、

```text
\timing off
```

---

# 17. SQLファイルを実行する

例えば、

```text
update.sql
```

というSQLファイルがあるなら、

```text
\i update.sql
```

で実行できます。

シェルから直接実行することもできます。

```bash
psql -h localhost -U postgres -d mydb -f update.sql
```

保守作業ではこちらもかなり重要です。

---

# 18. psqlからシェルコマンドを実行

```text
\! ls
```

など。

例えば、

```text
\! pwd
```

とすると、現在のディレクトリを確認できます。

ただし、サーバー上で作業している場合は「どのマシン上で実行されるコマンドなのか」を意識してください。

---

# 19. トランザクション

データ変更を伴う保守では非常に重要です。

例えば、

```sql
BEGIN;
```

としてから、

```sql
UPDATE users
SET name = 'Taro'
WHERE id = 100;
```

確認します。

```sql
SELECT *
FROM users
WHERE id = 100;
```

問題なければ、

```sql
COMMIT;
```

問題があれば、

```sql
ROLLBACK;
```

です。

つまり、

```text
BEGIN
  ↓
UPDATE / DELETE
  ↓
SELECTで確認
  ↓
問題なし → COMMIT
問題あり → ROLLBACK
```

という流れです。

**本番DBでUPDATE/DELETEを実行するなら、まずトランザクションを意識することを強くおすすめします。**

---

# 20. PostgreSQLのバージョン確認

SQLなら、

```sql
SELECT version();
```

psql自体のバージョンなら、シェルで、

```bash
psql --version
```

です。

例えば、

```text
psql (PostgreSQL) 16.4
```

のように表示されます。

---

# 21. 現在のユーザー

```sql
SELECT current_user;
```

現在のDB：

```sql
SELECT current_database();
```

現在の日時：

```sql
SELECT now();
```

このあたりは障害調査でも便利です。

---

# 22. よく使う確認セット

保守担当になったばかりなら、DBに接続したらまずこれを打てるようになるといいです。

```text
\conninfo
```

```text
\l
```

```text
\dn
```

```text
\dt
```

```text
\d テーブル名
```

そしてSQLで、

```sql
SELECT version();
```

```sql
SELECT current_user;
```

```sql
SELECT current_database();
```

です。

---

# 23. psqlを終了する

```text
\q
```

です。

```text
mydb=# \q
```

でシェルに戻ります。

---

# 24. 最初に覚えるべきコマンド一覧

まずはこの表を手元に置いておけば十分です。

| コマンド                        | 用途            |
| --------------------------- | ------------- |
| `psql -h ... -U ... -d ...` | PostgreSQLへ接続 |
| `\conninfo`                 | 現在の接続情報       |
| `\l`                        | DB一覧          |
| `\c DB名`                    | DB切り替え        |
| `\dn`                       | スキーマ一覧        |
| `\dt`                       | テーブル一覧        |
| `\d テーブル名`                  | テーブル定義        |
| `\d+ テーブル名`                 | 詳細なテーブル定義     |
| `\x`                        | 縦表示切り替え       |
| `\timing on`                | 実行時間表示        |
| `\i ファイル.sql`               | SQLファイル実行     |
| `\?`                        | psqlコマンドのヘルプ  |
| `\h`                        | SQLヘルプ        |
| `\q`                        | 終了            |
| `BEGIN;`                    | トランザクション開始    |
| `COMMIT;`                   | 確定            |
| `ROLLBACK;`                 | 取り消し          |

---

## そして、保守では「接続方法」より先に確認したいことがあります

実際の現場では、

```text
自分のPC
   │
   │ SSH
   ↓
DBサーバー
   │
   └── PostgreSQL :5432
```

なのか、

```text
自分のPC
   │
   │ psql
   ↓
DBサーバー
```

なのかで、接続方法がかなり変わります。

また、

* PostgreSQLがLinux上なのかWindows上なのか
* SSHでサーバーに入るのか
* Docker / Kubernetesなのか
* PostgreSQLがローカルなのか別サーバーなのか
* `postgres` ユーザーを使うのか専用ユーザーなのか
* 本番・検証・開発環境が分かれているのか
* SSL/TLS接続が必要なのか

によって、実際に使う `psql` コマンドも変わります。

**もし今回担当する環境の構成が分かるなら、そこに合わせて「実際の保守作業で使う psql コマンド集」を作れます。**
例えば「Windows PC → SSH → Linuxサーバー → PostgreSQL」のように構成を教えてもらえれば、接続からバックアップ、ログ確認、テーブル確認、インデックス確認、ロック・長時間SQLの確認まで、実務向けに順番に整理できます。
