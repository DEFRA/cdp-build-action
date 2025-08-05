import {
  ListTopicsCommand,
  PublishCommand,
  SNSClient
} from '@aws-sdk/client-sns'
import * as core from '@actions/core'

const client = new SNSClient({
  region: 'eu-west-2'
})

export async function sendSnsMessage(
  topic,
  message,
  groupId = 'none',
  deduplicationId = crypto.randomUUID()
) {
  await listTopics()
  core.info('preparing sns payload')

  const input = {
    TopicArn: topic,
    Message: JSON.stringify(message, null, 2)
  }

  // At the time of writing localstack doesn't support fifo queues and will fail if you set these values on a non-fifo
  // queue. Luckily, AWS requires all fifo queues to end with `.fifo` so we can selectively add these params.
  if (topic.endsWith('fifo')) {
    input.MessageDeduplicationId = deduplicationId
    input.MessageGroupId = groupId
  }

  const command = new PublishCommand(input)
  const snsResponse = await client.send(command)
  core.info(`SNS message MessageId: ${snsResponse?.MessageId}`)
  return snsResponse
}

async function listTopics() {
  const command = new ListTopicsCommand()
  console.log(await client.send(command))
}
