# workflow-timeout

A reusable GitHub Actions workflow that acts as a timeout guard for your workflows. It kills a job if the runner becomes stuck or unavailable, preventing workflows from hanging indefinitely.

## What does it do?

Runs a lightweight job on the same runner as your workflow with a configurable timeout. If the runner is stuck or unavailable, GitHub will cancel the job once the timeout is reached rather than letting it hang.

## Example usage

```yaml
jobs:
  timeout-guard:
    uses: defra-cdp-sandpit/cdp-build-action/.github/workflows/workflow-timeout.yml@main
    with:
      timeout: 15
      runner: [self-hosted, infra-dev]
```

> The `runner` input must match the runner used in your actual workflow jobs so the guard targets the same runner pool.

## Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `timeout` | Job timeout in minutes — kills the job if the runner is stuck or unavailable | No | `10` |
| `runner` | Runner to use — must match your actual workflow runner | No | `ubuntu-latest` |
