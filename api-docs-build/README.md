# CDP API docs build

Builds a tenant's API docs (`docs/guides/` and `docs/openapi/swagger.json`) with the shared
`defradigital/cdp-api-docs-builder` image.

## Build for publishing

The site's links include the path it is served from, so build once per target:

```yaml
- name: Build latest docs
  id: latest
  uses: DEFRA/cdp-build-action/api-docs-build@main
  with:
    target: latest

- name: Publish latest docs
  uses: DEFRA/cdp-build-action/publish-api-docs@main
  with:
    path: ${{ steps.latest.outputs.path }}
    target: latest
```

## Dry run on pull requests

`dry-run: true` builds and checks the docs, then keeps nothing. It fails on broken links,
broken anchors, broken Markdown links, MDX that doesn't compile, and an invalid `swagger.json`.

```yaml
- name: Check API docs
  uses: DEFRA/cdp-build-action/api-docs-build@main
  with:
    dry-run: true
```

## Inputs

`target`

Folder the docs will be served from under `api/<service-name>/` (unless `base-url` is set), e.g. `latest` or `1.2.3`. Required unless `dry-run` is `true`.

`dry-run`

Build and check only, keep nothing. Defaults to `false`.

`service-name`

Defaults to the repository name.

`base-url`

Optional override for the built site's base URL, for example `/` for
[cdp-api-docs-site](https://github.com/DEFRA/cdp-api-docs-site), which is published at the bucket root.
When empty, the default is `/api/<service-name>/<target>/`.
It must match where the output is uploaded, so don't combine it with `publish-api-docs`,
which always uploads to `api/<service-name>/<target>/`.

`builder-version`

Builder image tag. Defaults to `latest`.
