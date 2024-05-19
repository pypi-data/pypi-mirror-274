from datetime import datetime, UTC, timedelta
from typing import Optional, cast
import httpx
from asyncgauth.constants import OAUTH_TOKEN_ENDPOINT, TOKEN_EXPIRY_BUFFER
from asyncgauth.types import OauthOfflineRefreshResponse
from asyncgauth.exceptions import MissingToken


# https://developers.google.com/identity/protocols/oauth2/web-server#offline
class OfflineOauthWithRefresh:
    def __init__(
        self, client_id: str, client_secret: str, refresh_token: str, project_id: str
    ):
        self._client = httpx.AsyncClient()
        self._client_id = client_id
        self._client_secret = client_secret
        self._refresh_token = refresh_token
        self._token_expiry: Optional[datetime] = None

        self.project_id = project_id
        self.access_token: Optional[str] = None
        self.id_token: Optional[str] = None

    def _token_exists_not_expired(self, token: Optional[str]) -> bool:
        return bool(
            token
            and self._token_expiry
            and (datetime.now(tz=UTC) + timedelta(0, TOKEN_EXPIRY_BUFFER))
            < self._token_expiry
        )

    async def _refresh_tokens(self) -> None:
        params = {
            "grant_type": "refresh_token",
            "client_id": self._client_id,
            "client_secret": self._client_secret,
            "refresh_token": self._refresh_token,
        }
        async with self._client as client:
            raw_resp = await client.post(OAUTH_TOKEN_ENDPOINT, params=params)
            resp = OauthOfflineRefreshResponse.model_validate(raw_resp.json())
            self.access_token = resp.access_token
            self.id_token = resp.id_token
            self._token_expiry = datetime.now(tz=UTC) + timedelta(0, resp.expires_in)

    async def fetch_access_token(self) -> str:
        if self._token_exists_not_expired(self.access_token):
            return cast(str, self.access_token)

        await self._refresh_tokens()
        if not self.access_token:
            raise MissingToken("Failed to refresh access token")
        return self.access_token

    async def fetch_id_token(self) -> str:
        if self._token_exists_not_expired(self.id_token):
            return cast(str, self.id_token)

        await self._refresh_tokens()
        if not self.id_token:
            raise MissingToken("Failed to refresh ID token")
        return self.id_token
