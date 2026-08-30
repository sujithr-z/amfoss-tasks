
what even is this? 🤔
InvX2 is a clean, terminal-based shop inventory system that doesn't look like it's from the 90s. built with Python and the Rich library, it makes managing products actually enjoyable (yeah, we said it).
no databases, no complicated setup, no bs. just fire it up and start tracking your stuff.

features that slap 🔥

    aesthetic af terminal UI - forget ugly CLIs, we got colors and animations
    sick intro animations - three different styles because choices >>> no choices
    product management - add/delete items like you're playing a game
    price calculator - calculate bills with style (literally)
    inventory browser - see everything at a glance
    command-based interface - type commands like a hacker in a movie

    
screenshots (trust us, it looks good) 📸
    
<img width="1917" height="1015" alt="Invx" src="https://github.com/user-attachments/assets/e8b93f7e-9175-4ba6-8884-47042dcfb05e" />


installation (super easy, dw) ⚡
prerequisites

    Python 3.8+ (if you don't have this in 2025, install recent version in your timeline)
    pip (it comes with Python, you're good)

setup

    # clone this bad boy
    git clone https://github.com/sujith-cmd-IEEE/InvX2.git
    cd InvX2
    
    # install the only dependency (we kept it minimal fr)
    pip install rich
    
    # run it and vibe
    python shop_database.py

    #or using this command 
    py -3.13 shop_database.py
    #-3.13 is version of python

    
how to use 🎮
starting up
just run the main file and you'll see a fire intro animation (customize it later if you want)

    python shop_database.py
    # or using this 
    py -3.13 shop_database.py
   

### commands you'll actually use

| Command | What it does | Vibe Check |
|---------|-------------|-----------|
| `show table --info` | view your entire inventory | 👀 see everything |
| `ALT table --add` | add new products | ➕ stock up |
| `ALT table --del` | delete products | 🗑️ clean slate |
| `open price-cal --` | open the pricing calculator | 💰 calculate bills |
| `sys setting --intro_animation` | change intro style | 🎨 customize |
| `help` | show all commands | 📖 when you forget |
| `quit` | exit the program | 👋 peace out |

### adding products

```bash
$ ALT table --add
$ add
Enter product name: Gaming Mouse
Enter price for Gaming Mouse: $49.99
✓ Added Gaming Mouse at $49.99
```

### calculating prices

```bash
$ open price-cal --

# then in the calculator:
$ add                    # add items to bill
$ inventory              # browse products
$ view                   # see current bill
$ finish                 # calculate total
$ quit                   # go back
```

### customizing intro

```bash
$ sys setting --intro_animation
$ change intro=1         # animated intro
$ change intro=2         # fancy intro  
$ change intro=3         # simple intro
```

## file structure 📁

```
InvX/
│
├── shop database.py          # main program (the brain)
├── shop_excute.py           # price calculator module
├── animation_shop_intro.py  # intro animations (the drip)
└── README.md                # you're reading it bestie
```

## tech stack 💻

- **Python 3.13** - the language of choice
- **Rich** - makes the terminal look fire
- **your terminal** - CMD, PowerShell, whatever you got

## default products (sample data) 🎁

comes pre-loaded with 10 products so you can test it immediately:

- Wireless Mouse - $24.99
- USB-C Cable - $12.50
- Laptop Stand - $45.00
- Mechanical Keyboard - $89.99
- Bluetooth Headphones - $67.50
- Phone Case - $15.99
- Portable Charger - $32.00
- HDMI Cable - $9.99
- Webcam HD 1080p - $55.00
- Desk Lamp LED - $28.75

(you can delete these and add your own obvs)

## tips & tricks 💡

- commands are **case-sensitive** (yeah, we know)
- press `Ctrl+C` if something's taking too long
- type `help` literally anytime you're lost
- the intro animation runs every time you reset the system (it's a feature not a bug)
- prices automatically format to 2 decimal places (you're welcome)

## coming soon (maybe) 🚀

- [ ] save data to file (currently resets on close)
- [ ] export bills to PDF
- [ ] dark mode??? (jk it's already dark mode)
- [ ] more intro animations
- [ ] sound effects (if we're feeling crazy)


## why we built this 🎯

because every inventory system out there either:
- looks like it's from 1995
- costs money
- all of the above

we said nah, let's make something that just *works* and looks good doing it.

## license 📄

Apache License - do whatever you want with it, just don't blame us if something breaks

## support ☕

if this helped you out and you're feeling generous:

⭐ star this repo (it's free and makes us happy)

---

made with 💙 and way too much caffeine

*last updated: december 2025*

**now stop reading and go try it out fr fr** 🚀
