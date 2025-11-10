import { Ajv } from 'ajv'

export const schema = {
  type: 'object',
  properties: {
    eventType: { const: 'app-config' },
    timestamp: { type: 'string' },
    payload: {
      type: 'object',
      properties: {
        environment: { type: 'string' },
        commitSha: { type: 'string' },
        commitTimestamp: { type: 'string' },
        entities: {
          type: 'array',
          items: { type: 'string' }
        }
      },
      required: ['environment', 'commitSha', 'commitTimestamp', 'entities']
    }
  },
  required: ['eventType', 'timestamp', 'payload']
}

export const validate = new Ajv().compile(schema)
