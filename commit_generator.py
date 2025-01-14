import os
import subprocess
from datetime import datetime, timedelta

# Set the start and end date
start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 12, 31)
repo_path = os.getcwd()  # Assumes it's executed inside the Git repo

# Ensure we're in a git repository
if not os.path.exists(os.path.join(repo_path, ".git")):
    print("Error: This is not a git repository.")
    exit(1)

# Dummy file for commits
commit_file = os.path.join(repo_path, "commit_log.txt")

# Open the file (create if not exists)
if not os.path.exists(commit_file):
    with open(commit_file, "w") as f:
        f.write("Commit Log:\n")

current_date = start_date
while current_date <= end_date:
    formatted_date = current_date.strftime("%Y-%m-%d %H:%M")

    # Append a line to the file
    with open(commit_file, "a") as f:
        f.write(f"Commit on {formatted_date}\n")

    # Git commands
    subprocess.run(["git", "add", commit_file], check=True)
    subprocess.run(["git", "commit", "-m", f"Daily commit {formatted_date}"], check=True)

    # Amend commit date
    env = os.environ.copy()
    env["GIT_COMMITTER_DATE"] = formatted_date
    subprocess.run(
        ["git", "commit", "--amend", "--no-edit", f"--date={formatted_date}"],
        check=True,
        env=env,
    )

    print(f"Committed for {formatted_date}")

    # Move to the next day
    current_date += timedelta(days=1)

print("All commits completed.")
