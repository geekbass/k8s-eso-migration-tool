"""
Generate a dictionary of all secrets in a list of namespaces. Use this to build the final dictionary used for migration.
You can simply remove the secrets you dont want.
"""
from k8s_secrets import ESOMigrateAWSSec

if __name__ == '__main__':
    k8s_namespaces = ['default', 'test', 'argo', 'kubeflow', 'spark']

    # From the list of Namespaces return a dictionary with every secret in each namespace
    k8s_secrets_dict = ESOMigrateAWSSecretStore.get_namespace_secrets(namespaces=k8s_namespaces)
    print(k8s_secrets_dict)