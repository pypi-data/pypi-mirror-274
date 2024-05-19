import asyncio
import asyncgauth
import httpx


async def main():
    auth = asyncgauth.default()
    print(await auth.fetch_access_token())


asyncio.run(main())
#  c = asyncgauth.Client()
#  b = c.get_bucket("asyncgauthtest")
#  asyncio.run(b.get_blob("pkgbuild.txt"))
