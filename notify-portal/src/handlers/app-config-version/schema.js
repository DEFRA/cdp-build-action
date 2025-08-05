import { Ajv } from 'ajv'

export const schema = {
  type: 'object',
  properties: {
    eventType: { const: 'app-config-version' },
    timestamp: { type: 'string' },
    payload: {
      type: 'object',
      properties: {
        environment: { type: 'string' },
        commitSha: { type: 'string' },
        commitTimestamp: { type: 'string' }
      },
      required: ['environment', 'commitSha', 'commitTimestamp']
    }
  },
  required: ['eventType', 'timestamp', 'payload']
}

export const validate = new Ajv().compile(schema)
