#!/usr/bin/env bash
echo "=== python ==="
which python3 python 2>/dev/null; python3 --version 2>/dev/null
echo "=== uv ==="
which uv 2>/dev/null; uv --version 2>/dev/null || echo "NO_UV"
echo "=== pip ==="
which pip3 pip 2>/dev/null
echo "=== app reachable from host? ==="
curl -s -o /dev/null -w 'localhost:8080 -> %{http_code}\n' http://localhost:8080/api/v1/health
echo "=== 8000 port listening? ==="
(ss -ltnp 2>/dev/null | grep ':8000' || echo '8000 FREE')
echo "=== compose app service name ==="
grep -E '^\s+app:|container_name' /data/weknora/docker-compose.yml | head -5
