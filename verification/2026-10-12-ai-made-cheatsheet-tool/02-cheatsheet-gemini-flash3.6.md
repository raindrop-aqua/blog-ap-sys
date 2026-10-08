# PostgreSQL 保守用 psql コマンドチートシート

---

## 1. 接続コマンド

### 基本コマンド
```bash
psql -h <ホスト名/IP> -p <ポート> -U <ユーザー名> -d <データベース名>
```

### よく使う接続パターン
```bash
# ローカルDB接続（デフォルト）
psql -U postgres -d mydb

# リモート本番環境DB接続
psql -h 192.168.1.100 -p 5432 -U dbuser -d production_db
```

### 主要な接続オプション
- `-h`, `--host`: 接続先ホスト（省略時はローカルホスト）
- `-p`, `--port`: ポート番号（デフォルト: `5432`）
- `-U`, `--username`: 接続ユーザー名
- `-d`, `--dbname`: 接続データベース名
- `-W`: パスワード入力を強制

---

## 2. psql メタコマンド（接続中に使用）

> **Note**: コマンドの末尾に `+` を付けると（例: `\dt+`）、サイズや詳細説明などの拡張情報が表示されます。

### 接続・基本情報
| コマンド | 説明 |
| :--- | :--- |
| `\l` または `\list` | データベース一覧を表示 |
| `\c <DB名>` | 指定したデータベースに接続を切り替える |
| `\conninfo` | 現在の接続情報（ユーザー、DB、ホスト、ポート等）を表示 |
| `\q` | psql を終了する |

### オブジェクト確認
| コマンド | 説明 |
| :--- | :--- |
| `\dt` | テーブル一覧を表示 |
| `\d <テーブル名>` | テーブル構造（カラム、型、インデックス、制約など）を表示 |
| `\dn` | スキーマ一覧を表示 |
| `\du` | ユーザー（ロール）一覧と権限を表示 |
| `\di` | インデックス一覧を表示 |
| `\dv` | ビュー一覧を表示 |
| `\df` | 関数・関数定義一覧を表示 |

### 表示・操作補助
| コマンド | 説明 |
| :--- | :--- |
| `\x` | 縦表示（拡張表示）モードの ON / OFF 切替（列が多い場合に便利） |
| `\timing` | SQL実行時間の表示モード ON / OFF 切替 |
| `\e` | 外部エディタ（vim等）を開いて直前のSQLを編集・実行 |
| `\i <ファイルパス>` | 指定したファイル内のSQLスクリプトを実行 |
| `\o <ファイルパス>` | クエリ実行結果を指定ファイルに出力 |
| `\?` | psqlメタコマンドのヘルプ表示 |
| `\h <SQL文>` | 指定SQL命令の構文ヘルプ表示（例: `\h SELECT`） |

---

## 3. 保守管理用 SQL クエリ

### ① 実行中クエリ・アクティブ接続の確認
```sql
SELECT pid, usename, datname, client_addr, state, now() - query_start AS duration, query 
FROM pg_stat_activity 
WHERE state != 'idle' 
ORDER BY duration DESC;
```

### ② 長時間処理・ロックの強制停止
```sql
-- 指定したPIDのクエリを安全にキャンセル（接続は維持）
SELECT pg_cancel_backend(<PID>);

-- 指定したPIDのプロセス自体を強制終了
SELECT pg_terminate_backend(<PID>);
```

### ③ テーブル別ディスク使用量の確認
```sql
SELECT relname AS table_name,
       pg_size_pretty(pg_total_relation_size(relid)) AS total_size,
       pg_size_pretty(pg_relation_size(relid)) AS table_size,
       pg_size_pretty(pg_indexes_size(relid)) AS index_size
FROM pg_catalog.pg_statio_user_tables
ORDER BY pg_total_relation_size(relid) DESC;
```

### ④ データベース全体の容量確認
```sql
SELECT datname, pg_size_pretty(pg_database_size(datname)) AS db_size
FROM pg_database
ORDER BY pg_database_size(datname) DESC;
```

---

## 4. バックアップ・復元（CLIコマンド）

`psql` 内部ではなく、OSのターミナルで実行します。

### 単一データベースのバックアップ
```bash
# プレーンテキスト形式
pg_dump -U dbuser -d mydb > backup.sql

# カスタムフォーマット形式（圧縮・高速・pg_restore用）
pg_dump -F c -U dbuser -d mydb -f backup.dump
```

### 単一データベースの復元
```bash
# テキスト形式の復元
psql -U dbuser -d mydb -f backup.sql

# カスタムフォーマット形式の復元
pg_restore -U dbuser -d mydb backup.dump
```

---

## 5. 本番運用での安全対策テンプレート

誤った更新や削除を防ぐため、データ変更時は明示的にトランザクションを開始します。

```sql
-- 1. トランザクション開始
BEGIN;

-- 2. 変更操作の実行
DELETE FROM users WHERE last_login < '2022-01-01';

-- 3. 影響を受けた行数の確認（SELECT文で期待通りの状態かチェック）
SELECT count(*) FROM users WHERE last_login < '2022-01-01';

-- 4a. 問題なければ適用
COMMIT;

-- 4b. やり直す・問題がある場合は取り消し
ROLLBACK;
```