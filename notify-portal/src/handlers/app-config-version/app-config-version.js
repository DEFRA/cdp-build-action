import * as core from '@actions/core'
import { isDir } from '../../utils/index.js'
import { sendSnsMessage } from '../../utils/send-sns.js'
import { envelope } from '../../utils/envelope.js'
import { validate } from './schema.js'
import { getLatestGitInfo } from '../../utils/git.js'

export const messageType = 'app-config-version'

export async function handle() {
  const baseDir = core.getInput('path')
  const environment = core.getInput('environment')
  const topic = core.getInput('topic')

  if (!isDir(baseDir)) {
    throw new Error(`invalid path ${baseDir}`)
  }

  const payload = envelope(messageType, {
    ...getLatestGitInfo(baseDir),
    environment
  })

  if (!validate(payload)) {
    const validationError = validate.errors.map((e) => e.message).join(', ')
    throw new Error(`generated an invalid payload, ${validationError}`)
  }

  core.info(
    `Sending config version ${payload.payload.commitSha} for ${environment} to ${topic}`
  )
  await sendSnsMessage(topic, payload)
}
