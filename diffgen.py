import os
import subprocess
from datetime import datetime, timedelta

filename = "count.txt"
start_date = datetime(2008, 4, 3)
end_date = datetime.now()

def run(cmd, env=None):
    result = subprocess.run(cmd, capture_output=True, text=True, env=env)
    if result.returncode != 0:
        print(f"Error running {' '.join(cmd)}: {result.stderr}")
        exit(1)
    return result.stdout.strip()

if not os.path.exists(".git"):
    print("Initializing new git repo...")
    run(["git", "init"])

with open(filename, "w") as f:
    f.write("0\n")

run(["git", "add", filename])
env = os.environ.copy()
env["GIT_COMMITTER_DATE"] = start_date.strftime("%Y-%m-%d 12:00:00")
env["GIT_AUTHOR_DATE"] = start_date.strftime("%Y-%m-%d 12:00:00")
commit_msg = "Count is now 0"
tree = run(["git", "write-tree"])
commit = run(["git", "commit-tree", tree, "-m", commit_msg], env=env)
print(f"[0] Commit created with date {start_date.strftime('%Y-%m-%d')} and hash {commit}")

current_date = start_date + timedelta(days=1)
count = 1

while current_date <= end_date:
    with open(filename, "w") as f:
        f.write(f"{count}\n")

    tree = run(["git", "write-tree"])
    date_str = current_date.strftime("%Y-%m-%d 12:00:00")
    env["GIT_COMMITTER_DATE"] = date_str
    env["GIT_AUTHOR_DATE"] = date_str
    commit_msg = f"Count is now {count}"

    commit = run(["git", "commit-tree", tree, "-p", commit, "-m", commit_msg], env=env)
    print(f"[{count}] Commit created with date {current_date.strftime('%Y-%m-%d')} and hash {commit}")

    current_date += timedelta(days=1)
    count += 1

run(["git", "update-ref", "refs/heads/master", commit])
print("All done! History is now fully time-traveled and logged.")
