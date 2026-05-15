import { exec } from "child_process"
import { writeFileSync, unlinkSync } from "fs"
import { tmpdir } from "os"
import { fileURLToPath } from "url"
import { dirname, join } from "path"

const __dirname = dirname(fileURLToPath(import.meta.url))
const cyrifyPath = join(__dirname, "cyrify.py")

// Characters to replace with English words (will be cyrillified by cyrify.py)
// Exceptions kept as-is: + - / ± % # 3 , . ! ?
// , . ! ? - – — kept in text → SAPI natural pauses
const CHAR_MAP = {
  "0": " zero ", "1": " one ", "2": " two ", "4": " four ",
  "5": " five ", "6": " six ", "7": " seven ", "8": " eight ", "9": " nine ",
  "_": " underscore ",
  "$": " dollar ", "&": " and ", "\\": " back slash ",
  "(": " open paren ", ")": " close paren ",
  "{": " open curly ", "}": " close curly ",
  "[": " open bracket ", "]": " close bracket ",
}

function _replaceChars(segment) {
  // * → silent removal
  let s = segment.replace(/\*/g, "")
  // . between digits → " dot "
  s = s.replace(/(\d)\.(\d)/g, "$1 dot $2")
  // : # → silent
  s = s.replace(/[:#]/g, "")

  // Dashes → kept in text (SAPI provides natural pauses)

  // Named chars
  for (const [ch, word] of Object.entries(CHAR_MAP)) {
    s = s.split(ch).join(word)
  }

  // Collapse multiple spaces
  s = s.replace(/\s+/g, " ").trim()
  return s
}

function _prepareForSpeech(text) {
  // Preserve inline code spans: split on backtick-delimited segments
  // Even indices = outside code (apply replacements), odd = inside (passthrough)
  const parts = text.split(/(`[^`]*`)/)
  for (let i = 0; i < parts.length; i++) {
    if (i % 2 === 0) {
      parts[i] = _replaceChars(parts[i])
    }
  }
  return parts.join("")
}

const SpeakRunglishPlugin = async () => {
  return {
    "experimental.text.complete": async (_input, output) => {
      const text = output.text.trim()
      if (!text || text.length < 10) return
      if (text.startsWith("```") || text.startsWith("`")) return

      // Pre-process: replace special chars with speakable words
      const prepared = _prepareForSpeech(text)
      if (!prepared) return

      const stamp = Date.now()
      const inFile = `${tmpdir()}\\runglish_in_${stamp}.txt`
      const outFile = `${tmpdir()}\\runglish_out_${stamp}.txt`
      const ps1File = `${tmpdir()}\\runglish_${stamp}.ps1`

      writeFileSync(inFile, prepared, "utf8")

      exec(`python "${cyrifyPath}" --file "${inFile}"`, {
        timeout: 5000, windowsHide: true, encoding: "utf8",
      }, (err, stdout) => {
        try { unlinkSync(inFile) } catch {}
        if (err || !stdout) return
        const cyr = stdout.trim()
        if (!cyr) return

        writeFileSync(outFile, cyr, "utf8")

        const psBody = `$v = New-Object -ComObject SAPI.SpVoice
$voices = $v.GetVoices()
for ($i=0;$i -lt $voices.Count;$i++) {
  if ($voices.Item($i).GetDescription() -eq "Microsoft Pavel - Russian (Russia)") {
    $v.Voice = $voices.Item($i); break
  }
}
$t = (Get-Content "${outFile}" -Encoding UTF8 -Raw).Trim()
$v.Rate = -1
$v.Speak($t)
$v.WaitUntilDone(-1)
`
        writeFileSync(ps1File, psBody, "utf8")

        exec(`powershell -NoProfile -ExecutionPolicy Bypass -File "${ps1File}"`, {
          timeout: 60000, windowsHide: true,
        }, () => {
          try { unlinkSync(outFile) } catch {}
          try { unlinkSync(ps1File) } catch {}
        })
      })
    },
  }
}

export default SpeakRunglishPlugin
