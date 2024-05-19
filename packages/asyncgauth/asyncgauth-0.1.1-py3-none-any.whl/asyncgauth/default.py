from asyncgauth.oauth import OfflineOauthWithRefresh
from asyncgauth.metadata_server_auth import MetadataServerAuth
from asyncgauth.types import GcloudAdcFile
from typing import Union
from pathlib import Path
from os import getenv
from json import loads


def default() -> Union[OfflineOauthWithRefresh, MetadataServerAuth]:
    """Entrypoint for all auth, order of precedence for auth:
    1. Metadata server
    2. Gcloud application default credentials file
    """
    home_dir = getenv("HOME")

    # No $HOME env var, assuming GCE
    if not home_dir:
        return MetadataServerAuth()

    path_to_adc = f"{home_dir}/.config/gcloud/application_default_credentials.json"
    adc_file_maybe = Path(path_to_adc)
    if not adc_file_maybe.is_file():
        return MetadataServerAuth()

    # Gcloud file exists, use it
    with adc_file_maybe.open() as f:
        adc = GcloudAdcFile.model_validate(loads(f.read()))
        return OfflineOauthWithRefresh(
            client_id=adc.client_id,
            client_secret=adc.client_secret,
            refresh_token=adc.refresh_token,
            project_id=adc.quota_project_id,
        )
