---
name: runglish
description: >
  When active, every response is spoken aloud in Runglish (Cyrillic phonetic
  approximation) through the Microsoft Pavel SAPI 5 voice, while the text
  response stays in normal English.
---

## Behavior

For every response:

1. Write reply in normal English.
2. Auto-invoke the speak script at the end:
   ```powershell
   echo "your english text" | powershell -File speak_runglish.ps1
   ```
   Or pipe directly via bash tool:
   ```powershell
   $dir = "C:\Users\kristian\Downloads\NaturalVoiceSAPIAdapter_v0.2.3_x86_x64\x64\NaturalVoiceSAPIAdapter"
   echo "your english text" | powershell "$dir\speak_runglish.ps1"
   ```

## Trigger

- User writes in Runglish style → auto-activate.
- Manual: "speak it", "say it", "voice it"
- Deactivate: "english only", "stop voice"

## Files

| File | Path |
|------|------|
| `cyrify.py` | repo root |
| `speak_runglish.ps1` | repo root |
| `AGENTS.md` | repo root |
