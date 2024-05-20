## EMR Serverless Custom Sparkmagic Authenticator.

This package provides a custom implementation Jupyter Incubator Spark magic Kernel [Custom Authenticator interface](https://github.com/jupyter-incubator/sparkmagic#using-a-custom-authenticator-with-sparkmagic)
to enable integration from EMR-Serverless Application.
The Custom Authenticator subclasses shipped in this package computes the [AWS Signature Version 4](https://docs.aws.amazon.com/AmazonS3/latest/API/sig-v4-authenticating-requests.html)
and appends HTTP Authentication headers to the request to the public livy endpoint exposed by EMR Serverless Application.

## Pre-requisite
This package assumes that spark magic package is either already installed or will be installed by the 
consumer on the python environment to be used.

## Steps to Install
```shell
pip install emr-serverless-customauth
```
This will install the package along with its dependencies.

## Configuring Custom Authenticator with Sparkmagic
Please refer to the steps mentioned here on the [spark magic github repository](https://github.com/jupyter-incubator/sparkmagic?tab=readme-ov-file#custom-authenticators).
1. Add a new custom auth to `authenticators` map present in sparkmagic `config.json` file. 
```json
{
   ....
    "authenticators": {
        "Kerberos": "sparkmagic.auth.kerberos.Kerberos",
        "None": "sparkmagic.auth.customauth.Authenticator",
        "Basic_Access": "sparkmagic.auth.basic.Basic",
        "EMRServerlessAuth": "emr_serverless_customauth.customauthenticator.EMRServerlessCustomSigV4Signer"
  },
  ....
}
```

2. Update the corresponding python and/or scala kernels present in sparkmagic `config.json` file to use the `EMRServerlessAuth`. 
```json
{
  "kernel_python_credentials": {
    "username": "",
    "password": "",
    "url": "https://<emr-serverless-app-id>.livy.emr-serverless-services.<aws-region>.amazonaws.com",
    "auth": "EMRServerlessAuth"
  },
  "kernel_scala_credentials": {
    "username": "",
    "password": "",
    "url": "https://<emr-serverless-app-id>.livy.emr-serverless-services.<aws-region>.amazonaws.com",
    "auth": "EMRServerlessAuth"
  }
  .....
```

Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.