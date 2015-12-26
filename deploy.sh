#!/bin/bash
set -ev # exit with nonzero exit code if anything fails

# go to the out directory and create a *new* Git repo
cd gh-pages

# inside this git repo we'll pretend to be a new user
git config user.name "gramps_example_reports"
git config user.email "gramps@example.com"

# The first and only commit to this new Git repo contains all the
# files present with the commit message "Deploy to GitHub Pages".
git add .
git commit -m "Deploy example reports to GitHub pages"

# Force push from the current repo's master branch to the remote
# repo's gh-pages branch. (All previous history on the gh-pages branch
# will be lost, since we are overwriting it.) We redirect any output to
# /dev/null to hide any sensitive credential data that might otherwise be exposed.
echo "Pushing to the repository: github.com/${EXAMPLES_REPO_SLUG}.git"
# git push --quiet "https://${GH_TOKEN}@github.com/${EXAMPLES_REPO_SLUG}.git" gh-pages:gh-pages > /dev/null 2>&1
