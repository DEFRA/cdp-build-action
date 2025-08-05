import { dirname, resolve } from 'node:path'
import { vi, test, describe, beforeEach, expect, afterEach } from 'vitest'
import { handle } from './tenant-services.js'
import { sendSnsMessage } from '../../utils/send-sns'

import { fileURLToPath } from 'node:url'

const __dirname = dirname(fileURLToPath(import.meta.url))

vi.mock('../../utils/send-sns.js')

describe('handleTenants', () => {
  beforeEach(() => {
    vi.stubEnv(
      'INPUT_PATH',
      resolve(__dirname, './__fixtures__/cdp-tf-svc-infra')
    )
  })

  afterEach(() => {
    vi.resetAllMocks()
    vi.unstubAllEnvs()
  })

  test('expect error to be thrown when environment is set but does not exist', async ({
    expect
  }) => {
    vi.stubEnv('INPUT_ENVIRONMENT', 'foo')
    const promise = () => handle()
    await expect(promise).rejects.toThrowError(
      'No environment folder found for foo'
    )
  })

  test('expect error to be thrown when environment not set', async ({
    expect
  }) => {
    const promise = () => handle()
    await expect(promise).rejects.toThrowError('environment is not set')
  })

  test('expect two services to be sent for dev environment', async () => {
    vi.stubEnv('INPUT_ENVIRONMENT', 'dev')
    vi.stubEnv('INPUT_TOPIC', 'portal-topic')
    await handle()

    expect(sendSnsMessage).toBeCalledWith(
      'portal-topic',
      expect.objectContaining({
        eventType: 'tenant-services',
        timestamp: expect.any(String),
        payload: {
          environment: 'dev',
          services: expect.arrayContaining([
            {
              mongo: true,
              redis: false,
              name: 'backend',
              queues: ['foo_results_callback.fifo'],
              service_code: 'FOO',
              zone: 'protected'
            },
            {
              zone: 'public',
              mongo: false,
              redis: true,
              service_code: 'FOO',
              name: 'frontend'
            }
          ])
        }
      })
    )
  })
})
