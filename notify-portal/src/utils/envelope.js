/**
 * Generates a 'envelope' structure describing the type of payload to be
 * consumed by portal
 * @param {string} eventType
 * @param {any} payload
 * @returns {{payload: any, eventType: string, timestamp: string}}
 */
export function envelope(eventType, payload) {
  return {
    eventType,
    timestamp: new Date().toISOString(),
    payload
  }
}
