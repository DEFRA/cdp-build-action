import * as core from '@actions/core'

export async function main(handlers) {
  try {
    const eventType = core.getInput('eventType')

    if (!handlers[eventType]) {
      core.setFailed(
        `Unknown message type ${eventType}. Supported types are: ${Object.keys(handlers).join(', ')}`
      )
    }
    core.info(`Handling ${eventType}`)
    await handlers[eventType]()
  } catch (error) {
    core.setFailed(error.message)
  }
}
