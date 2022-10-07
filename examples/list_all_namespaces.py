"""
Get a list of all namespaces within the cluster. This will help you generate a list you can then pass to get all secrets
in a namespace.
"""
from k8s_secrets import ESOMigrateAWSSec

if __name__ == '__main__':
    k8s_namespace_list = ESOMigrateAWSSecretStore.get_namespaces()
    print(k8s_namespace_list)