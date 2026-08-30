# Task 01 — Git Exercises

- This task was basically a collection of Git exercises.
- The main thing I learned was how Git history works and how we can change, recover, and manage it.
- I learned many Git commands by actually using them instead of just reading about them.

## Commands I Used

- `git merge another-piece-of-work` — joins another branch with the current branch.
- `git add <file>` — adds a file or changes to the staging area.
- `git commit` — saves the staged changes as a commit.
- `git stash` — temporarily keeps unfinished changes aside.
- `git stash pop` — brings the stashed changes back.
- `git commit -m "message"` — creates a commit with a message.
- `git commit --amend` — changes the latest commit.
- `git commit --amend -m "message"` — changes the latest commit and its message.
- `git commit --amend --date="..." --no-edit` — changes the commit date without changing its message.
- `git rebase hot-bugfix` — moves branch changes on top of another branch.
- `git rebase -i <commit>` — lets me edit, reorder, squash, or change old commits.
- `git rebase --continue` — continues a rebase after fixing a problem.
- `git rm --cached ignored.txt` — stops tracking a file but keeps it on the computer.
- `git mv File.txt file.txt` — renames a file through Git.
- `git reflog` — shows where `HEAD` has been and helps find lost commits.
- `git reset --hard <commit>` — moves the current branch back to a commit and resets the working files.
- `git reset HEAD^` — moves back one commit while keeping the changes unstaged.
- `git reset --soft HEAD~1` — moves back one commit while keeping the changes staged.
- `git add -p file.txt` — lets me choose which parts of a file I want to stage.
- `git update-index --chmod=+x script.sh` — makes Git remember that a script should be executable.
- `git cherry-pick feature-a` — brings a specific commit from another branch into the current branch.
- `git cherry-pick feature-b` — brings another selected commit into the current branch.
- `git cherry-pick <C1-hash>^..feature-c` — brings a range of commits into the current branch.
- `git cherry-pick --continue` — continues cherry-picking after fixing a conflict.
- `git log --oneline -S shit -- words.txt list.txt` — finds commits where a specific word was added or removed.
- `git bisect start` — starts a search for the commit that introduced a bug.
- `git bisect bad HEAD` — tells Git that the current commit has the bug.
- `git bisect good 1.0` — tells Git that an older commit was working.
- `git bisect run <command>` — lets Git automatically test commits while searching for the bug.
- `git bisect reset` — ends the bisect process and returns to the normal branch.
- `git log --oneline --graph --all` — shows the commit history and branches in a simple graph.
- `git push origin <commit-hash>:find-bug` — pushes a selected commit to a remote branch.

## Issues I Faced

- I made a small typo in a file, and the checker rejected it because the content had to be exact.
- I accidentally left extra test content in a file.
- I accidentally created an extra commit while trying to amend a commit.
- I forgot to include `program.txt` in the final commit.
- I changed a commit message correctly but forgot to actually fix the file content.
- A rebase caused a merge conflict because the file had changed after the old commit was edited.
- Cherry-picking two features caused a merge conflict.
- Interactive staging with `git add -p` became confusing when multiple changes were mixed together.
- I accidentally added duplicate lines while trying to split changes into separate commits.
- I had to check `git log` and `git reflog` several times to understand where my commits actually were.
- The Git history exercises made me realize that changing history can easily change commit hashes and branch positions.

## What I Learned

- Git is not just about uploading code.
- A commit is a snapshot in the project's history.
- Branches are basically different timelines of the same project.
- Rebase can change the shape of the history.
- Reflog can help recover commits that look lost.
- Stash is useful when I need to temporarily put unfinished work aside.
- Cherry-pick lets me take only the changes I actually want.
- Interactive rebase is useful for cleaning and changing local history.
- `git bisect` can find a bad commit much faster than checking hundreds of commits one by one.
- Small mistakes matter a lot in Git exercises because the final file content and history can be checked exactly.

## Final Takeaway

- The biggest thing I got from these exercises is that Git history is something I can actually work with, not just something Git stores automatically.
- I learned how to create history, move through it, change it, recover it, and investigate it.
- This made Git much more interesting to me than just using `git add`, `git commit`, and `git push`.
