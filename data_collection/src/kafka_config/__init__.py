import os

# Authentication related variables ---------------------------------------------
# Define the security protocol for Kafka to ensure a secure connection between the client and server machines.
SECURITY_PROTOCOL = "SASL_SSL"
# Specify the SSL mechanism being used (in this case, "PLAIN" authentication).
SSL_MACHENISM = "PLAIN"

# Cloud API related variables ----------------------------------------------
# Retrieve the API key from the environment variables.
# This API key is crucial for authenticating and authorizing the application to interact with the Kafka cluster.
API_KEY = os.getenv("API_KEY", None)
# Retrieve the API secret key from the environment variables.
# The API secret key is essential for securely accessing and interacting with the Kafka cluster.
API_SECRET_KEY = os.getenv("API_SECRET_KEY", None)
# Retrieve the Kafka bootstrap server address from the environment variables.
# The bootstrap server enables the application to connect to the Kafka cluster.
BOOTSTRAP_SERVER = os.getenv("BOOTSTRAP_SERVER", None)

# Schema registry related variables --------------------------------------------
# Retrieve the schema registry API key from the environment variables.
# This API key is used for authentication when working with the schema registry.
SCHEMA_REGISTRY_API_KEY = os.getenv("SCHEMA_REGISTRY_API_KEY", None)
# Retrieve the schema registry API secret from the environment variables.
# The schema registry API secret key is used to securely access and manage schemas.
SCHEMA_REGISTRY_API_SECRET = os.getenv("SCHEMA_REGISTRY_API_SECRET", None)
# Retrieve the schema URL from the environment variables.
# The schema URL is used to validate the data format within the Kafka ecosystem.
ENDPOINT_SCHEMA_URL = os.getenv("ENDPOINT_SCHEMA_URL", None)


# API_KEY = 'ES3RCTGXMG4EWMHV'
# ENDPOINT_SCHEMA_URL  = 'https://psrc-em82q.us-east-2.aws.confluent.cloud'
# API_SECRET_KEY = 'Cu6TxnHheRQrM1xuSatwY6tECOqne+gMAptkFa1u3NeRRFNnaWlNKQHqHCmhKO7U'
# BOOTSTRAP_SERVER = 'pkc-lzvrd.us-west4.gcp.confluent.cloud:9092'
# API_KEY = os.environ('API_KEY',None)
# ENDPOINT_SCHEMA_URL  = os.environ('ENDPOINT_SCHEMA_URL',None)
# API_SECRET_KEY = os.environ('API_SECRET_KEY',None)
# BOOTSTRAP_SERVER = os.environ('BOOTSTRAP_SERVER',None)

# # SECURITY_PROTOCOL = os.getenv('SECURITY_PROTOCOL',None)
# SSL_MACHENISM = os.getenv('SSL_MACHENISM',None)
# SCHEMA_REGISTRY_API_KEY = 'RYKWGSZEG2ASOS4C'
# SCHEMA_REGISTRY_API_SECRET = 'r3HsabV0dB094ThMFslCcZtTQ2eHLcR+Ja5ZMSSJORReem86zZqgeOav+cV2cACL'
# SCHEMA_REGISTRY_API_KEY = os.environ('SCHEMA_REGISTRY_API_KEY',None)
# SCHEMA_REGISTRY_API_SECRET = os.environ('SCHEMA_REGISTRY_API_SECRET',None)


def sasl_conf():
    sasl_conf = {
        "sasl.mechanism": SSL_MACHENISM,
        # Set to SASL_SSL to enable TLS support.
        #  'security.protocol': 'SASL_PLAINTEXT'}
        "bootstrap.servers": BOOTSTRAP_SERVER,
        "security.protocol": SECURITY_PROTOCOL,
        "sasl.username": API_KEY,
        "sasl.password": API_SECRET_KEY,
    }
    print(sasl_conf)
    return sasl_conf


def schema_config():
    return {
        "url": ENDPOINT_SCHEMA_URL,
        "basic.auth.user.info": f"{SCHEMA_REGISTRY_API_KEY}:{SCHEMA_REGISTRY_API_SECRET}",
    }


if __name__ == "__main__":
    sasl_conf()
