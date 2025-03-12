# CDP Build HotFix Action

Very similar to the standard build action except:
- It creates a patch release
- It does not tag the docker images as latest
- It adds a hotfix label to the image

## What does it do?



### Example usage

```
jobs:
  build:
	name: CDP-build-workflow
	runs-on: ubuntu-latest
	steps:
  	- name: Check out code
    	uses: actions/checkout@v4

  	- name: Build and Publish
    	uses: defra-cdp-sandpit/cdp-build-action/build@main
    	with:
      	github-token: ${{ secrets.GITHUB_TOKEN }}
```

If any steps are required before building the image, they can be inserted as steps between checking the code out and calling the build action.

## Inputs

`github-token`

This should always be set to ${{ secrets.GITHUB_TOKEN }}
It’s used to tag the repository when the version is incremented

`image-name`

Overrides the name of the docker image. By default it will use the name of the github repository, but in some use cases (repositories being renamed, multi-project repos etc) it may be required to override this value.

`push`

Sets whether the image will be published to the docker registries. Defaults to true, setting this value to false allows the build action to be used as a dry run/build test.

