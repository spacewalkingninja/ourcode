import { writeFileSync } from "fs"

const CHAR_MAP = {
  "0": " zero ", "1": " one ", "2": " two ", "4": " four ",
  "5": " five ", "6": " six ", "7": " seven ", "8": " eight ", "9": " nine ",
  "_": " underscore ",
  "$": " dollar ", "&": " and ",
  "(": " open paren ", ")": " close paren ",
  "{": " open curly ", "}": " close curly ",
  "[": " open bracket ", "]": " close bracket ",
}

function _replaceChars(segment) {
  let s = segment.replace(/\*/g, "")
  s = s.replace(/(\d)\.(\d)/g, "$1 dot $2")
  s = s.replace(/[!?,.:#]/g, "")
  s = s.replace(/[–—-]/g, " dash ")
  s = s.replace(/-/g, " dash ")
  for (const [ch, word] of Object.entries(CHAR_MAP)) {
    s = s.split(ch).join(word)
  }
  s = s.replace(/\s+/g, " ").trim()
  return s
}

function _prepareForSpeech(text) {
  const parts = text.split(/(`[^`]*`)/)
  for (let i = 0; i < parts.length; i++) {
    if (i % 2 === 0) parts[i] = _replaceChars(parts[i])
  }
  return parts.join("")
}

const tests = [
  "hello * world * test *",
  "value is 3.14 and $100 (yes)",
  "look: star*test! here? ok.",
  "fire-and-forget—cool",
  "code `test * star` outside",
]

for (const t of tests) {
  const r = _prepareForSpeech(t)
  writeFileSync("test_out.txt", r, "utf8")
  console.log(`IN:  [${t}]`)
  console.log(`OUT: [${r}]`)
  console.log()
}
