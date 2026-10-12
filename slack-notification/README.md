# Slack Notification Action

Send a slack notification via the mono lambda

## Inputs

| Input      | Description                                                                                                          | Required | Default                   |
|------------|----------------------------------------------------------------------------------------------------------------------|----------|---------------------------|
| `channel`  | Name of the slack channel (e.g. cdp-infra-notifications)                                                             | No       | `cdp-infra-notifications` |
| `colour`   | Hex color code for the Slack message sidebar (e.g. #2EB67D for success, #ECB22E for warning, or #E01E5A for failure) | No       | `#2EB67D` (green)         |
| `icon_url` | URL of the icon displayed alongside the title in the Slack message context                                           | No       | ``                        |
| `title`    | Title displayed alongside the image in the Slack message context. Supports Slack mrkdwn formatting                   | No       | ``                        |
| `header`   | Header text displayed prominently in the Slack message                                                               | No       | ``                        |
| `message`  | Main notification message body. Supports Slack mrkdwn formatting                                                     | Yes      |                           |
| `footer`   | Footer text displayed in the Slack message context. Supports Slack mrkdwn formatting                                 | No       | ``                        |

## Usage

### Basic Usage

```yaml
- name: Slack Notification for Version 8.x
  uses: DEFRA/cdp-build-action/slack-notification@CORE-4131
  with:
    channel: "cdp-alert-testing"
    colour: '#ECB22E'
    icon_url: 'https://avatars.githubusercontent.com/u/1683025?s=48&v=4'
    title: 'Percona MongoDB New Release Built'
    header: 'Percona MongoDB ${{ inputs.percona_version }} built in ECR :mongodb-logo:'
    message: 'Runbook: https://github.com/DEFRA/cdp-platform-documentation/blob/main/runbooks/mongo-upgrades.md'
    footer: 'Triggered by: DEFRA/cdp-percona-mongo Build Percona 8x workflow'

```

## Related Documentation

- [actions/checkout Documentation](https://github.com/actions/checkout)
- [GitHub Actions Composite Actions Guide](https://docs.github.com/en/actions/creating-actions/creating-a-composite-action)
