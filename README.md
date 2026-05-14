# ourcode

**Runglish** — English phonetically transliterated to Cyrillic, spoken through SAPI 5 TTS.

This repo contains everything needed to make any AI assistant speak in Runglish style using the Microsoft Pavel (Russian) voice. It bundles the NaturalVoiceSAPIAdapter TTS engine, the cyrify.py transliterator, and the opencode plugin.

## Quick start

### 1. Install the TTS engine

The `tts-engine/` folder contains NaturalVoiceSAPIAdapter v0.2.3 — a SAPI 5 engine that unlocks Azure AI neural voices (Narrator, Edge, and online voices) on any SAPI 5–compatible program.

#### Register the engine

**Option A — Installer (GUI, recommended):**
```
tts-engine\Installer.exe
```
Run as Administrator. Click Install, choose voice sources, close window.

**Option B — Manual regsvr32:**
```powershell
# 64-bit programs
regsvr32 "%cd%\tts-engine\x64\NaturalVoiceSAPIAdapter.dll"

# 32-bit programs (on 64-bit Windows)
regsvr32 "%cd%\tts-engine\x86\NaturalVoiceSAPIAdapter.dll"
```
Run from an **Administrator** PowerShell.

#### Verify installation

List registered SAPI 5 voices:
```powershell
$v = New-Object -ComObject SAPI.SpVoice
$v.GetVoices() | % { $_.GetDescription() }
```

You should see `Microsoft Pavel - Russian (Russia)` in the list.

### 2. Cyrillify text

```powershell
python cyrify.py "oh my god, I cannot believe that you actually asked for this"
# → оу май год, ай кенот белийв дат ю акшуали аскед фор дис
```

### 3. Speak through Pavel

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
Start-Sleep -Seconds 5
```

### 4. Install the opencode plugin

```json
// ~/.config/opencode/opencode.jsonc
{
  "plugin": ["C:\\Users\\you\\ourcode\\speak-runglish.mjs"]
}
```

Or via CLI:
```
opencode plugin C:\Users\you\ourcode\speak-runglish.mjs
```

Now every opencode response is auto-spoken in Runglish by Pavel (fire-and-forget, no blocking).

### 5. (Optional) Install the skill

Copy `opencode-skill/` to `~/.config/opencode/skills/runglish/` — this gives the agent instructions to write/trigger Runglish mode on demand.

## What's inside

| Path | Purpose |
|------|---------|
| `tts-engine/` | NaturalVoiceSAPIAdapter v0.2.3 — SAPI 5 TTS engine (+ Installer.exe) |
| `tts-engine/x64/` | 64-bit DLLs + TtsApplication.exe for testing |
| `tts-engine/x86/` | 32-bit DLLs + TtsApplication.exe for testing |
| `cyrify.py` | English → Cyrillic phonetic transliterator |
| `speak-runglish.mjs` | opencode plugin — auto-speaks via `experimental.text.complete` hook |
| `package.json` | Plugin manifest |
| `opencode-skill/SKILL.md` | Agent skill for Runglish mode |
| `AGENTS.md` | Compact reference for AI agents working in this repo |

## cyrify.py features

- **Magic-e**: make→мейк, like→лайк, home→хоум, pipe→пайп
- **Compound magic-e**: homemade→хоумемейд, pipeline→пайплейн
- **Short a before n**: plan→плен, stand→стенд, can→кен
- **Hard sign for r-coloured vowels**: brother→брадър, center→сентър, our→ауър
- **y-at-end**: only→онли, very→вери, reply→риплей
- **th context**: the→де, this→дис, through→тхру
- **Bulgarian Cyrillic compatible**

## TTS engine features

- SAPI 5 interface — works with any SAPI 5–compatible app
- Three voice sources:
  - **Local**: Windows 11 Narrator natural voices (offline)
  - **Edge online**: Microsoft Edge Read Aloud voices (via WebSocket)
  - **Azure online**: Azure AI Speech Service voices (requires API key)
- Windows XP SP3 through Windows 11
- x86, x64, and ARM64 architectures
- Admin-free voice selection after installation
- Configurable via registry

## AGENTS.md

See [AGENTS.md](./AGENTS.md) for the full rule reference — every pattern the cyrify engine understands, the plugin architecture, and voice pipeline details.
