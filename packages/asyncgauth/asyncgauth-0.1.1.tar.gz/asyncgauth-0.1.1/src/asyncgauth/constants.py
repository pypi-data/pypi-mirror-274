OAUTH_TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"

METADATA_SERVER_TOKEN_ENDPOINT = (
    "http://169.254.169.254/computeMetadata/v1/instance/service-accounts/default/token"
)
METADATA_SERVER_PROJECT_ID_ENDPOINT = (
    "http://169.254.169.254/computeMetadata/v1/project/project-id"
)
METADATA_SERVER_HEADER_KEY = "Metadata-Flavor"
METADATA_SERVER_HEADER_VAL = "Google"

TOKEN_EXPIRY_BUFFER = 30  # seconds

LEGACTY_PROJECT_ENV_VAR = "GCLOUD_PROJECT"
PROJECT_ENV_VAR = "GOOGLE_CLOUD_PROJECT"

# Relative from $HOME
GCLOUD_ADC_PATH = ".config/gcloud/application_default_credentials.json"
