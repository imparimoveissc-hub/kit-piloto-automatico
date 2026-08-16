#!/usr/bin/env bash
# IMPAR OS — inicializa banco SQLite

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OS_DIR="$(dirname "$SCRIPT_DIR")"
DB="$OS_DIR/database/impar.db"

sqlite3 "$DB" <<'SQL'
CREATE TABLE IF NOT EXISTS automations (
  id TEXT PRIMARY KEY, name TEXT, type TEXT, path TEXT,
  mode TEXT DEFAULT 'read-only', risk TEXT DEFAULT 'low',
  ai_required INTEGER DEFAULT 0, enabled INTEGER DEFAULT 1,
  last_checked TEXT, status TEXT DEFAULT 'unknown'
);
CREATE TABLE IF NOT EXISTS workflows (
  id TEXT PRIMARY KEY, name TEXT, n8n_id TEXT,
  active INTEGER DEFAULT 0, category TEXT,
  created_at TEXT, updated_at TEXT
);
CREATE TABLE IF NOT EXISTS executions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  run_id TEXT, timestamp TEXT, origin TEXT,
  action TEXT, duration_ms INTEGER, status TEXT,
  output_summary TEXT, exit_code INTEGER,
  ai_used INTEGER DEFAULT 0, cache_used INTEGER DEFAULT 0,
  error_msg TEXT
);
CREATE TABLE IF NOT EXISTS errors (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  timestamp TEXT, source TEXT, error_type TEXT,
  message TEXT, context TEXT, resolved INTEGER DEFAULT 0
);
CREATE TABLE IF NOT EXISTS cache_entries (
  key TEXT PRIMARY KEY, content TEXT, origin_hash TEXT,
  created_at TEXT, expires_at TEXT, last_used TEXT,
  use_count INTEGER DEFAULT 0
);
CREATE TABLE IF NOT EXISTS services (
  id TEXT PRIMARY KEY, name TEXT, type TEXT,
  url TEXT, status TEXT, last_checked TEXT,
  response_time_ms INTEGER
);
CREATE TABLE IF NOT EXISTS credentials_status (
  id TEXT PRIMARY KEY, service TEXT, label TEXT,
  status TEXT DEFAULT 'CREDENTIAL_PENDING',
  last_verified TEXT, notes TEXT
);
CREATE TABLE IF NOT EXISTS ai_usage (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  timestamp TEXT, caller TEXT, reason TEXT,
  tokens_estimated INTEGER, avoided INTEGER DEFAULT 0,
  model_used TEXT, cache_hit INTEGER DEFAULT 0
);
CREATE TABLE IF NOT EXISTS token_savings (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  date TEXT, action TEXT, method TEXT,
  tokens_saved INTEGER, ai_avoided INTEGER DEFAULT 1
);
CREATE TABLE IF NOT EXISTS approvals (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  timestamp TEXT, action_id TEXT, status TEXT,
  requested_by TEXT, approved_by TEXT, notes TEXT
);
CREATE TABLE IF NOT EXISTS system_state (
  key TEXT PRIMARY KEY, value TEXT, updated_at TEXT
);
SQL

# Seed serviços conhecidos
sqlite3 "$DB" <<SQL
INSERT OR REPLACE INTO services VALUES
  ('n8n','n8n Orchestrator','http','http://127.0.0.1:5678','unknown',NULL,NULL),
  ('docker','Docker','daemon','unix:///var/run/docker.sock','unknown',NULL,NULL);

INSERT OR REPLACE INTO credentials_status VALUES
  ('nfse.portal','NFS-e Portal Nacional','login','CREDENTIAL_PENDING',NULL,'Ver 18_AUTOMATION_STACK/nfem-joinville/.env'),
  ('facebook.session','Facebook Playwright Session','cookie','CREDENTIAL_PENDING',NULL,'Ver logs/login-facebook.log'),
  ('asaas.api','Asaas API','api_key','CREDENTIAL_PENDING',NULL,'Ver MCP config');

INSERT OR REPLACE INTO system_state VALUES
  ('installed_at','$(date -u +%Y-%m-%dT%H:%M:%SZ)','$(date -u +%Y-%m-%dT%H:%M:%SZ)'),
  ('version','1.0.0','$(date -u +%Y-%m-%dT%H:%M:%SZ)'),
  ('ai_calls_today','0','$(date -u +%Y-%m-%dT%H:%M:%SZ)'),
  ('ai_calls_avoided','0','$(date -u +%Y-%m-%dT%H:%M:%SZ)'),
  ('token_savings_estimated','0','$(date -u +%Y-%m-%dT%H:%M:%SZ)');
SQL

echo "OK: banco inicializado em $DB"
sqlite3 "$DB" ".tables"
