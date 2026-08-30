## Level 2 – The Two Faces of Whiskey Peak 

For Level 2, the story says that Whiskey Peak has another hidden history behind what we see. I took this as a hint that I should look into the **Git history** of the repository.

When I checked the `Whiskey_Peak` folder, I couldn't find anything useful apart from `feast_manifest.txt`. I also checked for hidden files, but nothing obvious was there. So I thought that maybe something had been deleted or changed in the past.

I used:

```bash
git log --oneline --all
```

This showed me the changes and branches in the repository. I noticed a separate branch related to the Whiskey Peak investigation, which felt like the "hidden timeline" mentioned in the story.

After investigating the Git history, I found a deleted/hidden executable file called `unlock_vault.sh`. I extracted the file from the old commit and checked its code.

The script required the **AWAKENING_SIGNATURE** I obtained from Level 1. After using the correct key, it unlocked two log files. These files looked almost identical, so I used:

```bash
diff marine_intercept.log bounty_hunter_feed.log
```

The `diff` command showed that there was only one important difference between the two reports. That difference contained the hidden Executive Transmission Code/flag.

### What I learned

The main lesson from this level was that the current working directory does not always contain everything in a Git repository. If the story suggests a **hidden history**, checking Git branches and previous commits can reveal files and information that are no longer visible in the current version.