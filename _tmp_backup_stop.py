import os
import paramiko

HOST = "10.56.5.140"
USER = "root"
PASSWORD = os.environ.get("SERVER_PASSWORD") or input("请输入服务器密码: ")


def run(client, cmd, timeout=300):
    stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    out = stdout.read().decode()
    err = stderr.read().decode()
    return out, err


def main():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, username=USER, password=PASSWORD, timeout=30)

    # 1. pg 逻辑备份（数据库运行时）
    cmd = (
        "mkdir -p /data/backup-$(date +%Y%m%d) && "
        "docker exec WeKnora-postgres pg_dumpall -U postgres > /data/backup-$(date +%Y%m%d)/pgdump.sql 2>/data/backup-$(date +%Y%m%d)/pgdump.err; "
        "echo \"pgdump exit=$?\"; "
        "ls -lh /data/backup-$(date +%Y%m%d)/"
    )
    out, err = run(client, cmd, timeout=600)
    print("=== PG DUMP ===")
    print(out)
    if err.strip():
        print("STDERR:", err)

    # 2. 停旧 weknora 应用服务（保留数据服务）
    cmd2 = (
        "cd /data/WeKnora-0.6.0 && "
        "docker compose stop app frontend docreader sandbox 2>&1; "
        "echo 'stop done'; "
        "docker ps --format '{{.Names}}\\t{{.Status}}' | grep -iE 'weknora|postgres|qdrant|minio|neo4j'"
    )
    out2, err2 = run(client, cmd2, timeout=300)
    print("=== STOP APP ===")
    print(out2)
    if err2.strip():
        print("STDERR:", err2)

    client.close()
    print("done")


if __name__ == "__main__":
    main()
