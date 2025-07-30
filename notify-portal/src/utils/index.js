import fs from 'node:fs'

export function isDir(path) {
  try {
    const stat = fs.statSync(path)
    return stat.isDirectory()
  } catch (err) {
    return false
  }
}
