import os
import base64
import boto3
import json
from jinja2 import Environment, FileSystemLoader
from kubernetes import client, config


class ESOMigrateAWSSecretStore:
    secret_manager_prefix = os.getenv('SECRETS_MANAGER_PREFIX', 'k8s')
    cluster_secret_store_name = os.getenv('CLUSTER_SECRET_STORE_NAME', 'cluster-secret-store')
    refresh_interval = os.getenv('REFRESH_INTERVAL', '1m')

    client = boto3.client('secretsmanager')
    config.load_config()

    @classmethod
    def get_namespaces(cls):
        v1 = client.CoreV1Api()

        k8s_namespace = []
        ns = v1.list_namespace()

        for item in ns.items:
            k8s_namespace.append(item.metadata.name)

        return k8s_namespace

    @classmethod
    def get_namespace_secrets(cls, namespaces):

        v1 = client.CoreV1Api()

        k8s_secrets = {}
        for namespace in namespaces:
            k8s_secrets[namespace] = []
            secs = v1.list_namespaced_secret(namespace=namespace)
            for sec in secs.items:
                k8s_secrets[namespace].append(sec.metadata.name)

        return k8s_secrets

    @classmethod
    def migrate_eso(cls, secrets_dictionary):

        v1 = client.CoreV1Api()

        pairs = [(key, value) for key, values in secrets_dictionary.items() for value in values]

        for pair in pairs:
            k8s_ns = pair[0]
            k8s_secret_name = pair[1]

            sec = v1.read_namespaced_secret(k8s_secret_name, k8s_ns).data

            for key, value in sec.items():
                sec[key] = base64.b64decode(value).decode('utf-8')

            cls.write_aws_secret(secret_string=sec, name=k8s_ns + "-" + k8s_secret_name)

            cls.generate_external_secrets(secret_name=k8s_secret_name, namespace_name=k8s_ns)

    @classmethod
    def write_aws_secret(cls, secret_string, name):

        new_secret_string = json.dumps(secret_string)

        response = cls.client.create_secret(
            Name='{}-{}'.format(cls.secret_manager_prefix, name),
            SecretString='{}'.format(new_secret_string)
        )

        return response

    @classmethod
    def generate_external_secrets(cls, secret_name, namespace_name):

        environment = Environment(loader=FileSystemLoader("./"))
        template = environment.get_template("external-secret_tmpl.j2")

        content = template.render(
            secret_name=secret_name,
            namespace_name=namespace_name,
            secret_manager_prefix=cls.secret_manager_prefix,
            refresh_interval=cls.refresh_interval,
            cluster_secret_store_name=cls.cluster_secret_store_name
        )

        path = "manifests/{}".format(namespace_name)
        exist = os.path.exists(path)
        if not exist:
            os.makedirs(path)

        with open(f'{path}/{secret_name}.yaml', mode="w", encoding="utf-8") as message:
            message.write(content)
