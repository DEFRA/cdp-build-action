# CDP API Docs

This action allows services to publish static html API docs to the CDP API hub.


## What does it do?

- Pushes a folder containing a static HTML site to one folder owned by the service: `api/<service-name>/<target>/`.
- Replaces what was there before (`aws s3 sync --delete`).

It does not work out versions or decide what to publish. The calling workflow does that, and calls the action once per folder.

### Example usage

Most static site generators bake the path a site is served from into its links and assets, so build once per target:

```yaml
      - name: Publish API docs (latest)
        uses: DEFRA/cdp-build-action/publish-api-docs@main
        with:
          path: ./docs/build-latest
          target: latest

      - name: Publish API docs (versioned)
        uses: DEFRA/cdp-build-action/publish-api-docs@main
        with:
          path: ./docs/build-versioned
          target: ${{ steps.version.outputs.version }}
```

The workflow needs `id-token: write` and the `AWS_REGION` and `AWS_ACCOUNT_ID` env values, to assume the service's build role.


## Inputs

`path` (required)

This must point at the folder containing the docs.

`target` (required)

The folder under `api/<service-name>/` to publish to, for example a version (`1.2.3`) or `latest`. It must be a single folder name.

`service-name`

Defaults to the repository name.

`bucket`

Defaults to `cdp-management-api-docs`.
