# CDP Publish Database Migration

This action allows services to publish liquibase migrations so they can be applied to database instances in CDP environments.
Currently this action is intended to work with liquibase. Other tools may be supported in the future, but not currently.


## What does it do?

- Checks the liquibase changelog files actually exist.
- Archives the changelog/changeset files into a .tgz file.
- Versions the file using the current version tag on that branch.
- Pushes migration files to S3 so they can be used in CDP.

### Example usage

```yaml
jobs:
  build:
    name: CDP-build-workflow
    runs-on: ubuntu-latest
    steps:
      - name: Check out code
        uses: actions/checkout@v4

      - name: Build and Publish
        uses: DEFRA/cdp-build-action/build@main
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}

      - name: Publish database migrations
        uses: DEFRA/cdp-build-action/publish-db-migrations@main
        with:
          path: ./changelog
          github-token: ${{ secrets.GITHUB_TOKEN }}

```

This action is intended to be run _after_ DEFRA/cdp-build-action/build has finished running.
This ensures db migrations are versioned using the same version number as the release of the service.

## Inputs

`path` (required)

This must be the path to the folder containing the liquibase changelog files. If the folder is empty or does not exist the action will fail.

`version`

By default the action will get the version number for the latest tag. If you want to override this, you can set the `version` input.
You will not be able to overwrite existing version numbers if they've already been published.

`github-token`

This should always be set to `${{ secrets.GITHUB_TOKEN }}`.
It’s used to tag the repository when the version is incremented

`force`

By default the action will only publish the database migrations if the files set in `path` have changed.
Setting the `force` flag ignores this check and publishes a new version regardless of weather the files have changed or not.


