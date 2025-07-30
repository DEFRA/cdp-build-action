import { main } from './main.js'
import { tenantServiceHandler } from './handlers/tenant-services/tenant-services.js'

const handlers = {
  ...tenantServiceHandler
}

await main(handlers)
