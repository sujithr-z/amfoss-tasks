## Level 5 – The Buster Call Timeline Recovery 

For Level 5, the statement says to **walk backward through time** and mentions that the two Poneglyph fragments have no meaning individually and need to be restored together.

So I started by checking the Git history using:

```bash id="z3v3fa"
git log --oneline --all --graph
```

From the history, I found the Level 5 branch and went into the relevant commit. There was a Python file called `poneglyph.py`, which looked like it was made for decoding the fragments.

I checked the Python code and understood that it takes a Base64-encoded input, decodes it, and then applies an XOR operation using `0x42` to every byte.

I then took the **Fragment I** from Level 3 and **Fragment II** from Level 4, joined them together in the correct order, and used the Python script to decode them.

After decoding the combined fragments, I successfully got the **link for Level 6**.

This level was fairly easy for me because the story directly hinted at going into the past, which made Git history the obvious place to investigate. The main thing I learned was how information found separately in previous levels can become meaningful when combined later.