import { exec } from "child_process"
import { writeFileSync, unlinkSync } from "fs"
import { tmpdir } from "os"
import { fileURLToPath } from "url"
import { dirname, join } from "path"

const __dirname = dirname(fileURLToPath(import.meta.url))
const cyrifyPath = join(__dirname, "cyrify.py")

const SpeakRunglishPlugin = async () => {
  return {
    "experimental.text.complete": async (_input, output) => {
      const text = output.text.trim()
      if (!text || text.length < 10) return
      if (text.startsWith("```") || text.startsWith("`")) return

      const stamp = Date.now()
      const txtFile = `${tmpdir()}\\runglish_${stamp}.txt`
      const ps1File = `${tmpdir()}\\runglish_${stamp}.ps1`
      const escaped = text.replace(/"/g, '\\"')

      exec(`python "${cyrifyPath}" "${escaped}"`, {
        timeout: 5000, windowsHide: true, encoding: "utf8",
      }, (err, stdout) => {
        if (err || !stdout) return
        const cyr = stdout.trim()
        if (!cyr) return

        writeFileSync(txtFile, cyr, "utf8")

        const psBody = `$v = New-Object -ComObject SAPI.SpVoice
$voices = $v.GetVoices()
for ($i=0;$i -lt $voices.Count;$i++) {
  if ($voices.Item($i).GetDescription() -eq "Microsoft Pavel - Russian (Russia)") {
    $v.Voice = $voices.Item($i); break
  }
}
$t = (Get-Content "${txtFile}" -Encoding UTF8 -Raw).Trim()
$v.Rate = -1
$v.Speak($t) | Out-Null
while ($v.Status.RunningState -eq 1) { Start-Sleep -Milliseconds 200 }
`
        writeFileSync(ps1File, psBody, "utf8")

        exec(`powershell -NoProfile -ExecutionPolicy Bypass -File "${ps1File}"`, {
          timeout: 60000, windowsHide: true,
        }, () => {
          try { unlinkSync(txtFile) } catch {}
          try { unlinkSync(ps1File) } catch {}
        })
      })
    },
  }
}

export default SpeakRunglishPlugin
