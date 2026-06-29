Scenario 1: Push a project to a NEW EMPTY GitHub Repository (Recommended)
# Check status
git status

# Initialize Git (if not already initialized)
git init

# Add all files
git add .

# Commit files
git commit -m "Initial project commit"

# Rename branch to main
git branch -M main

# Add GitHub repository
git remote add origin https://github.com/<username>/<repository>.git

# Push to GitHub
git push -u origin main

Scenario 2: Change to another GitHub Repository

# Remove old remote
git remote remove origin

# Add new remote
git remote add origin https://github.com/<username>/<new-repository>.git

# Push
git push -u origin main
Scenario 3: Remote repository already has a README (Push is rejected)
Option A (Overwrite the remote)
git push -u origin main --force
Option B (Merge both histories)
git pull origin main --allow-unrelated-histories

git push -u origin main
Scenario 4: Check the configured remote
git remote -v
Scenario 5: Check current branch
git branch
Scenario 6: Check repository status
git status
Scenario 7: View commit history
git log --oneline
Scenario 8: Push latest changes after editing files
git add .

git commit -m "Updated project"

git push
Scenario 9: Pull latest changes from GitHub
git pull origin main
Scenario 10: Clone an existing repository
git clone https://github.com/<username>/<repository>.git
Scenario 11: First-time setup for a new project
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/<username>/<repository>.git
git push -u origin main
Scenario 12: If you accidentally typed the wrong remote
git remote remove origin
git remote add origin https://github.com/<username>/<repository>.git
Most Common Commands (Remember These)
git status
git add .
git commit -m "Your commit message"
git push
git pull
git branch
git remote -v

This set of commands covers about 95% of day-to-day Git operations you'll use in data science projects and software development.