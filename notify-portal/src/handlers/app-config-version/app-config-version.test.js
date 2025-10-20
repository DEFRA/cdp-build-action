import { vi, test, describe, beforeEach, expect, afterEach } from 'vitest'
import { dirname, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'
import { handle } from './app-config-version.js'
import { sendSnsMessage } from '../../utils/send-sns'
import { getLatestGitInfo } from '../../utils/git.js'

vi.mock('../../utils/git.js')
vi.mock('../../utils/send-sns.js')

const __dirname = dirname(fileURLToPath(import.meta.url))
const topic = 'arn:aws:sns:eu-west-2:000000000000:cdp_workflow_events'
const sha = '18e4a2a1be6e509382093931639b145c48ae43ff'
const timestamp = '2025-07-31T16:18:49+01:00'

describe('app-config', () => {
  beforeEach(() => {
    vi.stubEnv(
      'INPUT_PATH',
      resolve(__dirname, './__fixtures__/cdp-app-config')
    )

    vi.stubEnv('INPUT_TOPIC', topic)

    getLatestGitInfo.mockReturnValueOnce({
      commitSha: sha,
      commitTimestamp: timestamp
    })
  })

  afterEach(() => {
    vi.resetAllMocks()
    vi.unstubAllEnvs()
  })

  test('publish a message with the latest git hash', async () => {
    vi.stubEnv('INPUT_ENVIRONMENT', 'dev')

    await handle()

    expect(sendSnsMessage).toHaveBeenCalledWith(
      topic,
      expect.objectContaining({
        eventType: 'app-config-version',
        timestamp: expect.any(String),
        payload: {
          environment: 'dev',
          commitSha: sha,
          commitTimestamp: timestamp
        }
      })
    )
  })
})
