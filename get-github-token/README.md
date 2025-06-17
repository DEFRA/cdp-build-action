# CDP get-github-token Action

The `get-github-token` retrieves a GitHub app private key from AWS Secret Manager, uses it to get a PAT token and then sets the PAT token as the default git credentials inside the workflow.

This can be used when you need to commit code to a repository that has branch protection enabled.
The default github workflow secret (i.e. `github.secret`) does not have an ID associated with it, so it cannot be added to the bypass list in the branch protection rules.

## Inputs

| Input          | Description                                                           | Required |
|----------------|-----------------------------------------------------------------------|----------|
| role_to_assume | The IAM role to assume to get the secret from secrets manager.        | yes      |
| private_key_id | ARN of the secret in secrets manager that holds the app's private key | yes      |
| app_id         | App ID associated with the private key                                | yes      |
| aws_region     | AWS Region to use. (default `eu-west-2`)                              | no       |
| username       | username of the bot account. This shows up in the commit message      | no       |
| email          | email address of the bot account.                                     | no       |
|                |                                                                       |          |

Username is typically the name of the github application with `[bot]` on the end, e.g. `my-github-app[bot]`.

Email is typically `<install-id>+<username>@users.noreply.github.com`. 
The install id can be found by going to `https://api.github.com/users/<username>`. 
The username is the same username from he previous step.

e.g. `12345678+my-github-app[bot]@users.noreply.github.com`

## How to use it

Generally you will want to call this action after checking out the code.
```
      - name: Check out code
        uses: actions/checkout@v4

      - name: Get token
        id: get-token
        uses: DEFRA/cdp-build-action/get-github-token@main
        with:
          role_to_assume: arn:aws:iam::000000000000:role/my-repos-odic-role
          private_key_id: path/to/gh_app/private-key
          app_id: 123456
          email: ${{ env.cdp-gitbot-email }}
          username: ${{ env.cdp-gitbot-name }}
```

After it runs it will have done the following:
1. Set `GH_TOKEN` environment variable to be the new token from private key.
2. Configured git to use the new token
3. Configured git to use the username and email, if set.

## Branch protection

To be able to have the workflow bypass branch protection, you must first be using the new style github [rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets) 
rather than the classic 'branch protection'. Rulesets allow you to set which users or apps can bypass the rules. Add your app into the bypass list.
