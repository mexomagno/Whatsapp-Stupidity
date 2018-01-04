# Whatsapp-Stupidity
Completely useless random text formatting for whatsapp web messages.

Whatsapp supports mild formatting, such as **bold**, _italic_ and ~~strikeout~~...
Then why not write _every single character_ with format!

There's no doubt "hello world" looks better as "_h_ **e** ~~l~~ l _o_   ~~w~~ o _r_ **l** ~~d~~" :wink:


## Example:

#### Arguments mode

```shell
$ ./stupidify "hello world"
Success! Ctrl+V in whatsapp web to paste  # _h_ *e* ~l~ l _o_   ~w~ o _r_ *l* ~d~
$ ./stupidify hello world
Success! Ctrl+V in whatsapp web to paste  #  _h_ *e* ~l~ l _o_   ~w~ o _r_ *l* ~d~
$
```

#### Prompt mode

```shell
$ ./stupidify
Your text here (Ctrl+D or ESC to exit) >>> hello world  # Enter
Your text: 'hello world'
Success! Ctrl+V in whatsapp web to paste  # _h_ *e* ~l~ l _o_   ~w~ o _r_ *l* ~d~
Your text here (Ctrl+D or ESC to exit) >>> # Ctrl+D
Quitting...
$ 
```

# Features
* Bash-like prompt history. Navigate up and down through your previous entries
* Auto clipboard copy
* Oh god I don't even know why I did this

# Requirements
* Python 2.7
* see requirements.txt
* Linux machine
* xclip (available from apt for debian)

# Known issues
* When line exceeds the window width, multiple lines are printed for every additional character, although this does not affect the actual input

# TODO
* Map Ctrl+C to quit 
* Fix known issues
* Test on other platforms
* Word jumps with CTRL left, right, and delete
* Paste with Ctrl+Shift+V instead of Ctrl+V
* Maxi fuckup, like **cAmElCaSe**, [**l33tsp34k**](https://www.urbandictionary.com/define.php?term=l33t) and true randomization