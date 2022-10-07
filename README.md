# External Secrets Migration Tool
A Python Class to aid in simplifying the process of migrating Kubernetes secrets to [External Secrets Manager](https://external-secrets.io/) (ESO). All you need is a JSON containing the namespaces and secrets within those namespaces. This tool was written one afternoon to help migrate secrets originally created by Kubeseal to use AWS Secrets Manager provider for ESO. Currently only supports AWS Secrets Manager Provider. 

This tool helps with the following:

 1) Helps users to build a dictionary of namespaced secrets

 2) Create a secret on AWS Secrets Manager for each Kubernetes Secret (Each secret will be named as `$secret_manager_prefix-namespace-secret_name`)

 3) Generate external secrets manifest files for each secret.


This tool assumes the following but should be modified to fit your needs:

1) You are using a ClusterSecretStore (`cluster-secret-store.yaml` as example).

2) Generates external secrets in the following directory structure: `manifests/namespace/secret-name.yaml`


## Prereqs
Tested on Python 3.10.6
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage
1) Set envrionment variables for K8s and AWS:

 
Example:
```
export KUBECONFIG=~/.kube/config.yaml
export AWS_PROFILE=profile
export AWS_REGION=aws-region

```

2) *OPTIONAL:* Set environment variables if you wish to change names of cluster secret store, interval time, or prefix of the secret created on AWS Secret Manager.
```
export SECRETS_MANAGER_PREFIX='k8s-dev'
export CLUSTER_SECRET_STORE_NAME='dept-cluster-store'
export REFRESH_INTERVAL='10m'
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

5) Check the `manifests/` directory for external secret yaml files and AWS Secrets Manager for newly created Secrets.

## Other Usage
As mentioned there are also ways of helping generate the dictionary such as finding namespaces and secrets. See the examples directory for other uses.  