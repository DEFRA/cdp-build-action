import * as tenantServices from './handlers/tenant-services/tenant-services.js'
import * as appConfig from "./handlers/app-config/app-config.js"
import * as appConfigVersion from "./handlers/app-config-version/app-config-version.js";

const handlers = {
  'tenant-services': tenantServices.handle,
  'app-config': appConfig.handle,
  'app-config-version': appConfigVersion.handle
}

export default handlers
