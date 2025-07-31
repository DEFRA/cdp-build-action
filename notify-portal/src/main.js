import * as core from '@actions/core'

export async function main(handlers) {
  try {
    const messageType = core.getInput('messageType')

    if (!handlers[messageType]) {
      core.setFailed(
        `Unknown message type ${messageType}. Supported types are: ${Object.keys(handlers).join(', ')}`
      )
    }
    core.info(`Handling ${messageType}`)
    await handlers[messageType]()
  } catch (error) {
    core.setFailed(error.message)
  }
}
