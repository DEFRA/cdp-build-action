import { vi, test, describe, beforeEach, expect, afterEach } from 'vitest'
import { ExitCode } from '@actions/core'
import { main } from './main.js'

describe('#main', () => {
  beforeEach(() => {
    vi.stubEnv('INPUT_PATH', '/test')
  })

  afterEach(() => {
    vi.resetAllMocks()
  })

  test('main throws an error when the event type is not supported', async ({
    expect
  }) => {
    vi.stubEnv('INPUT_EVENTTYPE', 'foo')

    await main({})

    expect(process.exitCode).toBe(ExitCode.Failure)
  })

  test('main calls the correct handler based on input', async () => {
    vi.stubEnv('INPUT_ENVIRONMENT', 'test')
    vi.stubEnv('INPUT_EVENTTYPE', 'tenant-service')

    const handlers = { 'tenant-service': vi.fn() }
    await main(handlers)

    expect(handlers['tenant-service']).toHaveBeenCalled()
  })
})
