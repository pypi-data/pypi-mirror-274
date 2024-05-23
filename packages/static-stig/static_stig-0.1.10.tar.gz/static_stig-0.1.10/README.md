# Static STIG

## Overview

This tool allows users to run OSCAP STIGs against a static image instead of waiting to do so at runtime. It will pull the image and determine its base distro and run a standard STIG profile against the image before outputting the results to a file on your local machine.

## Requirements

Static STIG requires docker to run. Ensure that Docker is installed and your user is a part of the Docker group so the use of sudo isn't required to run docker commands. Additionally, ensure that your user owns the directory you are running Static STIG in.

## How to Run

Run `pip install -U static-stig`

To run Static STIG, simply run package and give it the desired target image: `static-stig -i registry_url/repo/image:tag`

For exammple, to run a stig against the latest ubuntu image run `static-stig -i docker.io/library/ubuntu:latest`

To run a STIG against an image in a private repository, run the same command with the credential flags: `static-stig -i registry_url/repo/image:tag -u username -p password -r registry_url`

## Future Features

- More compatibility with OSCAP XCCDF options
- Compatibility with more OSCAP Profiles
- Add a flag to allow specifying a profile

## Known Shortcomings

- The DISA STIG list lags a few years behind releases of OS versions
- The STIG list used here isn't compatible with MacOS based images