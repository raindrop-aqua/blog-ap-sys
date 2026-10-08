# PostgreSQL / psql 保守用チートシート

## 1. psqlへの接続

### 基本形

```bash
psql -h ホスト名 -p ポート番号 -U ユーザー名 -d データベース名
```

例：

```bash
psql -h localhost -p 5432 -U postgres -d mydb
```

### ローカル接続

```bash
psql -U postgres
```

環境によっては、

```bash
psql
```

だけで接続できる場合もある。

### 主なオプション

| オプション | 意味                     |
| ----- | ---------------------- |
| `-h`  | PostgreSQLサーバーのホスト名/IP |
| `-p`  | ポート番号（通常 `5432`）       |
| `-U`  | PostgreSQLユーザー         |
| `-d`  | データベース名                |
| `-f`  | SQLファイルを実行             |

---

# 2. 接続直後に確認すること

## 現在の接続情報

```text
\conninfo
```

接続先DB、ユーザー、ホスト、ポートなどを確認できる。

**本番DBで作業する前には必ず確認する。**

---

## PostgreSQLのバージョン

```sql
SELECT version();
```

またはシェルから：

```bash
psql --version
```

---

## 現在のユーザー

```sql
SELECT current_user;
```

## 現在のデータベース

```sql
SELECT current_database();
```

## 現在日時

```sql
SELECT now();
```

---

# 3. データベース操作

## データベース一覧

```text
\l
```

または：

```text
\list
```

---

## データベースを切り替える

```text
\c データベース名
```

例：

```text
\c mydb
```

ユーザーも変更：

```text
\c mydb admin
```

---

# 4. スキーマ・テーブル確認

## スキーマ一覧

```text
\dn
```

---

## テーブル一覧

```text
\dt
```

特定スキーマ：

```text
\dt public.*
```

すべてのスキーマ：

```text
\dt *.*
```

※ 大規模DBでは大量に表示される場合がある。

---

# 5. テーブル定義の確認

## 基本

```text
\d テーブル名
```

例：

```text
\d users
```

---

## 詳細情報

```text
\d+ テーブル名
```

インデックスなどの詳細も確認できる。

---

# 6. SQLの基本

## SELECT

```sql
SELECT * FROM users;
```

---

## 件数確認

```sql
SELECT COUNT(*) FROM users;
```

---

## 上位10件

```sql
SELECT *
FROM users
LIMIT 10;
```

---

## 条件指定

```sql
SELECT *
FROM users
WHERE id = 100;
```

---

## 複数条件

```sql
SELECT *
FROM users
WHERE id > 100
  AND status = 'active';
```

---

## 並び替え

```sql
SELECT *
FROM users
ORDER BY id DESC;
```

---

# 7. SQL入力時の注意

SQLは通常、最後に `;` を付けて実行する。

```sql
SELECT *
FROM users
WHERE id = 100;
```

文字列：

```sql
'Taro'
```

テーブル名・カラム名などの識別子：

```sql
"users"
```

`'` と `"` を混同しない。

---

# 8. SQL入力をキャンセル

入力途中のSQLをキャンセル：

```text
\cancel
```

---

# 9. 表示を見やすくする

## 縦表示

```text
\x
```

例えば、

```sql
SELECT *
FROM users
WHERE id = 1;
```

通常の横表示ではなく、

```text
-[ RECORD 1 ]-----
id    | 1
name  | Taro
email | taro@example.com
```

のように表示できる。

もう一度、

```text
\x
```

で元に戻る。

---

# 10. SQL実行時間を確認

有効化：

```text
\timing on
```

例：

```text
SELECT COUNT(*) FROM users;
```

実行結果に、

```text
Time: 12.345 ms
```

のように実行時間が表示される。

無効化：

```text
\timing off
```

---

# 11. SQLファイルを実行

## psql内から

```text
\i update.sql
```

---

## シェルから

```bash
psql -h localhost -U postgres -d mydb -f update.sql
```

---

# 12. トランザクション

データ変更を伴う保守作業では重要。

## 開始

```sql
BEGIN;
```

## 変更

```sql
UPDATE users
SET name = 'Taro'
WHERE id = 100;
```

## 結果確認

```sql
SELECT *
FROM users
WHERE id = 100;
```

## 問題なければ確定

```sql
COMMIT;
```

## 問題があれば取り消し

```sql
ROLLBACK;
```

### 基本パターン

```text
BEGIN;
  ↓
UPDATE / DELETE
  ↓
SELECTで結果確認
  ↓
問題なし → COMMIT;
問題あり → ROLLBACK;
```

**本番DBでUPDATE/DELETEする場合は、トランザクションを意識する。**

---

# 13. psqlのヘルプ

## psqlコマンド一覧

```text
\?
```

## SQLコマンドのヘルプ

```text
\h
```

例：

```text
\h SELECT
```

```text
\h CREATE TABLE
```

---

# 14. SQL履歴

```text
\s
```

環境によっては、

```text
~/.psql_history
```

にも履歴が保存される。

---

# 15. psqlからシェルコマンド

```text
\! コマンド
```

例：

```text
\! pwd
```

```text
\! ls
```

※ サーバー上で作業している場合、どのマシン上で実行されるか注意する。

---

# 16. psql終了

```text
\q
```

---

# 17. よく使うコマンド早見表

| コマンド           | 用途                |
| -------------- | ----------------- |
| `\conninfo`    | 現在の接続情報           |
| `\l`           | DB一覧              |
| `\c DB名`       | DB切り替え            |
| `\dn`          | スキーマ一覧            |
| `\dt`          | テーブル一覧            |
| `\dt public.*` | publicスキーマのテーブル一覧 |
| `\d テーブル名`     | テーブル定義            |
| `\d+ テーブル名`    | 詳細なテーブル定義         |
| `\x`           | 縦表示切り替え           |
| `\timing on`   | SQL実行時間を表示        |
| `\timing off`  | SQL実行時間表示を解除      |
| `\i ファイル.sql`  | SQLファイル実行         |
| `\s`           | SQL履歴             |
| `\?`           | psqlコマンドヘルプ       |
| `\h`           | SQLヘルプ            |
| `\cancel`      | 入力中のSQLをキャンセル     |
| `\! コマンド`      | シェルコマンド実行         |
| `\q`           | psql終了            |

---

# 18. よく使うSQL早見表

| SQL                             | 用途              |
| ------------------------------- | --------------- |
| `SELECT version();`             | PostgreSQLバージョン |
| `SELECT current_user;`          | 現在のユーザー         |
| `SELECT current_database();`    | 現在のDB           |
| `SELECT now();`                 | 現在日時            |
| `SELECT * FROM table;`          | データ確認           |
| `SELECT COUNT(*) FROM table;`   | 件数確認            |
| `SELECT * FROM table LIMIT 10;` | 先頭10件確認         |
| `SELECT ... WHERE ...;`         | 条件検索            |
| `BEGIN;`                        | トランザクション開始      |
| `COMMIT;`                       | 変更確定            |
| `ROLLBACK;`                     | 変更取り消し          |

---

# 19. 保守作業の基本フロー

## ① 接続

```bash
psql -h HOST -p 5432 -U USER -d DATABASE
```

## ② 接続先確認

```text
\conninfo
```

## ③ DB・スキーマ確認

```text
\l
\dn
```

## ④ テーブル確認

```text
\dt
```

## ⑤ テーブル構造確認

```text
\d テーブル名
```

## ⑥ 必要なデータをSELECT

```sql
SELECT *
FROM テーブル名
LIMIT 10;
```

## ⑦ データ変更が必要ならトランザクション

```sql
BEGIN;
```

## ⑧ UPDATE / DELETE

```sql
UPDATE ...;
```

または

```sql
DELETE ...;
```

## ⑨ 結果確認

```sql
SELECT ...;
```

## ⑩ 問題なければ確定

```sql
COMMIT;
```

問題があれば：

```sql
ROLLBACK;
```

## ⑪ 終了

```text
\q
```

---

# 20. 本番DBでの注意事項

### 最初に必ず接続先を確認

```text
\conninfo
```

特に、

* 本番
* ステージング
* 開発
* ローカル

を間違えない。

---

### UPDATE / DELETE の前にSELECT

例えば、

```sql
SELECT *
FROM users
WHERE id = 100;
```

で対象を確認してから、

```sql
UPDATE users
SET status = 'inactive'
WHERE id = 100;
```

とする。

---

### WHERE句を確認

危険：

```sql
DELETE FROM users;
```

これはテーブルの全レコードを削除する。

危険：

```sql
UPDATE users
SET status = 'inactive';
```

これは全レコードを更新する。

基本的には、

```sql
DELETE FROM users
WHERE id = 100;
```

```sql
UPDATE users
SET status = 'inactive'
WHERE id = 100;
```

のように対象を限定する。

---

### 可能ならトランザクションを使用

```sql
BEGIN;

UPDATE users
SET status = 'inactive'
WHERE id = 100;

SELECT *
FROM users
WHERE id = 100;

-- 問題なければ
COMMIT;

-- 問題があれば
-- ROLLBACK;
```

---

# 21. 最低限これだけ覚える

最初は以下だけでも十分。

```text
\conninfo     接続先確認
\l            DB一覧
\c DB名       DB切り替え
\dn           スキーマ一覧
\dt           テーブル一覧
\d テーブル   テーブル構造
\x            縦表示
\timing on    実行時間
\q            終了
```

SQL：

```sql
SELECT * FROM table LIMIT 10;

SELECT COUNT(*) FROM table;

BEGIN;

UPDATE ...;

DELETE ...;

COMMIT;

ROLLBACK;
```

**特に本番環境では `\conninfo` → SELECT確認 → BEGIN → 変更 → SELECT確認 → COMMIT/ROLLBACK の流れを習慣にする。**
