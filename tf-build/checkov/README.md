# Centralized Checkov Scan Action

This composite action provides a standardized wrapper for a pinned [Checkov](https://www.checkov.io/) CLI invocation. It centralizes the versioning and default configuration for Infrastructure as Code (IaC) security scanning across all workflows in this repository.

## Why Use This Action?

* **Single Source of Truth:** Manage the Checkov version (`3.3.9`) in one file rather than updating dozens of workflow files.
* **Consistent Policy:** Ensures that the Prisma API URL, output formats, and framework settings are identical across the organization.
* **Runner Compatibility:** Avoids the Docker-action path and problem matcher issues seen on persistent self-hosted runners.
* **Clean Workflows:** Reduces boilerplate code in your main CI/CD pipeline files.

## Inputs

| Input | Description | Required | Default |
| :--- | :--- | :--- | :--- |
| `quiet` | If set to `true`, only display failed checks. | No | `true` |
| `framework` | The IaC framework to scan (e.g., `terraform`, `cloudformation`, `all`). | No | `terraform` |
| `output_format` | The report format (`cli`, `json`, `sarif`). | No | `cli` |
| `prisma-api-url` | The URL for the Prisma Cloud API endpoint. | No | `https://api0.prismacloud.io` |

## Usage

To use this action, simply reference its local path in your workflow. Ensure you have performed a checkout step before running the scan.

```yaml
jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: ./.github/actions/ui-checkout

      - name: Run Checkov Scan
        uses: ./.github/actions/tf-checkov
        with:
          framework: 'terraform'
          quiet: true
