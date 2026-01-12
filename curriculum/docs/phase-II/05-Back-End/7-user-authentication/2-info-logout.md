# User Authentication (Info & Logout)

### User Info

```python
class Info(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"email": request.user.email})

```

> This class-based view (Info) provides user information. This could essentially be any information about the user we would like to expose. For simplicities sake the only thing that we will be returning will be the users email.

> Exposing user information is very sensitive and should be treated with as many restrictions we can apply. We wouldn't want anyone getting someone else information, so we will implement both `authentication and permission` classes

> The authentication_classes and permission_classes attributes specify that the view requires token authentication (meaning that the request Authorization HEADER holding the users token in the following format `f"Token {token}"`) it then utilizes the token to ensure the user is authenticated and able to access this view.

> This user already has their token otherwise they wouldn't be able to send the request so we will just return the users email without adding anything else.

### User Log Out

> We've talked about different ways a user can get their Token, and how they can utilize their token to validate their permissions before being able to access a view. Now let's talk about how to `logout` our users.

```python
class Log_out(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=HTTP_204_NO_CONTENT)
```

> This class-based view (Log_out) handles the user logout functionality. The authentication_classes and permission_classes attributes specify that the view requires token authentication and that the user must be authenticated to access this view.

> Once the user sends this request, we will delete the authentication token associated with the user who made the request. This will take away their ability to access any views that require authentication and will force them to `login` and get a newly generated token.

> We don't really have to give a user any sort of message at this point so lets send them response with an HTTP 204 No Content status is returned.

### Breaking down imports

> We are utilizing quite a bit of imports here. Lets take a step back and go over what each import is doing for us.

```python
from django.contrib.auth import authenticate
```

> The `authenticate` function is used for user authentication in the login view (Log_in). It takes the username (email) and password as parameters and verifies the credentials against the user model specified in the Django settings. It returns the authenticated user object if the credentials are valid, or None otherwise

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
    HTTP_204_NO_CONTENT,
)
```

> These imports are from Django Rest Framework (DRF) and are used to work with API views, handle responses, and use standard HTTP status codes.

```python
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
```

> These imports are also from DRF and are used for token-based authentication and permissions. The Token model is used to create and manage tokens for users. The TokenAuthentication class is used as an authentication class in the logout (Log_out) and user information (Info) views. The IsAuthenticated class is used as a permission class in the logout and user information views to ensure that only authenticated users can access those views.

## Handling Super Users

> Now that we've created an `AbstractUser` you'll notice you can't log into the Django Admin page to manage your database. This is because Django's default superuser is no longer active for this project. Now we will have to manually handle this by creating a separate view that will specifically trigger the creation of admin users.
> Let's create a view and url path to create a Master_Trainer

```python
    path('master/', Master_Sign_Up.as_view(), name='master')

    class Master_Sign_Up(APIView):

        def post(self, request):
            master_trainer = Trainer.objects.create_user(**request.data)
            master_trainer.is_staff = True
            master_trainer.is_superuser = True
            master_trainer.save()
            token = Token.objects.create(user=trainer)
            return Response(
                {"master_trainer": master_trainer.email, "token": token.key}, status=HTTP_201_CREATED
            )
```

> Finally we could create a master_trainer through postman, register the Trainer model onto the admin site, and log into Django Admin.

## External Resources

- [django auth docs](https://docs.djangoproject.com/en/4.0/topics/auth/default/)
