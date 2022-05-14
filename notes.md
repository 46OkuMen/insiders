Intro: たった, at memory 31740

COMMAND.COM: A bunch of error messages and that's all
	A bunch of text at 680

	書込み禁止です.$ドライブの指定が違います.$ドライブの準備ができていません.$無効なコマンドです.$データエラーです.$要求形式が違います.$シークエラーです.$このディスクは使えません.$セクタが見つかりません.$用紙がありません.$書込みができません.$読取りができません.$エラーです.$共有違反です.$ロック違反です.$ディスク交換はできません.$FCBが使えません.$共有バッファに余裕がありません.$ディスクを差し込んでください.
	$<読取り中>$<書込み中>$$<ドライブ A:>
		$ デバイス

	$中止<A>, もう一度<R>, 無視<I>? $

	ファイルアロケーションテーブルが不良です.$
	COMMAND.COMのバージョンが違います.
	$
	 $の入ったディスクをカレントドライブに差し込み，
	どれかキーを押してください.
	$
	バッチ処理を中止しますか <Y/N>?

	 $実行できませんでした.
	$.EXEファイルのエラーです.
	$プログラムが大きすぎてメモリに入りません.
	$
	現在オープンされているファイルの数が多すぎます.$コマンドまたはファイル名が間違いです.
	$アクセスは拒否されました.
	$
	メモリのアロケーションエラーです.$


	COMMAND.COMをロードできません. リセットしてください.$
	COMMAND.COMをロードできません.
	$
	トップレベルのプロセスが中止されました. 続行できません.$

BOOK - explains various CS concepts, plaintext

ZNC - something

Decompressing opening text
	Char under consideration: 82 bd 82 c1, ta liltsu

EAX: 0d0a      EBX: b816   ECX: 3f5    EDX: 078d
15f4:74c6 8b07 mov ax, [bx]  ; (puts ba0f in eax)
push ax                      ; 08af on stack
xor ax, dx                   ; ax <- bd82
pop dx                       ; ba0f in edx
mov [bx], ax
inc bx
inc bx
loop 74c6

When it loads from [bx], this might be the text that was just written?
And when it writes to [bx], that is the next text. (That's how it writes to the dest memory)

**These memory accesses are done with DS:[bx], NOT CS:[bx]**
(That's probably why I never successfully traced any memory operands!)

It does this from the very beginning of a recognizable "structure" at $30f40

Beginning of file at 0x25f40
31740 - 25f40 = b800

eax: holds current memory contents
ebx: program offset counter
edx: xor thing

Slight rearrangement:

push ax
ax = ax XOR dx
pop dx
memory[bx] = ax
bx += 2
ax = memory[bx]
loop

Each value gets xor'd with the uncompressed value right before it?

Typing text, scrolling text, post-title screen text all seem to be in IDS

Sphinx text is at 3e5f0~
	ISS location 8400 gets loaded into memory at location 3e340.
	3e340 - 8400 = 35f50~

Considerations: When there's a long block of stuff AFTER some text I want to replace, like "33 A6 33 A6...", I may need to replace this with something that makes it zero out (or 55 out) in the plaintext...

IDS appears to decompress starting at 0x2800. (memory 28740)
Bytes 1f-20 are 00 28.

So where does EDX get initialized?
	5a4b doesn't show up anywhere, but 4b5a shows up:
		at 0x2805
		at 0x2809
		at 0x3223
	5a4b also shows up at the beginning of ISS

ISS gets loaded into memory starting at 35f50.
	EAX is 0000, EDX is 4b5a again.

Possibilities:
	EDX is always 4b5a
	EDX is set to [bx+5]

FILES WITH TEXT:
	ISS (compressed)
	IDS (compressed)
		Interface text, actions, etc. at 0x3400
		Post-title screen intro text at 0xb800
	IS2 (compressed)
	ALD (compressed)
	AMD (compressed)
	BKD (compressed)
	CPU (compressed)
	DAT1 (compressed)
	BOOK (not compressed)

OTHER FILES:
	ALC (?)
	BASM ("MAP1")
	BASP (?)
	BKC (?)

# More notes
* Some blocks are spaced out with UUUUUUUUUUUU's. Those can probably be reclaimed to get more space for stuff.
	* I can subclass Block to get a method to look ahead a bit, and figure out how many UUU's can be replaced if a block is too long.
* I think [=] should be a control code, since the dumps are freaking Excel out whenever a string starts with one.
	* Treated it in the dumper, need to treat it in the reisnerter.
* What is the code that appends another JP ... to the "press z" instruction? Need to replace that.
* Insiders manual and map are included in Neo Kobe, but as part of Insiders 2 (Network no Bouken).
	* Not the giant book we had heard about, but probably good enough if we can't find that.

# 88 version
* Insiders '88 appears a lot simpler in structure. Seems like all the text is not encoded, and put in IN.COM.
	* But significantly less text? Is the game smaller or am I missing something?


## Coming back to this in 2022
* Reinserter looks to be basic.
	* Individual strings can have different lengths, but blocks need to have diff <= 0.
* Need to add support for control codes, start with [LN].
* How do pointers work in this game?
	* Pointers in the first scrolling text go to ba80, bab8, bae8, bb08, bb30, bb48.
		* Offsets: 0, 38, 68, 88, b0, c8
	* Text routine: Looks for 00, 0d, 1c, etc
	* Text at bab8 gets read, not the previous byte.
	* lodsb = load ds:si into al. (25f4:bae8 = 6c)
		* Where is SI getting set?
	* Looks like some numbers starting around 1a590 -
		  * 6d fd be [80 ba] e8 77 fd be [b8 ba] e8 71 fd be [e8 ba] e8 6b fd be [08 bb] e8 65 fd be [30 bb] e8 fd fd be 48 bb e8 59 fd 
		  * These are in the ICS (not IDS) base file and not the decompressed one. (3e5a)
		  	* ICS doesn't have any text. Let's mark it as uncompressed
* If we dump all the UUUUUU stuff, we can try replacing it and using it for text.