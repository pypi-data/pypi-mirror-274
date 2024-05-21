"""
Accounts
https://docs.joinmastodon.org/methods/accounts/
"""
from httpx import Response
from tooi.api import request
from tooi.api.statuses import drop_empty_values


async def lookup(acct: str) -> Response:
    """
    Look up an account by name and return its info.
    https://docs.joinmastodon.org/methods/accounts/#lookup
    """
    return await request("GET", "/api/v1/accounts/lookup", params={"acct": acct})


async def relationships(account_ids: list[str], *, with_suspended: bool) -> Response:
    """
    Check relationships to other accounts
    https://docs.joinmastodon.org/methods/accounts/#relationships
    """
    params = {"id[]": account_ids, "with_suspended": with_suspended}
    return await request("GET", "/api/v1/accounts/relationships", params=params)


async def verify_credentials() -> Response:
    """
    Test to make sure that the user token works.
    https://docs.joinmastodon.org/methods/accounts/#verify_credentials
    """
    return await request("GET", "/api/v1/accounts/verify_credentials")


async def follow(
    account_id: str, *,
    reblogs: bool | None = None,
    notify: bool | None = None,
) -> Response:
    """
    Follow the given account.
    Can also be used to update whether to show reblogs or enable notifications.
    https://docs.joinmastodon.org/methods/accounts/#follow
    """
    json = drop_empty_values({"reblogs": reblogs, "notify": notify})
    return await request("POST", f"/api/v1/accounts/{account_id}/follow", json=json)


async def unfollow(account_id: str) -> Response:
    """
    Unfollow the given account.
    https://docs.joinmastodon.org/methods/accounts/#unfollow
    """
    return await request("POST", f"/api/v1/accounts/{account_id}/unfollow")


async def remove_from_followers(account_id: str) -> Response:
    """
    Remove the given account from your followers.
    https://docs.joinmastodon.org/methods/accounts/#remove_from_followers
    """
    return await request("POST", f"/api/v1/accounts/{account_id}/remove_from_followers")


async def block(account_id: str) -> Response:
    """
    Block the given account.
    https://docs.joinmastodon.org/methods/accounts/#block
    """
    return await request("POST", f"/api/v1/accounts/{account_id}/block")


async def unblock(account_id: str) -> Response:
    """
    Unblock the given account.
    https://docs.joinmastodon.org/methods/accounts/#unblock
    """
    return await request("POST", f"/api/v1/accounts/{account_id}/unblock")


async def mute(account_id: str) -> Response:
    """
    Mute the given account.
    https://docs.joinmastodon.org/methods/accounts/#mute
    """
    return await request("POST", f"/api/v1/accounts/{account_id}/mute")


async def unmute(account_id: str) -> Response:
    """
    Unmute the given account.
    https://docs.joinmastodon.org/methods/accounts/#unmute
    """
    return await request("POST", f"/api/v1/accounts/{account_id}/unmute")


async def pin(account_id: str) -> Response:
    """
    Add the given account to the user’s featured profiles.
    https://docs.joinmastodon.org/methods/accounts/#pin
    """
    return await request("POST", f"/api/v1/accounts/{account_id}/pin")


async def unpin(account_id: str) -> Response:
    """
    Remove the given account from the user’s featured profiles.
    https://docs.joinmastodon.org/methods/accounts/#unpin
    """
    return await request("POST", f"/api/v1/accounts/{account_id}/unpin")


async def note(account_id: str, comment: str) -> Response:
    """
    Sets a private note on a user.
    https://docs.joinmastodon.org/methods/accounts/#note
    """
    return await request("POST", f"/api/v1/accounts/{account_id}/note", json={"comment": comment})
