import fs from 'node:fs'
import path from 'node:path'

import * as glob from '@actions/glob'
import * as core from '@actions/core'

import { sendSnsMessage } from '../../utils/send-sns.js'
import { validate } from './schema.js'
import { envelope } from '../../utils/envelope.js'
import { isDir } from '../../utils/index.js'

const messageType = 'tenant-services'

export async function handle() {
  const baseDir = core.getInput('path')
  const environment = core.getInput('environment')
  const topic = core.getInput('topic')

  if (!environment) {
    throw new Error('environment is not set')
  }

  const envDir = path.join(baseDir, `environments/${environment}/tenants/`)
  if (!isDir(envDir)) {
    throw new Error(`No environment folder found for ${environment}`)
  }

  core.info(`searching for tenant files in ${envDir}`)

  const pattern = `${envDir.replace(/\/$/, '')}/**/*.json`
  const globber = await glob.create(pattern)
  const files = await globber.glob()

  const services = []

  for (const filePath of files) {
    try {
      const content = fs.readFileSync(filePath, 'utf-8')
      const service = JSON.parse(content)
      service.name = path.basename(filePath, '.json')
      services.push(service)
    } catch (err) {
      core.debug(`Skipping invalid JSON file: ${filePath}: ${err.message}`)
    }
  }

  const payload = envelope(messageType, { environment, services })

  if (validate(payload)) {
    core.info(
      `Sending ${services.length} tenant services in ${environment} to ${topic}`
    )
    await sendSnsMessage(topic, payload)
  } else {
    const validationError = validate.errors.map((e) => e.message).join(', ')
    core.error(validationError)
    throw new Error(
      `generated an invalid payload, ${validationError}`
    )
  }
}

export const tenantServiceHandler = {
  [messageType]: handle
}
