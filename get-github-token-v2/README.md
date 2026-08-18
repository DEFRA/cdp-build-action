# CDP get-github-token-v2 Action

The `get-github-token-v2` action requests a scoped, short-lived GitHub App installation token from the CDP token service. The token is restricted to the **calling repository only** and expires in approximately one hour.

Unlike the original `get-github-token` action, the GitHub App private key **never leaves AWS**. Token minting happens inside the CDP mono-lambda, and the caller's identity is determined from their IAM role (via the SigV4 signature on the request).

## Prerequisites

**This action requires a self-hosted runner.** The token service is exposed via a private API Gateway endpoint that is only reachable from within the AWS VPC. GitHub-hosted runners (`ubuntu-latest`) cannot reach it.

The IAM role specified in `role_to_assume` must be listed in `api_gateway_allowed_principal_arns` in `cdp-tf-core/cdp-mono-lambda.tf`. If it is not, the API Gateway will return 403. See [Adding a new caller](https://github.com/DEFRA/cdp-platform-documentation/blob/main/lambdas/cdp-mono-lambda/get-github-token.md#adding-a-new-caller) in the platform docs.

## Inputs

| Input             | Description                                                                                          | Required |
|-------------------|------------------------------------------------------------------------------------------------------|----------|
| `token_service_url` | Full HTTPS URL of the `/github/token` endpoint, e.g. `https://cdp-mono-lambda.api.management.cdp-int.defra.cloud/github/token` | yes |
| `role_to_assume`  | IAM role ARN to assume. Must be listed in the API Gateway resource policy. The OIDC session name of this role encodes the calling repo — used by the Lambda to scope the token. | yes |
| `aws_region`      | AWS region for SigV4 signing. (default: `eu-west-2`)                                               | no       |
| `username`        | Git `user.name` to configure. Recommended when the token is used for git commits.                  | no       |
| `email`           | Git `user.email` to configure. Recommended when the token is used for git commits.                 | no       |

`username` is typically the name of the GitHub App with `[bot]` on the end, e.g. `cdp-github-action[bot]`.

`email` is typically `<install-id>+<username>@users.noreply.github.com`. The install ID can be found at `https://api.github.com/users/<username>`, e.g. `147416134+cdp-github-action[bot]@users.noreply.github.com`.

## How to use it

Generally you will want to call this action after checking out the code.

```yaml
      - name: Check out code
        uses: actions/checkout@v4

      - name: Get token
        id: get-token
        uses: DEFRA/cdp-build-action/get-github-token-v2@main
        with:
          role_to_assume: arn:aws:iam::094954420758:role/github-actions-role
          token_service_url: https://cdp-mono-lambda.api.management.cdp-int.defra.cloud/github/token
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
2. Called the CDP token service (SigV4-signed POST to `/github/token`).
3. Set `GH_TOKEN` environment variable to the scoped token.
4. Configured the git credential helper to use the token for all `https://github.com` operations.
5. Set `git config user.name` and `git config user.email`, if provided.

## Branch protection

The same GitHub App bypass rules apply as with the original action. To push commits that bypass branch protection you must be using GitHub [rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets) (not classic branch protection), with the GitHub App added to the bypass list.

## Token scope

The token is **restricted to the calling repository only**. The repository name is derived from the OIDC session name embedded in the STS ARN — it cannot be overridden by the caller.

Tokens are created with the following fixed permissions:

| Permission      | Level   |
|-----------------|---------|
| `contents`      | `write` |
| `pull_requests` | `write` |
| `workflows`     | `write` |
