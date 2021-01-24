# ScummBack

ScummBack is a simple script to extract the embedded resource file from the 
re-releases of several LucasArts games:

- Indiana Jones and the Last Crusade
- Indiana Jones and the Fate of Atlantis
- Loom
- The Dig

This script should work on both Windows and Mac versions from most if not all 
releases (Steam, Humble, Discord).

## Usage

The script takes 3 arguments:

```
--game  - A short identifier of the game to extract. 
          Accepted values: loom, indy3, indy4, dig
--exe   - Path to the game Executable
--out   - Optional output path, by default the script will output to the current
          working path
```

Example:

```sh
python3 scummback.py --game indy4 --exe '.\Indiana Jones and the Fate of Atlantis.exe' --out 'ATLANTIS'
````
