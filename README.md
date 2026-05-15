                    ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
                    █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█
                    █  П Р О Л Е Т А Р И И  В С Е Х  █
                    █  С О Е Д И Н Я Й Т Е С Ь  !    █
                    █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█
                    ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀

                    ╔═══════════════════════════╗
                    ║  O U R C O D E  v1.0.0  ║
                    ║   CCCP  ·  1984  ·  TTS  ║
                    ╚═══════════════════════════╝

                           ★  ★  ★  ★  ★

                    ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
                    РУНГЛИШ — ГОЛОС ПРОЛЕТАРИАТА
                    ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░


**Runglish** — English phonetically transliterated to Cyrillic, spoken through SAPI 5 TTS.
The voice of the people. The voice of the revolution. The voice of Comrade Pavel.

This repository contains everything necessary to make any AI assistant speak in proper
proletarian Runglish style using the glorious **Microsoft Pavel (Russian)** voice.
It bundles the **NaturalVoiceSAPIAdapter** TTS engine, the **cyrify.py** transliterator,
and the **opencode** plugin — a complete armament for the working programmer.


═══════════════════════════════════════════════════════════════════
           П Я Т И Л Е Т К А  —   F I V E  Y E A R  P L A N
═══════════════════════════════════════════════════════════════════

## ★ Step 1 — Install the TTS Engine

The `tts-engine/` folder contains NaturalVoiceSAPIAdapter v0.2.3 — a SAPI 5 engine
that liberates Azure AI neural voices (Narrator, Edge, online) from capitalist
software restrictions onto any SAPI 5–compatible program.

### Register the Engine

**Option A — Installer (GUI, recommended for comrades):**
```
tts-engine\Installer.exe
```
Run as Administrator. Click Install. Choose voice sources. Close window. Glory to labour.

**Option B — Manual regsvr32 (for the Party elite):**
```powershell
regsvr32 "%cd%\tts-engine\x64\NaturalVoiceSAPIAdapter.dll"
regsvr32 "%cd%\tts-engine\x86\NaturalVoiceSAPIAdapter.dll"
```
Run from an **Administrator** PowerShell. The Party trusts you.

### Verify Installation

List registered SAPI 5 voices:
```powershell
$v = New-Object -ComObject SAPI.SpVoice
$v.GetVoices() | % { $_.GetDescription() }
```

You should see `Microsoft Pavel - Russian (Russia)` in the list.
The voice of the revolution is now available. Comrade Pavel reports for duty.


## ★ Step 2 — Cyrillify Text

```powershell
python cyrify.py "oh my god, I cannot believe that you actually asked for this"
→ оу май год, ай кенот белийв дат ю акшуали аскед фор дис
```

The bourgeois English letters are reeducated. They emerge as proper Cyrillic proletarians.


## ★ Step 3 — Speak Through Comrade Pavel

```powershell
$v = New-Object -ComObject SAPI.SpVoice
$voices = $v.GetVoices()
for ($i=0;$i -lt $voices.Count;$i++) {
  if ($voices.Item($i).GetDescription() -eq "Microsoft Pavel - Russian (Russia)") {
    $v.Voice = $voices.Item($i); break
  }
}
$v.Rate = -1
$v.Speak("оу май год, ай хир ю. дис из а лонгър тест.")
```

The voice of Pavel echoes across the motherland. Workers hear and understand.


## ★ Step 4 — Install the opencode Plugin

```json
// ~/.config/opencode/opencode.jsonc
{
  "plugin": ["C:\\Users\\you\\ourcode\\speak-runglish.mjs"]
}
```

Or via the Party CLI:
```
opencode plugin C:\Users\you\ourcode\speak-runglish.mjs
```

Every opencode response now automatically spoken in Runglish by Comrade Pavel.
Fire-and-forget. No blocking. No bureaucracy. Five-year plan completed ahead of schedule.


## ★ Step 5 — (Optional) Install the Skill

Copy `opencode-skill/` to `~/.config/opencode/skills/runglish/`.
This gives the agent instructions to write and trigger Runglish mode on demand.
Propaganda material for the machine intellect.


═══════════════════════════════════════════════════════════════════
      С Т Р У К Т У Р А   Р Е В О Л Ю Ц И О Н Н О Г О  К О Д А
═══════════════════════════════════════════════════════════════════

| Path                          | Purpose                                           |
|-------------------------------|---------------------------------------------------|
| `tts-engine/`                 | NaturalVoiceSAPIAdapter — SAPI 5 engine + Installer|
| `tts-engine/x64/`             | 64-bit DLLs + TtsApplication.exe                  |
| `tts-engine/x86/`             | 32-bit DLLs + TtsApplication.exe                  |
| `cyrify.py`                   | English → Cyrillic phonetic transliterator        |
| `speak-runglish.mjs`          | opencode plugin — auto-speaks via hook            |
| `package.json`                | Plugin manifest (for the Party records)           |
| `opencode-skill/SKILL.md`     | Agent skill for Runglish mode                     |
| `AGENTS.md`                   | Compact reference for AI comrades                 |


═══════════════════════════════════════════════════════════════════
   Д О С Т И Ж Е Н И Я   Н А У К И  И  Т Е Х Н И К И
═══════════════════════════════════════════════════════════════════

## cyrify.py — Scientific Achievements

- **Magic-e**: make→мейк, like→лайк, home→хоум, pipe→пайп
- **Compound magic-e**: homemade→хоумемейд, pipeline→пайплейн
- **Short a before n**: plan→плен, stand→стенд, can→кен
- **Hard sign for r-coloured vowels**: brother→брадър, center→сентър, our→ауър
- **y-at-end**: only→онли, very→вери, reply→риплей
- **th context**: the→де, this→дис, through→тхру
- **Bulgarian Cyrillic compatible** — international solidarity!

## TTS Engine — Industrial Capacity

- SAPI 5 interface — compatible with any SAPI 5–compliant industry
- Three voice sources:
  - **Local**: Windows 11 Narrator natural voices (offline — no foreign dependency)
  - **Edge online**: Microsoft Edge Read Aloud voices (via WebSocket)
  - **Azure online**: Azure AI Speech Service (requires Party approval — API key)
- Windows XP SP3 through Windows 11 — backward compatible, forward thinking
- x86, x64, ARM64 architectures — all fronts
- Admin-free voice selection after installation — democratic centralism
- Configurable via registry — Gosplan approved


═══════════════════════════════════════════════════════════════════
              Д А   З Д Р А В С Т В У Е Т  А Г Е Н Т  М Д
═══════════════════════════════════════════════════════════════════

See [AGENTS.md](./AGENTS.md) for the complete rule reference — every pattern the
cyrify engine understands, the plugin architecture, and the voice pipeline details.
Study it. Memorize it. Apply it in the service of the people.

```
     ███████████████████████████████████████████████████
     █                                                █
     █    ★  ★  СЛАВА  ТРУДУ!  ★  ★                 █
     █    ★  ★  МИР  ДРУЖБА  РУНГЛИШ!  ★  ★          █
     █                                                █
     ███████████████████████████████████████████████████
```

                    ★  ★  ★  ★  ★  ★  ★  ★  ★  ★
