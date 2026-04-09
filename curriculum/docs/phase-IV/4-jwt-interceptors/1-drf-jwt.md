# DRF JSON Web Tokens

## Introduction

Our application already handles authentication using DRF's built-in token system stored in `httpOnly` cookies. That approach works, but it has a fundamental limitation: every authenticated request requires a database lookup to validate the token. As our application scales and handles more concurrent users, that cost compounds quickly.

In this lesson we are going to replace DRF's token system with **JSON Web Tokens (JWTs)**, a stateless authentication strategy that validates requests cryptographically — no database lookup required on every request.

---

## Lesson

### What is a JSON Web Token

A **JSON Web Token** is a compact, self-contained string that carries claims (pieces of information) about a user and is cryptographically signed so its integrity can be verified without hitting a database. It was standardized in [RFC 7519](https://datatracker.ietf.org/doc/html/rfc7519) as a solution to stateless authentication across distributed systems.

A JWT is made up of three dot-separated parts, each Base64URL-encoded:

```
header.payload.signature
```

- **Header** — declares the token type (`JWT`) and the signing algorithm (e.g. `HS256`).
- **Payload** — the actual claims: who the user is (`user_id`), when the token expires (`exp`), when it was issued (`iat`), and any other data you embed.
- **Signature** — a hash of the encoded header + payload using a secret key only the server knows. This is what makes the token tamper-proof.

Because the signature is derived from your server's `SECRET_KEY`, any server with that key can verify a token independently. No database row needs to be fetched to confirm authenticity — the math either checks out or it doesn't. This is what makes JWTs **stateless**.

JWTs typically come in two flavors that work together:

- **Access token** — short-lived (minutes). Sent with every request to prove identity.
- **Refresh token** — long-lived (days/weeks). Used only to request a new access token when the current one expires.

---

### DRF Token vs JWT Token

Both DRF Token auth and JWT auth are valid strategies for securing an API, but they operate very differently under the hood.

**DRF Token** is **stateful** — the token is a random string stored in the `authtoken_token` database table. Every time the client sends that token, Django queries the database to look it up and find the associated user. This means:

- There is exactly **one** token per user (1-to-1 relationship).
- Revoking access is simple — delete the row.
- But every request carries a DB round-trip cost.

**JWT** is **stateless** — the token encodes the user's identity and an expiry timestamp directly in the token string, and it is signed with the server's secret key. Django verifies the signature mathematically. This means:

- One user can have **many** valid tokens simultaneously (many-to-1 relationship) — think logging in on your laptop, your phone, and your work computer all at once.
- No database query is needed to validate the token.
- Revocation requires an optional **blacklist** mechanism (more on this below).

| Feature | DRF Token | JWT |
|---|---|---|
| Storage | Database row | Cryptographic signature |
| User relationship | 1-to-1 (one token per user) | Many-to-1 (many tokens per user/device) |
| Validation method | Database lookup | Signature verification |
| DB hit per request | Yes | No |
| Built-in expiry | No (manual) | Yes (configurable) |
| Revocation | Delete row from DB | Blacklist (optional app) |
| Multi-device support | No | Yes |

---

### How Does It Work (Conceptually)

Think of DRF Token auth like a **coat check at a restaurant**. When you arrive you hand over your coat, they give you a numbered ticket, and they write your name next to that number in their ledger. Every time you want your coat back you show the ticket, they look up the number in the ledger, confirm it is yours, and retrieve it. The coat check counter (the database) has to be consulted every single time.

JWT works more like a **theme park wristband**. When you pay for admission at the front gate, the park prints a wristband stamped with your name, your ticket tier (VIP, standard, etc.), and the date it expires. Every ride operator can read that wristband directly and let you through — they do not need to call the front gate to confirm you paid. The information and the proof of authenticity are baked right into the band. When the wristband expires, you go back to the gate (the refresh endpoint) and get a new one using your receipt (the refresh token).

The refresh token is that receipt — it does not get you onto rides, but it proves you are entitled to a new wristband. It lives longer than the wristband itself, and when it is used you get a fresh wristband and a fresh receipt, while the old receipt is voided (blacklisted).

---

### Applying it to Django

#### Installing DRF JWT

`djangorestframework-simplejwt` is the recommended JWT library for Django REST Framework. It integrates seamlessly with DRF's authentication class system, which makes migrating from our current `CookieAuthentication` pattern straightforward.

Add it to `requirements.txt`:

```text
# server/requirements.txt

djangorestframework-simplejwt==5.5.0
```

Then install it in your environment:

```bash
pip install djangorestframework-simplejwt
```

Next, update `INSTALLED_APPS` in `settings.py`. We are removing `rest_framework.authtoken` (DRF's old token app) and adding two new entries: the core simplejwt app and its optional **token blacklist** app. The blacklist app gives us a database table to record invalidated refresh tokens — this is what lets logout actually revoke access.

We also add a `SIMPLE_JWT` configuration block to control token lifetimes and rotation behavior:

```python
# server/task_proj/settings.py
from datetime import timedelta

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'rest_framework_simplejwt',              # add
    'rest_framework_simplejwt.token_blacklist', # add
    # 'rest_framework.authtoken',             # remove
    'task_app',
    'user_app',
]

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
}
```

`ACCESS_TOKEN_LIFETIME` of 15 minutes keeps the attack window small — if an access token is ever intercepted, it expires quickly. `REFRESH_TOKEN_LIFETIME` of 7 days matches the original session length our app offered. `ROTATE_REFRESH_TOKENS` means every time a client exchanges a refresh token for a new access token, it also gets a brand new refresh token. `BLACKLIST_AFTER_ROTATION` immediately invalidates the old refresh token so it can never be reused. Together these two settings implement **refresh token rotation**, a security best practice.

Because we added `token_blacklist`, run migrations to create the blacklist tables:

```bash
python manage.py migrate
```

---

#### Updating User Authentication Views for JWT

With DRF Token auth we called `Token.objects.create(user=new_user)` and got back a single opaque string. With simplejwt we call `RefreshToken.for_user(user)` and get back a `RefreshToken` object. From that object we can derive both the refresh token string and the access token string.

We also need two separate cookie lifetimes now — one short (matching `ACCESS_TOKEN_LIFETIME`) and one long (matching `REFRESH_TOKEN_LIFETIME`). We update our helper function to accept a `days` argument:

```python
# server/user_app/views.py

from django.contrib.auth import authenticate
from .models import AppUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status as s
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from task_proj.utilies import handle_exceptions
from datetime import datetime, timedelta
from .utilities import CookieAuthentication


def create_time_for_cookie(days=0, minutes=0):
    life_time = datetime.now() + timedelta(days=days, minutes=minutes)
    format_time = life_time.strftime("%a, %d %b %Y %H:%M:%S GMT")
    return format_time
```

`CreateUser` now generates a JWT pair instead of a DRF token. Notice that we set two separate cookies — `access` and `refresh` — each with its own expiry matching the `SIMPLE_JWT` settings:

```python
# server/user_app/views.py

class CreateUser(APIView):
    authentication_classes = []
    permission_classes = []

    @handle_exceptions
    def post(self, request):
        data = request.data.copy()
        data['username'] = data.get('email')
        new_user = AppUser.objects.create_user(**data)
        try:
            new_user.full_clean()
            new_user.save()
            # generate a JWT pair for the newly created user
            refresh = RefreshToken.for_user(new_user)
            response = Response({"email": new_user.email}, status=s.HTTP_201_CREATED)
            response.set_cookie(
                key='access',
                value=str(refresh.access_token),
                httponly=True,
                secure=True,
                samesite='Lax',
                expires=create_time_for_cookie(minutes=15)
            )
            response.set_cookie(
                key='refresh',
                value=str(refresh),
                httponly=True,
                secure=True,
                samesite='Lax',
                expires=create_time_for_cookie(days=7)
            )
            return response
        except Exception as e:
            return Response(e.args, status=s.HTTP_400_BAD_REQUEST)
```

`LogIn` follows the same pattern — authenticate the user credentials, generate a fresh JWT pair, and set both cookies:

```python
# server/user_app/views.py

class LogIn(APIView):
    authentication_classes = []
    permission_classes = []

    @handle_exceptions
    def post(self, request):
        data = request.data.copy()
        data['username'] = data.get('email')
        user = authenticate(username=data.get('username'), password=data.get('password'))
        if user:
            refresh = RefreshToken.for_user(user)
            response = Response({"email": user.email}, status=s.HTTP_200_OK)
            response.set_cookie(
                key='access',
                value=str(refresh.access_token),
                httponly=True,
                secure=True,
                samesite='Lax',
                expires=create_time_for_cookie(minutes=15)
            )
            response.set_cookie(
                key='refresh',
                value=str(refresh),
                httponly=True,
                secure=True,
                samesite='Lax',
                expires=create_time_for_cookie(days=7)
            )
            return response
        return Response("No user matching credentials", status=s.HTTP_404_NOT_FOUND)
```

`LogOut` no longer deletes a database token row. Instead it reads the refresh token from the cookie and calls `.blacklist()` on it — that is what the `token_blacklist` app handles. We delete both cookies from the browser regardless of whether the blacklist operation succeeds, so the client is always logged out from its perspective:

```python
# server/user_app/views.py

class LogOut(UserView):

    @handle_exceptions
    def post(self, request):
        user = request.user
        refresh_token = request.COOKIES.get('refresh')
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except TokenError:
                pass  # token already invalid or expired — still log out cleanly
        response = Response(f"{user.email} has been logged out")
        response.delete_cookie('access')
        response.delete_cookie('refresh')
        return response
```

We also need a new `RefreshView`. Its job is simple: read the refresh token from the cookie, validate it, and issue a fresh access token. Because `ROTATE_REFRESH_TOKENS` is enabled, simplejwt also issues a new refresh token and blacklists the old one automatically:

```python
# server/user_app/views.py

class RefreshView(APIView):
    authentication_classes = []
    permission_classes = []

    @handle_exceptions
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh')
        if not refresh_token:
            return Response("Refresh token not present", status=s.HTTP_401_UNAUTHORIZED)
        try:
            refresh = RefreshToken(refresh_token)
            # calling .access_token triggers rotation when ROTATE_REFRESH_TOKENS=True
            new_access = str(refresh.access_token)
            new_refresh = str(refresh)
            response = Response({"message": "Token refreshed successfully"})
            response.set_cookie(
                key='access',
                value=new_access,
                httponly=True,
                secure=True,
                samesite='Lax',
                expires=create_time_for_cookie(minutes=15)
            )
            response.set_cookie(
                key='refresh',
                value=new_refresh,
                httponly=True,
                secure=True,
                samesite='Lax',
                expires=create_time_for_cookie(days=7)
            )
            return response
        except TokenError:
            return Response("Invalid or expired refresh token", status=s.HTTP_401_UNAUTHORIZED)
```

Finally, register the new endpoint in `user_app/urls.py`:

```python
# server/user_app/urls.py

from django.urls import path
from .views import *

urlpatterns = [
    path("", Info.as_view()),
    path("create/", CreateUser.as_view()),
    path("login/", LogIn.as_view()),
    path("logout/", LogOut.as_view()),
    path("refresh/", RefreshView.as_view()),   # new
]
```

---

#### Updating CookieAuthentication Class

Our `CookieAuthentication` class previously extended DRF's `TokenAuthentication` and overrode where to read the token from (the cookie instead of the `Authorization` header). The pattern is identical with simplejwt — we extend `JWTAuthentication` and override the token source.

`JWTAuthentication` exposes two methods we can chain together:

- `get_validated_token(raw_token)` — decodes the raw token string and verifies its signature and expiry, returning a validated token object.
- `get_user(validated_token)` — uses the `user_id` claim inside the token to fetch the `AppUser` instance.

```python
# server/user_app/utilities.py

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework import exceptions


class CookieAuthentication(JWTAuthentication):

    def authenticate(self, request):
        access_token = request.COOKIES.get('access')

        if not access_token:
            raise exceptions.AuthenticationFailed("Authentication cookie is not present")

        try:
            validated_token = self.get_validated_token(access_token)
            return self.get_user(validated_token), validated_token
        except (InvalidToken, TokenError) as e:
            raise exceptions.AuthenticationFailed(str(e))
```

`UserView` — the base class that `Info` and `LogOut` inherit from — already declares `authentication_classes = [CookieAuthentication]`, so no changes are needed there. Swapping the parent class of `CookieAuthentication` is all it takes to upgrade the entire authentication layer.

At this point the full view file looks like this:

```python
# server/user_app/views.py

from django.contrib.auth import authenticate
from .models import AppUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status as s
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from task_proj.utilies import handle_exceptions
from datetime import datetime, timedelta
from .utilities import CookieAuthentication


def create_time_for_cookie(days=0, minutes=0):
    life_time = datetime.now() + timedelta(days=days, minutes=minutes)
    format_time = life_time.strftime("%a, %d %b %Y %H:%M:%S GMT")
    return format_time


class CreateUser(APIView):
    authentication_classes = []
    permission_classes = []

    @handle_exceptions
    def post(self, request):
        data = request.data.copy()
        data['username'] = data.get('email')
        new_user = AppUser.objects.create_user(**data)
        try:
            new_user.full_clean()
            new_user.save()
            refresh = RefreshToken.for_user(new_user)
            response = Response({"email": new_user.email}, status=s.HTTP_201_CREATED)
            response.set_cookie(
                key='access',
                value=str(refresh.access_token),
                httponly=True,
                secure=True,
                samesite='Lax',
                expires=create_time_for_cookie(minutes=15)
            )
            response.set_cookie(
                key='refresh',
                value=str(refresh),
                httponly=True,
                secure=True,
                samesite='Lax',
                expires=create_time_for_cookie(days=7)
            )
            return response
        except Exception as e:
            return Response(e.args, status=s.HTTP_400_BAD_REQUEST)


class LogIn(APIView):
    authentication_classes = []
    permission_classes = []

    @handle_exceptions
    def post(self, request):
        data = request.data.copy()
        data['username'] = data.get('email')
        user = authenticate(username=data.get('username'), password=data.get('password'))
        if user:
            refresh = RefreshToken.for_user(user)
            response = Response({"email": user.email}, status=s.HTTP_200_OK)
            response.set_cookie(
                key='access',
                value=str(refresh.access_token),
                httponly=True,
                secure=True,
                samesite='Lax',
                expires=create_time_for_cookie(minutes=15)
            )
            response.set_cookie(
                key='refresh',
                value=str(refresh),
                httponly=True,
                secure=True,
                samesite='Lax',
                expires=create_time_for_cookie(days=7)
            )
            return response
        return Response("No user matching credentials", status=s.HTTP_404_NOT_FOUND)


class UserView(APIView):
    authentication_classes = [CookieAuthentication]
    permission_classes = [IsAuthenticated]


class Info(UserView):

    @handle_exceptions
    def get(self, request):
        user = request.user
        return Response({"email": user.email})


class LogOut(UserView):

    @handle_exceptions
    def post(self, request):
        user = request.user
        refresh_token = request.COOKIES.get('refresh')
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except TokenError:
                pass
        response = Response(f"{user.email} has been logged out")
        response.delete_cookie('access')
        response.delete_cookie('refresh')
        return response


class RefreshView(APIView):
    authentication_classes = []
    permission_classes = []

    @handle_exceptions
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh')
        if not refresh_token:
            return Response("Refresh token not present", status=s.HTTP_401_UNAUTHORIZED)
        try:
            refresh = RefreshToken(refresh_token)
            new_access = str(refresh.access_token)
            new_refresh = str(refresh)
            response = Response({"message": "Token refreshed successfully"})
            response.set_cookie(
                key='access',
                value=new_access,
                httponly=True,
                secure=True,
                samesite='Lax',
                expires=create_time_for_cookie(minutes=15)
            )
            response.set_cookie(
                key='refresh',
                value=new_refresh,
                httponly=True,
                secure=True,
                samesite='Lax',
                expires=create_time_for_cookie(days=7)
            )
            return response
        except TokenError:
            return Response("Invalid or expired refresh token", status=s.HTTP_401_UNAUTHORIZED)
```

---

## Conclusion

We have fully replaced DRF's stateful token authentication with stateless JWT authentication. Here is a summary of every change made:

| File | Change |
|---|---|
| `requirements.txt` | Added `djangorestframework-simplejwt` |
| `settings.py` | Removed `rest_framework.authtoken`, added `rest_framework_simplejwt` + `token_blacklist`, added `SIMPLE_JWT` config |
| `user_app/utilities.py` | `CookieAuthentication` now extends `JWTAuthentication` |
| `user_app/views.py` | Replaced `Token` with `RefreshToken`, updated all auth views, added `RefreshView` |
| `user_app/urls.py` | Added `refresh/` endpoint |

Every authenticated request now validates without a database hit. The `refresh/` endpoint gives our frontend a way to silently obtain new access tokens when they expire — which is exactly what we will wire up in the next lesson using Axios interceptors.
