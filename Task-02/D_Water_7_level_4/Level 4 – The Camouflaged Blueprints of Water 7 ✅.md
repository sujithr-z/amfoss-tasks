## Level 4 – The Camouflaged Blueprints of Water 7

For Level 4, the statement says that names can be changed, but the true nature of something cannot. So I understood that I should find out what the file actually is instead of judging it by its name.

First, I went to the `Water_7` folder and used:

```bash
ls -la
```

There was one file called `puffing_tom_blueprints`. When I tried to read it using `cat`, it looked like complete gibberish and was not readable.

So instead of trying to read it directly, I checked its actual file type using:

```bash
file puffing_tom_blueprints
```

I found that it was a compressed file. I then started extracting it layer by layer. The first layer contained another archive, and inside that archive there was another ZIP file.

After extracting the layers step by step, I finally got two files: `secret_link.txt` and `frame_specs.dat`.

The `secret_link.txt` contained **PONEGLYPH_FRAGMENT_II**, which was the second fragment I was looking for. I added this fragment to my Logbook.

I found this level interesting because the file name made it look like a blueprint, but the `file` command helped me discover its actual nature. The main lesson for me was **not to judge a file by its name or extension, but to check what the file actually is**.