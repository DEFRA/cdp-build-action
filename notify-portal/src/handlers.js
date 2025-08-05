import * as tenantServices from "./handlers/tenant-services/index.js";
import * as appConfig from "./handlers/app-config/index.js";
import * as appConfigVersion from "./handlers/app-config-version/index.js";

const handlers = {
  ...tenantServices,
  ...appConfig,
  ...appConfigVersion,
}

export default handlers
