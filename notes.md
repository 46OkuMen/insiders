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