import { Ajv } from 'ajv'

export const schema = {
  type: 'object',
  properties: {
    eventType: { const: 'tenant-services' },
    timestamp: { type: 'string' },
    payload: {
      type: 'object',
      properties: {
        environment: { type: 'string' },
        services: {
          type: 'array',
          items: {
            type: 'object',
            properties: {
              name: { type: 'string' },
              zone: { type: 'string' },
              mongo: { type: 'boolean' },
              redis: { type: 'boolean' },
              service_code: { type: 'string' },
              test_suite: { type: 'string' },
              buckets: {
                type: 'array',
                items: { type: 'string' }
              },
              queues: {
                type: 'array',
                items: { type: 'string' }
              },
              api_enabled: { type: 'boolean' },
              api_type: { type: 'string' }
            },
            required: ['name', 'mongo', 'redis', 'service_code']
          }
        }
      },
      required: ['environment', 'services']
    }
  },
  required: ['eventType', 'timestamp', 'payload']
}

export const validate = new Ajv().compile(schema)
