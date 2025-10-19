#!/usr/bin/env python3
"""Simple discovery module: ping-sweep and save results to logs/ as JSON."""
import argparse, subprocess, json, os, datetime, sys

def ping_host(host):
    try:
        ret = subprocess.run(["ping","-c","1","-W","1", host],
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return ret.returncode == 0
    except Exception:
        return False

def run(args):
    target = getattr(args, "target", None)
    if not target:
        print("No target provided. Use --target 192.168.1.0/24 or single host.")
        return

    hosts = []
    if "/" in target:
        base = target.split("/")[0]
        parts = base.split(".")
        if len(parts) == 4:
            prefix = ".".join(parts[:3])
            hosts = [f"{prefix}.{i}" for i in range(1,255)]
        else:
            print("Unsupported CIDR format.")
            return
    else:
        hosts = [target]

    print(f"[discovery] scanning {len(hosts)} hosts (this may take a while)...")
    alive = []
    for h in hosts:
        if ping_host(h):
            print(f"[+] {h} is alive")
            alive.append(h)

    os.makedirs("logs", exist_ok=True)
    fn = datetime.datetime.now().strftime("logs/discovery_%Y%m%d_%H%M%S.json")
    with open(fn,"w") as f:
        json.dump({"target":target,"alive":alive,"scanned":len(hosts),
                   "timestamp":datetime.datetime.now().isoformat()}, f, indent=2)

    print(f"[discovery] done. {len(alive)} hosts alive. Log: {fn}")

if __name__ == "__main__":
    class A: pass
    a = A(); a.target = "127.0.0.1"
    run(a)
