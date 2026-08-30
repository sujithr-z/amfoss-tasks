## Level 1

For Level 1, there were many folders containing copies of the same files, but only one of them had the actual Devil Fruit.

First, I opened the `eat.sh` bash script to understand what condition the correct fruit had to satisfy. I found that the script checks whether the given file is **executable** using the `-x` condition.

So I went through the folders and used:

```bash
ls -la
```

This helped me see the permissions of the files. Since `x` means executable, I looked for the file that had the executable permission. I found the fruit file this way and used it with `eat.sh` to complete Level 1.

Overall, the main thing I learned from this level was to first understand the script and then use Linux file permissions to find what I was looking for.