"""
Canonical-host redirect.

If CANONICAL_HOST is set (e.g. "loanphp.live"), any request that reaches the
app on a different host (the Railway-generated domain, a www. variant, an old
preview URL, etc.) is 301-redirected to the same path on the canonical host.

Disabled by default: if CANONICAL_HOST is empty the middleware is a no-op, so
nothing changes until the env var is configured on Railway.
"""

import os

from django.http import HttpResponsePermanentRedirect

CANONICAL_HOST = os.getenv("CANONICAL_HOST", "").strip().lower()

# Hosts that must never be redirected (local dev + platform health checks).
_EXEMPT_HOSTS = {"localhost", "127.0.0.1", "testserver"}


class CanonicalHostRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if CANONICAL_HOST:
            host = (request.get_host() or "").split(":")[0].lower()
            if host and host not in _EXEMPT_HOSTS and host != CANONICAL_HOST:
                return HttpResponsePermanentRedirect(
                    f"https://{CANONICAL_HOST}{request.get_full_path()}"
                )
        return self.get_response(request)
