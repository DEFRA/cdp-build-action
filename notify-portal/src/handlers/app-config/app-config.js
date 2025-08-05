import path from 'node:path'

import * as core from '@actions/core'
import * as glob from '@actions/glob'

import { isDir } from '../../utils/index.js'
import { getLatestGitInfo } from '../../utils/git.js'
import { sendSnsMessage } from '../../utils/send-sns.js'
import { envelope } from '../../utils/envelope.js'

import { validate } from './schema.js'

export const messageType = 'app-config'

export async function handle() {
  const baseDir = core.getInput('path')
  const environment = core.getInput('environment')
  const topic = core.getInput('topic')

  if (!isDir(baseDir)) {
    throw new Error(`invalid path ${baseDir}`)
  }

  const pattern = `${baseDir.replace(/\/$/, '')}/services/*/${environment}/*.env`
  const globber = await glob.create(pattern)
  const files = await globber.glob()
  const entities = files.map((f) => path.basename(f).replace('.env', ''))

  const payload = envelope(messageType, {
    ...getLatestGitInfo(baseDir),
    environment,
    entities
  })

  console.log(payload)
  if (!validate(payload)) {
    const validationError = validate.errors.map((e) => e.message).join(', ')
    throw new Error(`generated an invalid payload, ${validationError}`)
  }

  core.info(
    `Sending config version ${payload.payload.commitSha} for ${environment} to ${topic}`
  )
  await sendSnsMessage(topic, payload)
}
