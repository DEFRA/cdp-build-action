# CDP Build Test Action

End-to-end tests are designed to be run against the internal ECS environments. 
Like the services, it assumes that project has a valid docker file that builts into an image capable of running the test suite and then exiting.
The platform provides the infrastructure for running this container against the lower environments as well as provisinging a side-car container running chromedriver.

## What does it do?

- Increments the version number of the release (minor version by default, see below for more details of major/patch)
- Builds the projects Dockerfile
- Appends various labels and metadata to the docker image so it can be surfaced in the CDP Portal
- Handles publishing the image to the platforms Docker Registries

### Example usage

```
jobs:
  build:
	name: CDP-build-testsuite--workflow
	runs-on: ubuntu-latest
	steps:
  	- name: Check out code
    	uses: actions/checkout@v3

  	- name: Build and Publish
    	uses: defra-cdp-sandpit/cdp-build-test-action/build@main
    	with:
      	github-token: ${{ secrets.GITHUB_TOKEN }}
```

If any steps are required before building the image, they can be inserted as steps between checking the code out and calling the build action.

## Inputs

`version`

If you wish to use your own versioning systems for whatever reason (maybe a custom one that bumps the package.json version etc), you can override the version number via the version input.

`github-token`

This should always be set to ${{ secrets.GITHUB_TOKEN }}
It’s used to tag the repository when the version is incremented

`image-name`

Overrides the name of the docker image. By default it will use the name of the github repository, but in some use cases (repositories being renamed, multi-project repos etc) it may be required to override this value.

`push`

Sets whether the image will be published to the docker registries. Defaults to true, setting this value to false allows the build action to be used as a dry run/build test.

## Major and Patch releases

By default, each build will bump the minor version (e.g. 0.1.0 -> 0.2.0). To do a major or patch releases simply include `#major` or `#patch` in the commit message.

`git commit -m “bump to #major”`

Would result in 0.55.0 -> 1.0.0, while


```
git commit -a -m “possible bug fix #patch”
```

Would result in 0.55.0 -> 0.55.1
