# Notify Portal

This action centralises the various scripts used to generate and notify the CDP Portal about changes in infrastructure.

## Inputs

| Input       | Description                                                              | Required |
| ----------- | ------------------------------------------------------------------------ | -------- |
| messageType | The type of message you want to generate (see below).                    | yes      |
| path        | The path to the files the action will use to generate the message from   | yes      |
| topic       | The SNS topic to send the messages to                                    | yes      |
| environment | Which CDP environment to generate messages for (depends on message type) | no       |
|             |                                                                          |          |

## Supported message types

- `tenant-services`

## Requirements

### Node Version

GitHub actions support a limited number of Node versions (currently Node 20).
Do not update the Node version without checking that it is supported in GitHub actions.

The version of Node used must match the version in `actions.yml`.

## Building and Releasing

1. Run `npm run package`
2. Commit any changes to `dist/index.js` to the repo
3. Raise a pull request and merge the changes into main

If you have updated the code but not rebuilt the package the PR validator will warn you.

## Running locally

You can trigger the action locally to test it or use it with portal running locally.
The GitHub action pulls its inputs from environment variables prefixed with `INPUT`

```bash
export INPUT_MESSAGE
export INPUT_ENVIRONMENT=dev
export INPUT_PATH=/path/to/local/cdp-tf-svc-infra
export INPUT_TOPIC=arn:aws:sqs:eu-west-2:000000000000:cdp_workflow_events
```

`node src/index.js`
