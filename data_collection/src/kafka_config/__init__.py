import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file


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
# ENDPOINT_SCHEMA_URL = os.getenv("ENDPOINT_SCHEMA_URL", None)
# ENDPOINT_SCHEMA_URL = os.environ.get("ENDPOINT_SCHEMA_URL", None)
ENDPOINT_SCHEMA_URL = os.environ["ENDPOINT_SCHEMA_URL"]


# This function will return dictionary of sasl configuration
def sasl_conf():
    """
    This function will return dictionary of sasl configuration
    """
    sasl_conf = {
        "sasl.mechanism": SSL_MACHENISM,
        # Set to SASL_SSL to enable TLS support.
        #  'security.protocol': 'SASL_PLAINTEXT'}
        "bootstrap.servers": BOOTSTRAP_SERVER,
        "security.protocol": SECURITY_PROTOCOL,
        "sasl.username": API_KEY,
        "sasl.password": API_SECRET_KEY,
    }
    # print(sasl_conf)
    return sasl_conf


def schema_config():
    """
    This function will return dictionary of schema registry configuration
    """
    return {
        "url": ENDPOINT_SCHEMA_URL,
        "basic.auth.user.info": f"{SCHEMA_REGISTRY_API_KEY}:{SCHEMA_REGISTRY_API_SECRET}",
    }


if __name__ == "__main__":
    sasl_conf()
