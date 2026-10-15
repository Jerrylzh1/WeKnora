#!/usr/bin/env bash
set -e
MCP_DIR=/opt/weknora-mcp
APP_DIR=/data/weknora/mcp-server

echo "=== install deps ==="
pip install --quiet -r "$APP_DIR/requirements.txt" starlette uvicorn 2>&1 | tail -3

echo "=== write env file ==="
cat > /opt/weknora-mcp.env <<'EOF'
WEKNORA_BASE_URL=http://localhost:8080/api/v1
WEKNORA_API_KEY=REPLACE_WITH_YOUR_KEY
MCP_TRANSPORT=http
MCP_SERVER_HOST=0.0.0.0
MCP_SERVER_PORT=8000
MCP_SERVER_AUTH_TOKEN=WeKnoraMcp@2026!token
EOF

echo "=== test config ==="
python "$APP_DIR/main.py" --check-only 2>&1 | tail -10 || true

echo "=== start in background ==="
# 用 nohup 后台跑; 读取 env 文件
set -a; source /opt/weknora-mcp.env; set +a
cd "$APP_DIR"
nohup python main.py --transport http --host 0.0.0.0 --port 8000 > /var/log/weknora-mcp.log 2>&1 &
echo "started pid $!"
sleep 6
echo "=== log tail ==="
tail -15 /var/log/weknora-mcp.log
echo "=== probe ==="
curl -s -o /dev/null -w 'mcp endpoint -> %{http_code}\n' -H "Authorization: Bearer WeKnoraMcp@2026!token" http://localhost:8000/mcp
