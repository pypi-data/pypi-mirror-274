from typing import Optional, cast
from datetime import datetime, UTC, timedelta
import httpx
from asyncgauth.types import MetadataTokenResponse
from asyncgauth.constants import (
    METADATA_SERVER_HEADER_KEY,
    METADATA_SERVER_HEADER_VAL,
    METADATA_SERVER_TOKEN_ENDPOINT,
    TOKEN_EXPIRY_BUFFER,
    METADATA_SERVER_PROJECT_ID_ENDPOINT,
)
from asyncgauth.exceptions import MissingToken


# https://cloud.google.com/docs/authentication/rest#metadata-server
class MetadataServerAuth:
    def __init__(self):
        self._token_expiry: Optional[datetime] = None
        self.access_token: Optional[str] = None
        self._project_id: Optional[str] = None

    def _token_exists_not_expired(self) -> bool:
        return bool(
            self.access_token
            and self._token_expiry
            and (datetime.now(tz=UTC) + timedelta(0, TOKEN_EXPIRY_BUFFER))
            < self._token_expiry
        )

    async def _refresh_token(self) -> None:
        headers = {METADATA_SERVER_HEADER_KEY: METADATA_SERVER_HEADER_VAL}
        async with httpx.AsyncClient() as client:
            raw_resp = await client.post(
                METADATA_SERVER_TOKEN_ENDPOINT, headers=headers
            )
            resp = MetadataTokenResponse.model_validate(raw_resp.json())
            self.access_token = resp.access_token
            self._token_expiry = datetime.now(tz=UTC) + timedelta(0, resp.expires_in)

    async def fetch_access_token(self) -> str:
        if self._token_exists_not_expired():
            return cast(str, self.access_token)

        await self._refresh_token()
        if not self.access_token:
            raise MissingToken("Failed to refresh access token")
        return self.access_token

    async def fech_id_token(self) -> str:
        # TODO: We could support ID token, but takes an audience param.
        # https://cloud.google.com/docs/authentication/get-id-token#metadata-server
        raise NotImplementedError("ID token not supported for metadata server auth")

    @property
    async def project_id(self) -> str:
        if self._project_id:
            return self._project_id
        headers = {METADATA_SERVER_HEADER_KEY: METADATA_SERVER_HEADER_VAL}
        async with httpx.AsyncClient() as client:
            raw_resp = await client.post(
                METADATA_SERVER_PROJECT_ID_ENDPOINT, headers=headers
            )
            self._project_id = raw_resp.text
        return self._project_id
