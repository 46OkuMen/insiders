## insiders
![Insiders title screen](img/title.png)
Romhacking notes and utilities for 46 OkuMen's upcoming translation of Michiaki Tsubaki's 'Maou Halton no Wana - Insiders - Pasokon Naibu e no Tabi', an educational RPG for the PC-98 about computer science.

### Usage
Place your dump of INSIDERS '94 into the 'original' folder. Extract the files from the dump using DiskExplorer or NDC.
Use codec.py to decompress the files into 
```
python dump.py
```

Translate the game with insiders_dump.xlsx.
```
python reinsert.py

```

### Scripts
* dump.py - dumps text into insiders_dump.xlsx.
* reinsert.py - reinserts translated text.

### Scripts used above
* rominfo.py - map of text blocks within files.
* codec.py - functions to encode/decode text in the game files.

### Notes
* Most game files are "compressed" (obfuscated) with a binary XOR routine described in codec.py. The reinserter re-encodes the files.
* There are two releases of this game, from 1988 and 1994. This patch targets the 1994 re-release.
	* Not entirely sure what the differences are, plan to investigate this. '88 has a blue logo title screen and '94 has a larger red logo title screen.