"""Role checks for routes. Authentication itself happens in the security middleware."""

from collections.abc import Callable

from fastapi import HTTPException, Request, status

from app.models.enums import Role
from app.security.principal import PUBLIC, Principal

API_KEY_HEADER = "X-API-Key"


def current_principal(request: Request) -> Principal:
    return getattr(request.state, "principal", PUBLIC)


def require_role(*roles: Role) -> Callable[[Request], Principal]:
    """Dependency allowing only the listed roles; every call to the route is audited.

    No key → 401, a valid key with another role → 403. (An unknown or revoked key
    is already refused with 401 by the middleware, on every route.)
    """
    allowed = frozenset(roles)

    def dependency(request: Request) -> Principal:
        request.state.audit = True
        principal = current_principal(request)
        if principal.role in allowed:
            return principal
        if principal.role == Role.PUBLIC:
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED,
                detail=f"Authentication required: send an API key in the {API_KEY_HEADER} header.",
                headers={"WWW-Authenticate": API_KEY_HEADER},
            )
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="This API key's role cannot access this resource.")

    return dependency
