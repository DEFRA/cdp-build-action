# CDP get-github-token-v2 Action

The `get-github-token-v2` action requests a scoped, short-lived GitHub App installation token from the mono-lambda `get-github-token` module. The token is restricted to the repositories you specify and expires in approximately one hour.

Unlike the original `get-github-token` action, the GitHub App private key **never leaves AWS**. Token creation happens inside the mono-lambda, and the caller authenticates via SigV4 (IAM role).

## Prerequisites

**This action requires a self-hosted runner.** The token service is a private API Gateway endpoint, not reachable from GitHub-hosted runners (`ubuntu-latest`).

All CDP environments have an `execute-api` VPC interface endpoint which routes to the management mono-lambda API GW via AWS PrivateLink. This means **any `cdp-default` stable runner can call the token service**, regardless of which environment it is in. You do not need to pin to a specific environment *just to reach the token service*:

```yaml
runs-on:
  group: cdp-default
  labels:
    - stable    # any environment's runners can reach the management token service
```

If your job also needs to reach a resource that is private to a specific environment (e.g. an internal OpenSearch endpoint in dev), you need to add that environment's label.

The IAM role specified in `role_to_assume` must be listed in `api_gateway_allowed_principal_arns` in `cdp-tf-core/cdp-mono-lambda.tf`. If it is not, the API Gateway will return 403.

## Inputs

| Input               | Description                                                                                                   | Required |
|---------------------|---------------------------------------------------------------------------------------------------------------|----------|
| `token_service_url` | Full HTTPS URL of the `/github/token` endpoint. Use the management execute-api URL: `https://dn6yr97qx9.execute-api.eu-west-2.amazonaws.com/management/github/token`. This URL works from any CDP environment's runner via PrivateLink | yes |
| `role_to_assume`    | IAM role ARN to assume before calling the endpoint. Must be listed in the API Gateway resource policy       | yes      |
| `repositories`      | Comma-separated list of repo names to scope the token. Defaults to the calling repository.                  | no       |
| `aws_region`        | AWS region for SigV4 signing. (default: `eu-west-2`)                                                        | no       |
| `username`          | Git `user.name` to configure. Recommended when the token is used for git commits.                           | no       |
| `email`             | Git `user.email` to configure. Recommended when the token is used for git commits.                          | no       |

`username` is typically the name of the GitHub App with `[bot]` on the end, e.g. `cdp-github-action[bot]`.

`email` is typically `<install-id>+<username>@users.noreply.github.com`. The install ID can be found at `https://api.github.com/users/<username>`, e.g. `147416134+cdp-github-action[bot]@users.noreply.github.com`.

## How to use it

### Standard CI/CD workflow (single repo)

Most workflows only need a token for their own repository to commit/push and bypass branch protection.
Omit `repositories` and it defaults to the calling repo:

```yaml
      - name: Check out code
        uses: actions/checkout@v4

      - name: Get token
        id: get-token
        uses: DEFRA/cdp-build-action/get-github-token-v2@stable
        with:
          role_to_assume: arn:aws:iam::094954420758:role/github-actions-role
          token_service_url: https://dn6yr97qx9.execute-api.eu-west-2.amazonaws.com/management/github/token
          email: ${{ env.cdp-gitbot-email }}
          username: ${{ env.cdp-gitbot-name }}
```

### Orchestrator / multi-repo workflow

Workflows that need to interact with several repositories (like cdp-tenant-config triggering other repos workflows) can pass a comma-separated list:

```yaml
      - name: Get token (multi-repo)
        uses: DEFRA/cdp-build-action/get-github-token-v2@stable
        with:
          role_to_assume: arn:aws:iam::094954420758:role/github-actions-role
          token_service_url: https://dn6yr97qx9.execute-api.eu-west-2.amazonaws.com/management/github/token
          repositories: "cdp-tf-svc-infra,cdp-tf-waf,cdp-grafana-svc"
          email: ${{ env.cdp-gitbot-email }}
          username: ${{ env.cdp-gitbot-name }}
```

The workflow job must also have `id-token: write` permission for the OIDC role assumption to work:

```yaml
permissions:
  id-token: write
  contents: read
```

After the action runs it will have:

1. Assumed the specified IAM role via GitHub OIDC.
2. Called the mono-lambda `get-github-token` module (SigV4-signed POST to `/github/token`).
3. Set `GH_TOKEN` environment variable to the scoped token.
4. Configured the git credential helper to use the token for all `https://github.com` operations.
5. Set `git config user.name` and `git config user.email`, if provided.

## Branch protection

The same GitHub App bypass rules apply as with the original action. To push commits that bypass branch protection you must be using GitHub [rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets) (not classic branch protection), with the GitHub App added to the bypass list.

## Token scope

The token is restricted to the repositories listed in the `repositories` input. Access control is enforced at the API Gateway layer, only IAM principals listed in `api_gateway_allowed_principal_arns` can reach the endpoint.

Tokens are created with the following fixed permissions:

| Permission      | Level   |
|-----------------|---------|
| `actions`       | `write` |
| `contents`      | `write` |
| `metadata`      | `read`  |
| `pull_requests` | `write` |
| `workflows`     | `write` |
