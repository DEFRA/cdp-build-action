import fs from 'node:fs/promises'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

/**
 * Auto-discovers all the handlers in the handlers folder.
 * Handler folders must have an index.js file that exports messageType and handle.
 *
 * @returns {Promise<{}>}
 */
async function autoLoadHandlers() {
  const __dirname = path.dirname(fileURLToPath(import.meta.url))
  const handlersDir = path.resolve(__dirname, 'handlers')

  const handlers = {}

  const handlerFolders = await fs.readdir(handlersDir)

  for (const folderName of handlerFolders) {
    const folderPath = path.join(handlersDir, folderName)
    const indexFilePath = path.join(folderPath, 'index.js')

    try {
      const stat = await fs.stat(indexFilePath)
      if (stat.isFile()) {
        const handlerModule = await import(indexFilePath)
        if (
          handlerModule.default &&
          handlerModule.default.messageType &&
          handlerModule.default.handle
        ) {
          handlers[handlerModule.default.messageType] =
            handlerModule.default.handle
          console.log(
            `registered handler for ${handlerModule.default.messageType}`
          )
        } else {
          console.warn(
            `Could not load handler from ${folderName}: missing export messageType or handle`
          )
        }
      }
    } catch (error) {
      console.warn(`Could not load handler from ${folderName}:`, error.message)
    }
  }

  return handlers
}
// TODO: over-complex? this might be better as a simple object?
const handlers = await autoLoadHandlers()

export default handlers
