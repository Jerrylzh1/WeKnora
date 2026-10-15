import sys
import io

if hasattr(sys.stdout, "buffer") and sys.stdout.encoding != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

import paramiko

HOST = "10.56.5.140"
USER = "root"
PASSWORD = (len(sys.argv) > 1 and sys.argv[1]) or input("请输入服务器密码: ")


def ssh_exec(client, cmd, timeout=300):
    stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    out = stdout.read().decode()
    err = stderr.read().decode()
    return out, err


def main():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, username=USER, password=PASSWORD, timeout=60)

    # 1) 准备备份目录
    ts = ssh_exec(client, "date +%Y%m%d-%H%M%S")[0].strip()
    bdir = f"/data/backup/weknora-0.7.2-{ts}"
    print("备份目录:", bdir)
    ssh_exec(client, f"mkdir -p {bdir}/config {bdir}/volumes {bdir}")

    # 2) 备份配置文件（.env / compose / frontend 源码）
    cfg, e = ssh_exec(client,
        f"cp /data/weknora/.env {bdir}/config/.env && "
        f"cp /data/weknora/docker-compose.yml {bdir}/config/ && "
        f"cp /data/weknora/docker-compose.dev.yml {bdir}/config/ && "
        f"cp -r /data/weknora/frontend {bdir}/config/frontend-src 2>/dev/null; "
        f"echo cfg_done")
    print("配置备份:", cfg.strip(), e.strip())

    # 3) 从 .env 读取 postgres 凭据，做 pg_dumpall（在线，不中断服务）
    env_out, _ = ssh_exec(client, "grep -E '^POSTGRES_(USER|PASSWORD|DB)=' /data/weknora/.env")
    puser, ppass, pdb = "postgres", "", "postgres"
    for line in env_out.splitlines():
        if line.startswith("POSTGRES_USER="):
            puser = line.split("=", 1)[1].strip()
        elif line.startswith("POSTGRES_PASSWORD="):
            ppass = line.split("=", 1)[1].strip()
        elif line.startswith("POSTGRES_DB="):
            pdb = line.split("=", 1)[1].strip()
    print(f"PG user={puser} db={pdb}")

    pg, e = ssh_exec(client,
        f"PGPASSWORD='{ppass}' docker exec -i WeKnora-postgres pg_dumpall -U {puser} "
        f"> {bdir}/postgres_all.sql 2>/dev/null; echo pg_done; ls -lh {bdir}/postgres_all.sql")
    print("PG dump:", pg.strip(), e.strip())

    # 4) 数据卷快照（崩溃一致性，服务不中断）：直接从宿主机 volume 路径 tar
    vols_out, _ = ssh_exec(client, "docker volume ls --format '{{.Name}}' | grep weknora")
    volumes = [v.strip() for v in vols_out.splitlines() if v.strip()]
    for vol in volumes:
        cmd = (
            f"MP=$(docker volume inspect -f '{{{{.Mountpoint}}}}' {vol}); "
            f"tar czf {bdir}/volumes/{vol}.tar.gz -C \"$MP\" . 2>/dev/null; "
            f"echo {vol}:$(du -h {bdir}/volumes/{vol}.tar.gz | cut -f1)"
        )
        out, e = ssh_exec(client, cmd)
        print("卷快照:", out.strip(), e.strip())

    # 5) 汇总
    summ, _ = ssh_exec(client, f"du -sh {bdir}; echo '---'; ls -lhR {bdir}")
    print("==== 备份汇总 ====")
    print(summ)

    client.close()


if __name__ == "__main__":
    main()
