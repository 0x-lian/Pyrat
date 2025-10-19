#!/usr/bin/env python3
import argparse, os, sys, importlib
MODULES_DIR = os.path.join(os.path.dirname(__file__), "modules")
def discover_modules():
    mods=[]
    if not os.path.isdir(MODULES_DIR): return mods
    for f in os.listdir(MODULES_DIR):
        if f.endswith(".py") and not f.startswith("_"):
            mods.append(f[:-3])
    return mods
def run_module(name,args):
    sys.path.insert(0, MODULES_DIR)
    try:
        m=importlib.import_module(name)
        if hasattr(m,"run"):
            m.run(args)
        else:
            print(f"Module {name} has no run(args)")
    except Exception as e:
        print("Error:",e)
if __name__=="__main__":
    p=argparse.ArgumentParser(); p.add_argument("--list",action="store_true"); p.add_argument("--run"); p.add_argument("--target")
    a=p.parse_args()
    if a.list:
        print("Available modules:"); print("\\n".join(discover_modules()) or "(none)")
    elif a.run:
        run_module(a.run,a)
    else:
        print("Use --list or --run <module>")
