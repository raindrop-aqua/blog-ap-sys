# PostgreSQL 保守担当者向けチートシート

## 接続

### ローカル接続

```bash
psql -U postgres
```

### データベースを指定して接続

```bash
psql -U postgres -d mydb
```

### リモート接続

```bash
psql -h 192.168.1.100 -p 5432 -U postgres -d mydb
```

### 接続文字列形式

```bash
psql "host=192.168.1.100 port=5432 dbname=mydb user=postgres"
```

### パスワード指定（確認用）

```bash
export PGPASSWORD='password'
psql -h localhost -U postgres -d mydb
```

---

# psqlメタコマンド

## 接続情報確認

```sql
\conninfo
```

## データベース一覧

```sql
\l
```

または

```sql
\list
```

## データベース切替

```sql
\c mydb
```

## スキーマ一覧

```sql
\dn
```

## テーブル一覧

```sql
\dt
```

## ビュー一覧

```sql
\dv
```

## ユーザー一覧

```sql
\du
```

## テーブル定義確認

```sql
\d users
```

## テーブル詳細確認

```sql
\d+ users
```

## psql終了

```sql
\q
```

---

# 基本情報確認SQL

## PostgreSQLバージョン

```sql
SELECT version();
```

## 現在のDB名

```sql
SELECT current_database();
```

## 現在のユーザー

```sql
SELECT current_user;
```

## 現在時刻

```sql
SELECT now();
```

---

# データ確認

## 件数確認

```sql
SELECT COUNT(*) FROM users;
```

## 先頭100件表示

```sql
SELECT *
FROM users
LIMIT 100;
```

## テーブル構造確認

```sql
SELECT *
FROM information_schema.columns
WHERE table_name = 'users';
```

---

# セッション・接続確認

## 現在の接続一覧

```sql
SELECT *
FROM pg_stat_activity;
```

## 必要最低限の確認

```sql
SELECT
    pid,
    usename,
    application_name,
    client_addr,
    state,
    query
FROM pg_stat_activity;
```

---

# ロック確認

## ロック状況確認

```sql
SELECT *
FROM pg_locks;
```

## ロック待ち確認

```sql
SELECT
    pid,
    usename,
    wait_event_type,
    wait_event,
    query
FROM pg_stat_activity
WHERE wait_event IS NOT NULL;
```

---

# サイズ確認

## テーブルサイズ

```sql
SELECT
    pg_size_pretty(
        pg_relation_size('users')
    );
```

## テーブル総サイズ（インデックス含む）

```sql
SELECT
    pg_size_pretty(
        pg_total_relation_size('users')
    );
```

## サイズの大きいテーブル一覧

```sql
SELECT
    relname,
    pg_size_pretty(
        pg_total_relation_size(relid)
    ) AS total_size
FROM pg_catalog.pg_statio_user_tables
ORDER BY pg_total_relation_size(relid) DESC;
```

---

# インデックス確認

## テーブルのインデックス確認

```sql
\d users
```

## SQLで確認

```sql
SELECT
    indexname,
    indexdef
FROM pg_indexes
WHERE tablename = 'users';
```

---

# SQL性能調査

## 実行計画確認

```sql
EXPLAIN
SELECT *
FROM users
WHERE id = 100;
```

## 実行時間付き実行計画

```sql
EXPLAIN ANALYZE
SELECT *
FROM users
WHERE id = 100;
```

---

# メンテナンス

## 統計情報更新

```sql
ANALYZE users;
```

## 不要領域回収

```sql
VACUUM users;
```

## 両方実施

```sql
VACUUM ANALYZE users;
```

## 全データベース対象

```sql
VACUUM ANALYZE;
```

---

# 障害時によく使うコマンド

## 長時間実行中のSQL確認

```sql
SELECT
    pid,
    now() - query_start AS duration,
    usename,
    state,
    query
FROM pg_stat_activity
WHERE state <> 'idle'
ORDER BY duration DESC;
```

## セッション終了

```sql
SELECT pg_terminate_backend(PID);
```

例

```sql
SELECT pg_terminate_backend(12345);
```

※ 本番環境では影響確認必須

---

# 保守担当の必須コマンド TOP10

```sql
\conninfo
\l
\dt
\d テーブル名

SELECT version();
SELECT current_database();
SELECT current_user();

SELECT * FROM pg_stat_activity;

EXPLAIN ANALYZE ...

VACUUM ANALYZE テーブル名;
```

---

# 保守業務で最もよく使う確認フロー

```sql
-- 接続確認
\conninfo

-- テーブル確認
\dt

-- テーブル構造確認
\d テーブル名

-- 接続状況確認
SELECT * FROM pg_stat_activity;

-- サイズ確認
SELECT pg_size_pretty(
    pg_total_relation_size('テーブル名')
);

-- SQL性能確認
EXPLAIN ANALYZE SELECT ...;

-- 統計更新
VACUUM ANALYZE テーブル名;
```