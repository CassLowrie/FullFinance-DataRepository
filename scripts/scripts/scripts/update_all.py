import subprocess
import sys

def run(cmd):
    print(f"$ {' '.join(cmd)}")
    res = subprocess.run(cmd, check=False)
    if res.returncode != 0:
        print(f"!! Command failed: {' '.join(cmd)}")
        sys.exit(res.returncode)

def main():
    # Update FRED & World Bank datasets
    run([sys.executable, "scripts/fetch_fred.py"])
    run([sys.executable, "scripts/fetch_worldbank.py"])

if __name__ == "__main__":
    main()
