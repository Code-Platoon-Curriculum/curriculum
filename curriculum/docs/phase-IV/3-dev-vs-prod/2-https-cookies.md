# HTTPS and Cookies

## Introduction

In the previous module we locked down our server configuration and eliminated exposed secrets. But there is still one piece of the authentication flow that deserves attention: the token.

Right now, after a user logs in, our API returns the token in the response body. The React frontend receives it, stores it in browser memory or `localStorage`, and manually attaches it as an `Authorization` header on every subsequent request. This works — but it has a significant weakness. Any JavaScript running on the page can read `localStorage`. If an attacker manages to inject a script into your application through an XSS vulnerability, that script can read the token and send it anywhere in the world.

HTTP cookies — specifically **HttpOnly** cookies — solve this problem. The token lives in a cookie that JavaScript cannot touch. The browser manages it, attaches it automatically to every matching request, and it never appears in JavaScript-accessible memory.

---

## Lesson

### What are HTTP Cookies

An HTTP cookie is a small piece of data the server sends to the browser in a response header. The browser stores it and automatically includes it in the header of every future request to the same domain — no manual attachment required.

Cookies are structured as key-value pairs with optional attributes that control their behavior:

| Attribute | Purpose |
|---|---|
| `HttpOnly` | JavaScript cannot read this cookie — it is only accessible by the browser's networking layer |
| `Secure` | The cookie is only sent over HTTPS connections, never over plain HTTP |
| `SameSite` | Controls whether the cookie is sent with cross-site requests — `Lax` allows it for top-level navigations but blocks it for embedded requests |
| `Expires` | When the cookie should be deleted from the browser |

The `HttpOnly` attribute is the critical one for security. A cookie marked `HttpOnly` is invisible to `document.cookie` and all JavaScript APIs. Even if an attacker injects a script into your page, that script cannot read the token.

---

### Auth Tokens vs Auth Cookies

Let's compare how the current token flow and the cookie flow differ:

| | Auth Token (current) | Auth Cookie |
|---|---|---|
| **Where is the token stored?** | `localStorage` or JavaScript memory | Browser cookie storage |
| **Can JavaScript read it?** | Yes | No (`HttpOnly`) |
| **Is it sent automatically?** | No — must be manually attached as a header | Yes — browser attaches it automatically |
| **Vulnerable to XSS?** | Yes — a script can steal the token | No — `HttpOnly` makes it unreachable |
| **Requires HTTPS?** | No | Yes (with `Secure` flag) |

The core tradeoff is control vs. security. Tokens in `localStorage` give you full control — you can read, write, and delete them from JavaScript. But that accessibility is precisely what makes them a target. HttpOnly cookies give that control to the browser instead, and attackers can no longer steal what they cannot read.

---

### How do Cookies Work

Here is the exact sequence when authentication switches to cookies:

1. The user submits their email and password to `/api/v1/users/login/`.
2. Django authenticates the credentials and retrieves or creates a token for the user.
3. Instead of returning the token in the response body, Django calls `response.set_cookie(...)`, which adds a `Set-Cookie` header to the response.
4. The browser reads the `Set-Cookie` header and stores the cookie locally, associating it with the domain.
5. On every subsequent request to the same domain, the browser automatically includes the cookie in a `Cookie` header — with no JavaScript involvement required.
6. Django's authentication middleware reads the cookie, extracts the token value, and uses it to identify the user.

The browser handles steps 4 and 5 entirely. The React frontend no longer needs to know the token exists.

---

### Applying Cookies with Django

#### Updating Server Configurations

Add the following settings to `settings.py`. These settings control how Django's session cookies behave — and they need to align with our new cookie-based authentication strategy:

```python
SESSION_COOKIE_SECURE = eval(os.environ.get('SESSION_COOKIE_SECURE', 'False'))

SESSION_COOKIE_HTTPONLY = eval(os.environ.get('SESSION_COOKIE_HTTPONLY', 'False'))

CSRF_COOKIE_SECURE = eval(os.environ.get('CSRF_COOKIE_SECURE', 'False'))
```

Add the corresponding variables to `.env`:

```
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
CSRF_COOKIE_SECURE=True
```

And to `.env.example`:

```
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
CSRF_COOKIE_SECURE=True
```

`SESSION_COOKIE_SECURE` ensures session cookies are only transmitted over HTTPS — the browser will refuse to send them over plain HTTP. `SESSION_COOKIE_HTTPONLY` makes session cookies inaccessible to JavaScript. `CSRF_COOKIE_SECURE` applies the same HTTPS requirement to Django's CSRF token cookie.

The `eval(...)` call converts the string `'True'` or `'False'` that `os.environ.get()` returns into an actual Python boolean. Environment variables are always strings — `eval` handles the conversion.

The defaults are `'False'` so that local development still works without HTTPS. On the production server, the `.env` file sets them all to `True`.

---

#### Updating Create and Log In User Views

The `LogIn` and `CreateUser` views currently return the token in the response body. We're going to change them to set the token as an HttpOnly cookie instead.

In `user_app/views.py`:

```python
from django.contrib.auth import authenticate
from .models import AppUser
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status as s
from datetime import datetime, timedelta
from task_proj.utils import handle_exceptions


class CreateUser(APIView):
    authentication_classes = []
    permission_classes = []

    @handle_exceptions
    def post(self, request):
        data = request.data.copy()
        data['username'] = data.get('email')
        new_user = AppUser.objects.create_user(**data)
        new_user.full_clean()
        new_user.save()
        token = Token.objects.create(user=new_user)
        life_time = datetime.now() + timedelta(days=7)
        format_life_time = life_time.strftime("%a, %d %b %Y %H:%M:%S GMT")
        response = Response({"email": new_user.email}, status=s.HTTP_201_CREATED)
        response.set_cookie(
            key="token",
            value=token.key,
            httponly=True,
            secure=True,
            samesite="Lax",
            expires=format_life_time
        )
        return response


class LogIn(APIView):
    authentication_classes = []
    permission_classes = []

    @handle_exceptions
    def post(self, request):
        data = request.data.copy()
        data['username'] = data.get('email')
        user = authenticate(username=data.get('username'), password=data.get('password'))
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            life_time = datetime.now() + timedelta(days=7)
            format_life_time = life_time.strftime("%a, %d %b %Y %H:%M:%S GMT")
            response = Response({"email": user.email})
            response.set_cookie(
                key="token",
                value=token.key,
                httponly=True,
                secure=True,
                samesite="Lax",
                expires=format_life_time
            )
            return response
        return Response("No user matching credentials", status=s.HTTP_404_NOT_FOUND)
```

The key change is that the token is no longer in the response body — it is set on the response as a cookie via `response.set_cookie(...)`. The client receives the user's email to confirm the login succeeded, but never sees the raw token value.

Breaking down the `set_cookie` arguments:

| Argument | Value | Why |
|---|---|---|
| `key` | `"token"` | The cookie name — must match what `CookieAuthentication` looks for |
| `value` | `token.key` | The actual DRF auth token |
| `httponly` | `True` | JavaScript cannot read this cookie |
| `secure` | `True` | Only sent over HTTPS |
| `samesite` | `"Lax"` | Sent on same-site requests and top-level cross-site navigations, but blocked on embedded cross-site requests |
| `expires` | 7 days from now | When the browser should delete the cookie |

The expiry is formatted as an RFC 7231 date string because that is the format the `Set-Cookie` header requires.

---

#### Creating our own Authentication Class

`UserView` currently uses DRF's built-in `TokenAuthentication`. That class looks for an `Authorization: Token <key>` header on incoming requests. Now that the token arrives as a cookie instead of a header, `TokenAuthentication` will find nothing and reject every request.

We need to teach Django how to find the token in a cookie. Create a new class in `user_app/views.py` that inherits from `TokenAuthentication` and overrides where it looks for the token:

```python
from rest_framework.authentication import TokenAuthentication

class CookieAuthentication(TokenAuthentication):

    def get_auth_token_from_cookie(self, request):
        return request.COOKIES.get('token')

    def authenticate(self, request):
        auth_token = self.get_auth_token_from_cookie(request)

        if not auth_token:
            return None

        return self.authenticate_credentials(auth_token)
```

`TokenAuthentication` already knows how to validate a token string against the database and return the associated user — that logic lives in `authenticate_credentials`. All we are doing is changing *where* the token string comes from: instead of the `Authorization` header, it comes from `request.COOKIES.get('token')`.

When `authenticate` returns `None`, DRF moves on to the next authentication class in the list. This is important for backward compatibility — we can support both header-based and cookie-based authentication simultaneously.

---

#### Updating UserViews

Update `UserView` to include both authentication classes. DRF will try them in order and use whichever one successfully identifies a user:

```python
class UserView(APIView):
    authentication_classes = [CookieAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
```

`CookieAuthentication` is listed first. If the request has a `token` cookie, it is used. If not — for example, during testing with an API client that sends the `Authorization` header — `TokenAuthentication` handles it. No existing tooling breaks.

Update `LogOut` to also clear the cookie on logout so the browser stops sending it:

```python
class LogOut(UserView):
    @handle_exceptions
    def post(self, request):
        user = request.user
        user.auth_token.delete()
        response = Response(f"{user.email} has been logged out")
        response.delete_cookie("token")
        return response
```

`response.delete_cookie("token")` instructs the browser to remove the cookie immediately by setting its expiry date to the past.

---

### Applying Cookies to React

With the server setting the token as a cookie, the React frontend no longer needs to manage tokens at all. It does not need to store them, read them, or attach them to requests — the browser handles all of that automatically.

Two things need to change on the frontend.

**First**, the Axios instance must include `withCredentials: true`:

```jsx
const api = axios.create({
  baseURL: "https://yourdomain.com/api/v1/",
  withCredentials: true,
});
```

`withCredentials: true` tells Axios to include cookies when making cross-origin requests. Without this flag, the browser strips cookies from requests that cross domain boundaries — even if the cookie exists and the server is ready to read it. This is the browser's default security behavior. Setting `withCredentials` opts into the authenticated cross-origin pattern explicitly.

**Second**, remove all manual token handling. Anywhere the frontend previously:

- Read a token from `localStorage` after login
- Stored a token to `localStorage`
- Attached `Authorization: Token <key>` to request headers
- Deleted the token from `localStorage` on logout

...none of that is needed anymore. The browser handles it. A login request succeeds, the browser stores the cookie, and from that point forward every request from that browser automatically carries the authentication credential.

The login response now returns only `{ email }` — and that is all the frontend needs to update its state and redirect the user.

---

## Conclusion

Switching from `localStorage` token storage to HttpOnly cookies is one of the highest-impact security improvements available to a full-stack application, and the implementation is straightforward once the pieces are understood:

- **HttpOnly cookies** store the authentication token in a part of the browser that JavaScript cannot reach, eliminating the most common token theft vector.
- **The `Secure` flag** ensures the cookie never travels over unencrypted HTTP — which is why HTTPS had to come first.
- **`CookieAuthentication`** bridges DRF's token validation logic with the new cookie-based delivery mechanism without rewriting authentication from scratch.
- **`withCredentials: true`** opts Axios into the browser's cross-origin cookie behavior so the token travels with every request automatically.
- **Session and CSRF cookie settings** in `settings.py` bring Django's own internal cookies in line with the same security posture.

The frontend got simpler: no token storage, no header management, no logout cleanup logic. The server got more secure: the credential is invisible to JavaScript and only transmitted over encrypted connections. Both outcomes are the result of using the browser's built-in cookie infrastructure correctly rather than reinventing it in JavaScript.
