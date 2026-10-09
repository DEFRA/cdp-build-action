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
- name: Checkout code
  uses: ./cdp-build-action/checkout
```

## Maintenance

To update the underlying `actions/checkout` version:

1. Edit `action.yml`
2. Update the version in the `uses:` statement (currently `v5`)
3. Commit and push changes
4. All pipelines using this wrapper will automatically use the new version

## Related Documentation

- [actions/checkout Documentation](https://github.com/actions/checkout)
- [GitHub Actions Composite Actions Guide](https://docs.github.com/en/actions/creating-actions/creating-a-composite-action)
