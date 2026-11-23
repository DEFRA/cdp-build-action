# tf-build/secrets

This action is now deprecated! Switch to using DEFRA/get-github-token-v2.

## Migration

1. Ensure job is using the cdp self-hosted runner.
2. Check OIDC role for repo has the github-trigger-monolambda-role
3. Check the monolambda config grants the repo the permissions you need.
4. Update the workflow

**Old workflow:**

```yml
      - name: Secrets - prepare
        id: tf-secrets
        uses: DEFRA/cdp-build-action/tf-build/secrets@stable
        with:
          role_to_assume: <ROLE_TO_ASSUME>
          gh_actions_secrets: cdp/platform/gh_actions/DEFRA
          gh_app_private_key: key1/key2/etc
          use_defra_org: true
```

**Replace with**
```yml
    - name: Get GitHub Token
      uses: DEFRA/cdp-build-actions/get-github-token-v2@stable
      with:
        role_to_assume: arn:aws:iam::094954420758:role/github-trigger-monolambda-role
        token_service_url: https://dn6yr97qx9.execute-api.eu-west-2.amazonaws.com/management/github/token
        email: 147416134+cdp-github-action[bot]@users.noreply.github.com
        username: cdp-github-action[bot]

    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v6
      with:
        aws-region: ${{ env.AWS_REGION }}
        role-to-assume: <ROLE_TO_ASSUME>

    - run: aws sts get-caller-identity
      shell: bash
```
