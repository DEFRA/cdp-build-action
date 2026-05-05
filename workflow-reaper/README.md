# workflow-reaper

A reusable GitHub Actions workflow that cancels workflow runs that have been queued or running longer than a configured threshold. Useful as a scheduled job to clean up stuck or abandoned runs across a repository.

## What does it do?

Queries all `queued` and `in_progress` workflow runs in the repository and cancels any that were created before the configured cutoff time. Requires `actions: write` permission to cancel runs.

## Example usage

Run on a schedule to automatically reap stuck workflows:

```yaml
on:
  schedule:
    - cron: '0 * * * *'  # every hour

jobs:
  reaper:
    uses: defra-cdp-sandpit/cdp-build-action/.github/workflows/workflow-reaper.yml@main
    with:
      timeout_minutes: 120
```

## Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `timeout_minutes` | Cancel workflows that have been queued or running longer than this many minutes | No | `120` |

## Permissions

The calling workflow must grant the following permissions:

```yaml
permissions:
  actions: write
  contents: write
```
