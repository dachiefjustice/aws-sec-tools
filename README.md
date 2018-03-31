# AWS Security Auditing Container
---

## General
This Docker container aims to ease the process of auditing AWS environments for security issues. It bundles handy open-source AWS security analysis tools (plus the AWS CLI/Shell), handles their installation/dependencies, and provides a convenience launcher script. The focus is on finding issues by interrogating AWS APIs and analyzing the results (rather than e.g. looking inside EC2 instances, at application code, or other resources that are opaque to the AWS APIs).

## Tools
Thanks to the tool authors for their efforts!

- [AWS CLI](https://aws.amazon.com/cli/): manually interrogate AWS APIs
- [AWS Shell](https://github.com/awslabs/aws-shell): manually interrogate AWS APIs, in a helpful interactive environment
- [Scout2](https://github.com/nccgroup/Scout2): call various AWS APIs, assess security posture, generate report
- [Prowler](https://github.com/Alfresco/prowler): call various AWS APIs, assess security posture focusing on the [AWS CIS Foundations Benchmark](https://d0.awsstatic.com/whitepapers/compliance/AWS_CIS_Foundations_Benchmark.pdf), generate report
- [CloudSploit Scans](https://github.com/cloudsploit/scans): call various AWS APIs, assess security posture, report to STDOUT 
- [s3-inspector](https://github.com/kromtech/s3-inspector): examine S3 bucket permissions, report to STDOUT
- [AWS Bucket Dump](https://github.com/jordanpotti/AWSBucketDump): unauthenticated, wordlist-based S3 bucket enumeration and loot search.

## Prerequisites
- Docker (for building/running the container)
- git (for cloning this repo)
- Read-only AWS credentials (convenient if they're in `~/.aws` on your Docker host)
- Internet access (for tool/dependency installation, and running tools)

## Building
On a host meeting the prereqs:

1. Clone this repo: `git clone https://github.com/mimestyping/aws-sec-tools aws-sec-tools && cd aws-sec-tools` (or manually download/extract)
2. Build the container from the directory containing the Dockerfile: `docker build -t aws-sec-tools:01 .` (or whatever tag you want)
3. (Optional, but recommended) Make a directory for storing tool output: `mkdir ~/aws-reports`

## Running
Once you have the container built, on a host meeting the prereqs:

1. Run the container interactively. It's easiest to bind-mount your AWS dir and a reports dir into the container (adjust container name/tag and volume mounts as needed): `docker run -it -v ~/.aws:/home/awssec/.aws -v ~/aws-reports:/home/awssec/reports aws-sec-tools:01` 
2. Decide if you want want to run a tool manually, or use the launcher to get started quickly.
  - Manual tool launch:
    - `cd ~/toolname`
    - (For Python-based tools, i.e. most of them) Activate the virtualenv: `source ~/toolname/bin/activate`
    - Run the tool 
  - Use the tool launcher script:
    - `./tool_launcher.py`
    - Select the tool you want to run
    - After running a tool from the launcher, you might find yourself in the tool's virtualenv (handy for re-running the tool with different parameters, maybe to redirect STDOUT to a file in `~/reports`, etc.). Alternately, `exit` the bash shell invoked by the launcher script, re-run `~/tool_launcher.py`, and choose another tool.
 
## Notes
- Familiarize yourself with the tools included in this image before running them.
- Use read-only AWS credentials. The AWS-managed SecurityAudit policy (arn:aws:iam::aws:policy/SecurityAudit) is a good starting point; customize as appropriate to your AWS environment/the tools you're using.
- To get the latest tool versions, delete the container image and re-build. The Dockerfile installs each tool via pip or clones the tool's master branch from GitHub.
- Some tools launch automatically when invoked from the tool launcher script (they're labeled as such in the launcher).
- CloudSploit Scans needs AWS credentials, but doesn't check ~/.aws/credentials for them. The tool launcher script assumes you're using an IAM user (rather than role or other temporary credential), prompts for access key and secret key, and sets the `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` environment variables before invoking the tool. Alternately, set the `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and `AWS_SESSION_TOKEN` environment variables, then run the tool manually.
- To manually run a tool, `cd` into the tool's directory (under ~) and (for Python-based tools with a `~/toolname/bin` directory) activate the tool's virtualenv with `source ~/toolname/bin/activate`. `deactivate` when you're done using a tool with a virtualenv.
- tmux is available (for convenience/running multiple tools at once in a single container instance).
- git is available.
