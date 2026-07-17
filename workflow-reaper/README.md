# workflow-reaper

A composite GitHub Actions action that cancels workflow runs that have been queued or running longer than a configured threshold. Useful as a scheduled job to clean up stuck or abandoned runs across a repository.

## What does it do?

Queries all `queued` and `in_progress` workflow runs in the repository and cancels any that were created before the configured cutoff time.

## Example usage

Run on a schedule to automatically reap stuck workflows:

```yaml
on:
  schedule:
    - cron: '0 * * * *'  # every hour

jobs:
  reaper:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    permissions:
      actions: write
      id-token: write
    env:
      GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    steps:
      - name: Cancel long-running workflows
        uses: DEFRA/cdp-build-action/workflow-reaper@stable
        with:
          timeout_minutes: 120
```

## Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `timeout_minutes` | Cancel workflows that have been queued or running longer than this many minutes | No | `120` |

## Permissions

The calling job must grant `actions: write` permission so the action can cancel runs:

```yaml
permissions:
  actions: write
```
