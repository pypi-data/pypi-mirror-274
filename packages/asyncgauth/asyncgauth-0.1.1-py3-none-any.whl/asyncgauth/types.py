from typing import Optional
from pydantic import BaseModel


class GcloudAdcFile(BaseModel):
    account: Optional[str] = None
    client_id: str
    client_secret: str
    quota_project_id: str
    refresh_token: str
    type: str
    universe_domain: str


class MetadataTokenResponse(BaseModel):
    access_token: str
    expires_in: int
    token_type: str


class OauthOfflineRefreshResponse(BaseModel):
    access_token: str
    expires_in: int  # seconds
    scope: str
    token_type: str
    id_token: str
