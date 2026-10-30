# CDP API Docs

This action allows services to publish static html API docs to the CDP API hub.


## What does it do?

- Pushes a folder containing a static HTML site to a subfolder owned by the service.

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

      - name: Publish api docs
        uses: DEFRA/cdp-build-action/publish-api-docs@main
        with:
          path: ./docs/dist
          github-token: ${{ secrets.GITHUB_TOKEN }}

```

Tenants may store their migration files in any folder. The `path` value is persisted in the published `migrations.metadata.json` and is automatically used by the CDP deployment pipeline when running `liquibase`. The default path (`./changelog`) is preserved for existing services that do not specify a custom location.

```yaml
      - name: Publish database migrations (custom path)
        uses: DEFRA/cdp-build-action/publish-api-docs@main
        with:
          path: ./docs/dist
          github-token: ${{ secrets.GITHUB_TOKEN }}
```


## Inputs

`path` (required)

This must point at the folder containing the docs.

`version`

By default the action will get the version number for the latest tag. If you want to override this, you can set the `version` input.
You will not be able to overwrite existing version numbers if they've already been published.

`github-token`

This should always be set to `${{ secrets.GITHUB_TOKEN }}`.
It’s used to tag the repository when the version is incremented

`update-latest`

Updates the `/api/service-name/latest` alias to use these docs, overwritting the current latest release.

