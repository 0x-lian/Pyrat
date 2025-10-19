"""Template module for Pyrat"""
def run(args):
    t=getattr(args,"target",None)
    print("[template] target:",t)
if __name__=="__main__":
    class A: pass
    a=A(); a.target="127.0.0.1"
    run(a)
