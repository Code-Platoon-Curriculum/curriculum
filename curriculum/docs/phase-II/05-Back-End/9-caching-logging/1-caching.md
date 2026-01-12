# Server Side Caching

## Intro

As modern web applications scale, they must serve large volumes of requests while maintaining fast response times and a smooth user experience. Server-side caching is one of the most effective strategies for reducing unnecessary computation and database access by temporarily storing frequently accessed data. In the context of Django and Django REST Framework (DRF), caching allows APIs to respond faster, scale more efficiently, and remain resilient under load—especially when authenticated users repeatedly request similar data.

---

## What is Caching

Caching is the practice of storing the result of an expensive operation (such as a database query, external API call, or complex computation) so that future requests can reuse that stored result instead of recomputing it. Server-side caching occurs on the backend (e.g., in memory, Redis, or Memcached) and is completely transparent to the client. When a request comes in, the server first checks whether a cached response exists. If it does, the server returns that response immediately; if not, it computes the response, stores it in the cache, and then returns it.

---

### Why Caching

Server-side caching primarily solves performance and scalability problems. Without caching, every API request may trigger database queries, serializer work, and permission checks—each adding latency and load. Caching reduces:

- **Response time** by avoiding repeated work
- **Database load** by minimizing duplicate queries
- **Infrastructure cost** by handling more traffic with fewer resources

For authenticated APIs using DRF Token Authentication, caching can dramatically improve performance when users frequently request the same resources (e.g., dashboards, feeds, or profile data).

---

### Real World Relevance

Consider a popular application like Instagram. When a user opens the app, their home feed is populated with recent posts. While the feed is personalized, it does not change every second. Instagram caches portions of the feed server-side so that repeated refreshes within a short window return quickly. This ensures:

- Fast scrolling and reduced loading spinners
- Lower database stress during peak usage
- Consistent UI responsiveness  

If every refresh required rebuilding the feed from scratch, the app would feel sluggish and unreliable at scale.

---

### When to use caching

| Scenario | Use Caching? | Reason |
|--------|--------------|--------|
| Public or semi-static data (e.g., categories, tags) | ✅ Yes | Data changes infrequently |
| Authenticated user profile data | ✅ Yes (short TTL) | Read-heavy and frequently accessed |
| Real-time data (e.g., live chat, stock prices) | ❌ No | Data changes too frequently |
| Highly personalized, one-off queries | ❌ No | Low cache reuse |
| Expensive aggregate queries | ✅ Yes | High cost, low change rate |

---

## Applying it to a Django API View

### Step 1: Configure Caching Backend
Django supports multiple cache backends. Redis is common in production, but in-memory caching works for development.

```python
# settings.py
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-server-cache",
    }
}
```

This configuration enables an in-memory cache accessible within a single Django process. It is suitable for development and learning purposes, but not for horizontally scaled production environments. Lets break it down.

---

#### What BACKEND Really Means

```py
"BACKEND": "django.core.cache.backends.locmem.LocMemCache"
```

This tells Django which cache implementation to use, such as:

- `LocMemCache` → in-memory cache inside the Django process
- `RedisCache` → Redis server
- `MemcachedCache` → Memcached server
- `FileBasedCache` → filesystem

Think of *BACKEND* as the type of storage engine.

---

#### What LOCATION Means

*LOCATION* is backend-specific metadata, not a table or schema.

Django uses LOCATION as a configuration identifier whose meaning changes based on the backend, just like a variable works we are setting a variable for the memory location where  this cache will be stored.

```python
"LOCATION": "unique-server-cache"
```

It names the in-memory cache instance as "unique-server-cache" if we had multiple caches, we would just name them differently.

**🔑 Important With LocMemCache, the cache:**

- Lives only in RAM
- Exists only inside the Django process
- Is wiped when the server restarts
- Is not shared across multiple servers or workers

---

### Step 2: Cache an API View Response

DRF integrates cleanly with Django’s caching utilities.

```python
from django.views.decorators.cache import cache_page # new import
from django.utils.decorators import method_decorator # new import

@method_decorator(cache_page(60 * 5), name='dispatch')# at class level applies to all methods
class Info(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(cache_page(60 * 5)) # at method level applies to the dictated method
    def get(self, request):
        user = request.user
        return Response({
            "username": user.username,
            "email": user.email,
        })
```

**What this does:**

* `cache_page(60 * 5)` caches the entire response for 5 minutes
* Cached responses are returned without re-running the view logic

**Why it’s necessary:**

User profile data is read frequently and changes rarely. Caching avoids repeated database lookups for the same user during short time windows.

> ⚠️ Warning: View-level caching should be used with extreme caution on authenticated endpoints. Without varying the cache by user identity, cached responses may be served to the wrong user.

--- 

### Step 3: Per-User Cache Considerations

When caching authenticated views, ensure cache keys differ per user. Django automatically includes request path and headers, but more advanced scenarios may require manual cache keys using Django’s low-level cache API.

#### Data Leakage From Built In Caching Function

When using Django’s built-in view-level caching (such as `@cache_page`) on authenticated endpoints, responses are cached based primarily on the request URL and request headers—not on the authenticated user’s identity by default. In applications using DRF Token Authentication, many users may access the same endpoint path (for example, `/api/profile/`). If the response contains user-specific data, the cached response for the first user can be mistakenly served to subsequent users who hit the same endpoint within the cache timeout window.  

This is not a memory leak in the traditional sense of unreleased memory, but rather a **data leakage issue** where one user’s data “leaks” into another user’s response. The root cause is that the cache key does not automatically include the user’s identity, so multiple authenticated users collide on the same cache entry.

---

#### Fixing the Problem (Partial)

Django provides mechanisms to make built-in caching safer by varying cache keys based on request-specific information. One common approach is to vary the cache by the `Authorization` header, which is where DRF token authentication stores the user token.

```python
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from django.utils.decorators import method_decorator

@method_decorator(vary_on_headers("Authorization"), name="dispatch")
@method_decorator(cache_page(60 * 5), name="dispatch")
class UserProfileView(APIView):
    ...
```

By varying on the `Authorization` header:

* Each user’s token produces a different cache entry
* Cached responses are no longer shared across users
* View-level caching remains simple and declarative

However, this approach still has limitations:

* Cache keys can grow large if many users access the endpoint
* It is less explicit and harder to reason about in complex systems
* Fine-grained control over invalidation is limited

> ⚠️ While varying on the Authorization header prevents data leakage, it tightly couples cache keys to authentication tokens and can lead to large cache sizes in high-traffic systems.

---

#### Manual Caching Utilities

Manual caching using Django’s low-level cache API provides full control over what is cached and how it is keyed. Instead of caching the entire response, you cache only the **data that is expensive to compute** and explicitly include the user’s identity in the cache key.

```python
from django.core.cache import cache
from posts.models import Post
from followers.models import Follow

def expensive_stats_calculation(user):
    return {
        "post_count": Post.objects.filter(author=user).count(),
        "follower_count": Follow.objects.filter(following=user).count(),
        "following_count": Follow.objects.filter(follower=user).count(),
    }

def get_user_stats(user):
    cache_key = f"user_stats_{user.id}"
    data = cache.get(cache_key)

    if not data:
        data = expensive_stats_calculation(user)
        cache.set(cache_key, data, timeout=300)

    return data


class UserStatsView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        stats = get_user_stats(request.user)
        return Response(stats)
```

This approach:

* Prevents user data collisions by design
* Makes cache behavior explicit and predictable
* Allows selective caching of business logic rather than whole responses
* Scales better for authenticated, personalized APIs

In real-world Django applications, **per-user caching is essential** whenever responses depend on authenticated identity. It ensures correctness, security, and maintainability while still delivering the performance benefits of server-side caching.

---

## Conclusion

Server-side caching is a critical performance optimization for Django and DRF applications, particularly those using token-based authentication. By intelligently caching responses and expensive computations, developers can significantly reduce latency, improve scalability, and deliver a smoother user experience. When applied thoughtfully—especially with respect to data freshness and user-specific content—caching becomes an essential tool in building production-ready APIs.

