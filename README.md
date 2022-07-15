# lazypeon
 a basic pentesting cheat sheet generator

## about
If you're anything like me: you try to remember methodologies & techniques, and not the 100's (1000's?, 10000's?, ...) of commands necessary during pentesting/offsec/infosec work and play. You know *how* to do what you need to, but you don't have the bandwidth to keep all of the specifics of commands, reverse shells, etc. in working memory all day. Enter: The Lazy Peon. 

This is a simple script that outputs cheat sheets for regularly used commands in pentesting/ctf scenarios. It can be ran without arguments, just to get easy access to copy and paste the commands, or with arguments to get those cheat sheets pre-populated with whatever target or localhost you're currently working with. This way, I don't have to repeatedly open up google and type terribly long things like 'pentest monkey reverse shell cheatsheet.' A second saved is ... *well* ... a second saved.

## requirements
I tried to keep things simple and efficient. This just utilizes colorama, which my kali install had already, but yours may not so you can just run the follow command to get the requirements:

```pip install -r requirements.txt```

## currently available stuff & things

### Recon Command Cheat Sheet Generator
Generates a cheat sheet with very common recon and enumeration commands, such as: feroxbuster, dirbuster, ffuf, nmap, and smbclient

### Reverse Shells Cheat Sheet Generator
Literally just all the reverse shells available at https://pentestmonkey.net/cheat-sheet/shells/reverse-shell-cheat-sheet, but now they can be preopulated with an IP and PORT. No more copy pasting from the site to a text editor, putting in your IP/PORT, and then copy/pasting the constructed payload.

### Misc Commands Cheat Sheet Generator
Miscellaneous commands/data that don't fit into the above two categories here. Fun stuff like starting up your Nessus instance. Also has a bunch of TTY spawning commands.

## License
MIT Open Source . . . blah blah
Feel free to modify and whatever. Credit would be nice

## adoration, questions, concerns, or hatemail?
Direct that stuff here: twitter@mox_folder

## ToDo
- Clean, optimize, and comment the code (was rushing to get this out before htb's 2022 business ctf, so it's messy and uncommented)
- Come up with those cool icons/banners/images to put on here like all the other cool scripts have on their github repos
- ~~Figure out the meaning of life in this vast universe~~
