import path from 'node:path'
import { execSync } from 'node:child_process'

/**
 * Finds the latest commit and commit timestamp from a git repo
 * @param {string} baseDir
 * @returns {{commitSha: string, commitTimestamp: string}}
 */
function getLatestGitInfo(baseDir) {
  const options = {
    cwd: path.resolve(baseDir),
    encoding: 'utf-8'
  }

  const commitSha = execSync('git log -1 --format=%H', options).trim()
  const commitTimestamp = execSync('git log -1 --format=%cI', options).trim()

  return { commitSha, commitTimestamp }
}

export { getLatestGitInfo }
