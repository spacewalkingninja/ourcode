# ourcode — Runglish plugin for opencode

## Files

- `cyrify.py` — English→Cyrillic transliterator. Run: `python cyrify.py "text"`
- `speak-runglish.mjs` — opencode plugin (hooks `experimental.text.complete`)
- `opencode-skill/SKILL.md` — agent skill that tells the LLM to speak Runglish

## cyrify.py rules

Two-pass engine: regex context rules → literal longest-match substitutions.

### Vowel rules (regex pass)
| Pattern | Cyrillic | English words |
|---------|----------|---------------|
| `i + C + e\b` | ай | like, time, ride |
| `a + C + e\b` | ей | make, name, take |
| `o + C + e\b` | оу | home, hope, nose |
| `u + C + e\b` | ю | use, cute |
| `i + C + e + letter` | ай | pipeline, lifeline |
| `a + C + e + letter` | ей | homemade, takeover |
| `o + C + e + letter` | оу | (compound boundary) |
| `an + consonant` | ен | plan, stand, cannot |

### y-at-end rules (regex pass)
| Pattern | Cyrillic | Example |
|---------|----------|---------|
| `\by(?=[aeiou])` | й | yes → йес |
| `y\b` | и | only → онли, very → вери |
| `y` (other) | ай | my → май, try → трай |

### th rules (regex pass, in order)
| Pattern | Cyrillic | Example |
|---------|----------|---------|
| `\bthe` | де | the, them, then |
| `\btha` | да | that, than |
| `\bthi` | ди | this, thing |
| `\btho` | до | those, though |
| `\bthu` | ду | thus |
| `\bthr` | тр | three, through |
| `th` (fallback) | д | other words |

### Fixed digraphs (literal pass)
| Pattern | | |
|---------|---|
| `sh→ш, ch→ч, ck→к, tch→ч, ph→ф` | | |
| `ng→нг, nk→нк, qu→ку` | | |
| `tion→шн, sion→жн, ture→чур` | | |
| `eigh→ей, igh→ай, ee→и, oo→у` | | |
| `ou→ау, ow→оу, oi→ой, oy→ой` | | |
| `ay→ей, ai→ей, ea→и, oa→оу` | | |
| `wor→уър, war→уор` | | |
| `air→эр, ear→ир` | | |
| `er→ер, ir→ер, ur→ер, or→ор, ar→ар` | | |

### Post-processing
- Silent final `е` dropped after consonants
- Word-final `ер` → `ър` (multi-syllable only)
- Consecutive Cyrillic consonants deduplicated (except с, з, ш)
- First word after `.!?` lowercased

### Dictionary entries (irregular words)
Standard function words: `the→да, a→а, of→оф, to→то, is→из`
Pronouns: `I→ай, you→ю, your→юър, we→уи, me→ми, my→май`
Numbers: `one→уан, two→ту`
Verbs: `was→уас, are→аре, does→даз, done→дан, come→кам, said→сед, give→гив`
Runglish-style: `believe→белийв, because→бикъз, ridiculous→рейдикюлъс`
Compounds: `pipeline→пайплейн, homemade→хоумемейд, through→тхру, reply→риплей`

## Plugin architecture

- `speak-runglish.mjs` exports a `Plugin` returning `Hooks` with `experimental.text.complete`
- Hook fires after each LLM text part generation
- Uses `exec()` for fire-and-forget: `python cyrify.py` → write `.ps1` script → `powershell -File`
- PowerShell script uses SAPI `SpVoice` COM object, loops until `RunningState ≠ 1`
- Temp files cleaned up in callback
- Skips code blocks (starting with ``` or `)

## Common commands

```powershell
# Cyrillify text
python cyrify.py "your english text"

# Speak through SAPI
powershell -NoProfile -File path\to\speak.ps1
```

## Style conventions

- Code blocks, file paths, commands stay in Latin script
- Only prose gets cyrillified
- Bulgarian Cyrillic preferred (ё is used only where user requests it)
