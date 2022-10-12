# External Secrets Migration Tool
A Python Class to aid in simplifying the process of migrating Kubernetes secrets to [External Secrets Operator](https://external-secrets.io/) (ESO). All you need is a dictionary containing the namespaces and secrets within those namespaces. This tool was written one afternoon to help migrate secrets originally created by Kubeseal to use AWS Secrets Manager provider for ESO. 

**NOTE: Currently only supports AWS Secrets Manager Provider.** 

This tool helps with the following:

 1) Helps users to build a dictionary of namespaced secrets

 2) Create a secret on AWS Secrets Manager for each Kubernetes Secret (Each secret will be named as `$CLUSTER_PREFIX-namespace-secret_name`)

 3) Generate external secrets manifest files for each secret. Allows users to output external secrets manifest files to a desired location by using `MANIFEST_FOLDER` env variable OR as a default to  `manifests/namespace/secret-name.yaml`. This allows for easy integration for your currently deployment strategy via GitOps, kustomize, etc...


This tool assumes the following but should be modified to fit your needs:

1) You are using a ClusterSecretStore (`cluster-secret-store.yaml` as example).



## Prereqs
Tested on Python 3.10.6
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage
1) OPTIONAL: Set envrionment variables for K8s and AWS (See appropriate docs for K8s and Boto3 docs):

 
Example:
```
export KUBECONFIG=~/.kube/config.yaml
export AWS_PROFILE=profile
export AWS_REGION=aws-region

```

2) *OPTIONAL:* Set environment variables if you wish to change names of cluster secret store, interval time, or prefix of the secret created on AWS Secret Manager.
```
export CLUSTER_PREFIX='k8s-dev'
export CLUSTER_SECRET_STORE_NAME='dept-cluster-store'
export REFRESH_INTERVAL='10m'
export MANIFEST_FOLDER='kubernetes/overlays/dev'
```

3) Generate a dictionary containing the namespaces as the key and a list of secrets in each namespace you wish to retrieve.

```
secrets = {
            'default': ['secrets', 'password'],
            'tools': ['foo']
 }
```

4) Run the code:
```
from k8s_secrets import ESOMigrateAWSSecretStore

migrate_secrets = ESOMigrateAWSSecretStore.migrate_eso(secrets_dictionary=secrets)

```

5) Check the `manifests/` directory (or directory you specified for `$MANIFESTS_DIRECTORY`) for external secret yaml files and AWS Secrets Manager for newly created Secrets.
```
cat ./kubernetes/overlays/dev/default/secrets.yaml
...

apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: secrets
  namespace: default
spec:
  refreshInterval: 10m
  secretStoreRef:
    name: dept-cluster-store
    kind: ClusterSecretStore
  target:
    name: secrets
    creationPolicy: Owner
  dataFrom:
  - extract:
      key: k8s-dev-default-secrets
```

## Other Usage
As mentioned there are also ways of helping generate the dictionary such as finding namespaces and secrets. See the examples directory for other uses.  