# Get Plan Artifact

Downloads a Terraform plan artifact from a PR workflow for use in subsequent workflows.

## Description

This composite action downloads a previously generated Terraform plan file artifact from a pull request workflow. It's designed to work as part of a Terraform deployment pipeline where plans are generated during PR validation and then applied after approval.

## Inputs

### `pr_number`

**Required**: Yes

The pull request number to fetch the artifact from. This should be the PR number where the plan was originally generated.

### `environment`

**Required**: Yes

The environment name (e.g., `dev`, `prod`, `test`). This is used to construct the artifact name as `{environment}.plan.file`.

## Usage

### Basic Example

```yaml
- name: Download Terraform Plan
  uses: ./tf-build/download-plan
  with:
    pr_number: ${{ github.event.pull_request.number }}
    environment: dev
```

### Conditional Download

The action automatically skips the download step if `pr_number` is empty:

```yaml
- name: Download Terraform Plan
  uses: ./tf-build/download-plan
  with:
    pr_number: ${{ github.event.pull_request.number || '' }}
    environment: prod
```

### In a Deployment Workflow

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Get Terraform Plan
        uses: ./tf-build/download-plan
        with:
          pr_number: ${{ github.event.number }}
          environment: production

      - name: Apply Terraform Plan
        run: terraform apply production.plan.file
```

## How It Works

1. The action looks for artifacts from the `pull-request.yml` workflow
2. It searches for an artifact named `{environment}.plan.file`
3. Downloads the artifact to the current directory (`.`)
4. If no artifact is found, the action continues without failing (`if_no_artifact_found: ignore`)

## Dependencies

This action uses:
- [DEFRA/cdp-action-download-artifact@v20](https://github.com/DEFRA/cdp-action-download-artifact)

## Notes

- The action will gracefully skip if no PR number is provided
- Artifacts are downloaded to the current working directory
- If the artifact doesn't exist, the workflow will continue (no failure)
- The artifact name must match the pattern: `{environment}.plan.file`
