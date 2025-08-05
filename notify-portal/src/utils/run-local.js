import minimist from 'minimist'
import { main } from '../main.js'
import handlers from '../handlers.js'

const required = ['path', 'messagetype']

const argv = minimist(process.argv.slice(2))

if (argv.help) {
  console.log('Test notify action locally:')
  console.log(' --topic\tARN of the topic to send to. Defaults for localstack.')
  console.log(' --path\t\tPath to the config to generate the message from.')
  console.log(' --messagetype\tWhat type of message to generate.')
  console.log(' --environment\tUsed by some messagetypes.')
  process.exit(0)
}

let failed = false
for (const r of required) {
  if (!argv[r]) {
    console.log(`Required param: --${r}`)
    failed = true
  }
}

if (failed) process.exit(1)

for (const [k, v] of Object.entries(argv)) {
  const envname = `INPUT_${k}`.toUpperCase()
  process.env[envname] = v
  console.log(envname, v)
}

await main(handlers)
