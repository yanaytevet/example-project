# Project Guidelines

## Overview
This is a Django-based backend project that uses asynchronous patterns extensively. The project follows a specific structure and coding conventions that should be followed when making changes.

## Project Structure
- **common**: Contains common utilities, API views, serializers, and other shared components
- **configurations**: Contains configuration-related models and views
- **users**: Contains user-related models, views, serializers, and authentication logic
other apps are more specific.

## Asynchronous Patterns
The project uses asynchronous patterns extensively, with the following conventions:

1. **Asynchronous Method Naming**: Asynchronous versions of Django's ORM methods are prefixed with 'a'. For example:
   - `afirst()` instead of `first()`
   - `aget()` instead of `get()`
   - `asave()` instead of `save()`
   - `adelete()` instead of `delete()`
   - `acount()` instead of `count()`

2. **Async/Await**: All asynchronous methods should be awaited properly. For example:
   ```python
   total = await query_set.acount()
   ```

3. **Sync to Async Conversion**: The project uses `sync_to_async` from `asgiref.sync` to convert synchronous functions to asynchronous ones.

## API Structure
The project follows a structured approach to API development:

1. **Simple API Views**: Base classes for common API operations (create, read, update, delete)
2. **Serializers**: Used to convert model instances to JSON and vice versa
3. **Permissions Checkers**: Used to check if a user has permission to perform an action

## Serializers
Serializers are used to convert model instances to pydantic's schema. They follow a specific pattern:

1. **Output Schema**: Defined as a pydantic Schema with the expected output fields
2. **Serializer Class**: Inherits from `Serializer` and implements `inner_serialize` method

Example:
```python
from ninja import Schema

from blocks.enums.block_types import BlockTypes
from blocks.models import Block
from common.simple_api.serializers.serializer import Serializer


class FullBlockSerializerOutput(Schema):
    id: int
    a: str
    b: int
    c: bool
    block_type: BlockTypes
    another_field: str


class FullBlockSerializer(Serializer):
    def inner_serialize(self, obj: Block) -> FullBlockSerializerOutput:
        return FullBlockSerializerOutput(
            id=obj.id,
            a=obj.a,
            b=obj.b,
            c=obj.c,
            block_type=obj.block_type,
            another_field='another_value'
        )
```

## Pagination
The project uses a custom pagination implementation that follows a specific pattern:

1. **Pagination Query Params**: Defined as a schema with page, page_size, and filters
2. **Pagination Output**: Defined as a schema with total_amount, pages_amount, page, page_size, and data

## WebSockets
The project uses Django Channels for WebSocket support, with the following components:

1. **WebSocket Consumer**: Handles WebSocket connections and messages
2. **WebSocket Events Manager**: Manages WebSocket events and subscriptions

## Testing
The project includes tests for various components. When making changes, ensure that all tests pass.

## Enums
Enums in the project are organized in the app's enum directory. All enum classes must inherit from `BaseEnum`:

```python
from common.base_enum import BaseEnum


class BlockTypes(BaseEnum):
    ROUND = 'round'
    SQUARE = 'square'
    TRIANGLE = 'triangle'
```

The `BaseEnum` class provides utility methods:
1. `choices()`: Returns a list of tuples (value, value) for use in Django model choices
2. `get_list()`: Returns a list of all enum values
3. `get_dict()`: Returns a dictionary mapping enum names to their values

## Models
New models will always sit in the app's model module. Each model should be defined in its own file within the models directory, and it should be imported in the `__init__.py` file of that module.

Example of a model file structure:
```
app_name/
  models/
    __init__.py
    model1.py
    model2.py
```

Example of the `__init__.py` file:
```python
from .model1 import Model1
from .model2 import Model2
```

This pattern allows for easy importing of models from other parts of the application using:
```python
from app_name.models import Model1, Model2
```

## Apps structure
Apps have the following python modules:
1. enums
2. migrations
3. models
4. permissions_checkers
5. serializers
6. tasks
7. tests
8. views

and the following files:
1. admin.py
2. app.py

In addition, for every router in the app, a new router file will be created.

## Simple API Views
The project provides a set of base view classes in the `common/simple_api/views/` directory that simplify the creation of API endpoints. These classes follow a consistent pattern and handle common tasks such as permission checking, serialization, and error handling.

### Core View Classes

1. **CreateItemAPIView**: Simplifies the creation of POST endpoints for creating new objects.
   - Provides a `register_post` method to register the endpoint with the router
   - Handles permission checking, object creation, and serialization
   - Provides hooks for customizing behavior (e.g., `run_before_creation`, `run_after_creation`)
   - Requires a schema to be defined for the input data

2. **ReadItemByIdAPIView**: Simplifies the creation of GET endpoints for retrieving objects by ID.
   - Provides a `register_get_by_id` method to register the endpoint with the router
   - Handles permission checking, object retrieval by ID, and serialization
   - Provides hooks for customizing behavior (e.g., `run_after_get`)

3. **UpdateItemByIdAPIView**: Simplifies the creation of PATCH endpoints for updating objects by ID.
   - Provides a `register_patch_by_id` method to register the endpoint with the router
   - Handles permission checking, object retrieval by ID, updating, and serialization
   - Provides hooks for customizing behavior (e.g., `run_before_update`, `run_after_update`)
   - Requires a schema to be defined for the input data

4. **DeleteItemByIdAPIView**: Simplifies the creation of DELETE endpoints for deleting objects by ID.
   - Provides a `register_delete_by_id` method to register the endpoint with the router
   - Handles permission checking and object deletion by ID

5. **PaginateItemsAPIView**: Simplifies the creation of paginated GET endpoints.
   - Provides a `register_get` method to register the endpoint with the router
   - Handles pagination, filtering, and ordering of querysets
   - Returns a standardized pagination output with metadata (total_amount, pages_amount, etc.)

6. **RunActionOnItemByIdAPIView**: Simplifies the creation of endpoints for running custom actions on objects by ID.
   - Provides a `register_post_by_id` method to register the endpoint with the router
   - Handles permission checking, object retrieval by ID, and action execution
   - Requires a schema to be defined for the input data

### Usage Example

```python
from common.simple_api.views.create_item_api_view import CreateItemAPIView
from common.simple_api.views.read_item_by_id_api_view import ReadItemByIdAPIView
from blocks.models import Block
from blocks.serializers.blocks_serializers.block_serializer import BlockSerializer
from blocks.permissions_checkers.block_permissions_checker import BlockPermissionsChecker

class CreateBlockView(CreateItemAPIView):
    @classmethod
    def get_model_cls(cls):
        return Block

    @classmethod
    def get_serializer(cls):
        return BlockSerializer()

    @classmethod
    async def check_permitted_before_creation(cls, request, data, path):
        await BlockPermissionsChecker.check_can_create(request.user)
```

## Router files
In every router file, we will use the: 
```python
ApiRouterCreator.create_api_and_router
```
function to create an api and a router object. The function takes the app name as a parameter and returns a tuple containing the API and router objects.

Example:
```python
from common.django_utils.api_router_creator import ApiRouterCreator
from app_name.views.some_view import SomeView

api, router = ApiRouterCreator.create_api_and_router('app_name')

# Register views to the router
SomeView.register_get(router, 'path/')
```

We will add simple api views to the router using their respective register functions:
- `register_get(router, path='')`: Register a GET endpoint
- `register_post(router, path='')`: Register a POST endpoint
- `register_get_by_id(router, path='')`: Register a GET endpoint that takes an ID
- `register_patch_by_id(router, path='')`: Register a PATCH endpoint that takes an ID
- `register_delete_by_id(router, path='')`: Register a DELETE endpoint that takes an ID

Each router file should be named according to its purpose, e.g., `blocks_router.py`, `users_router.py`, etc.

The api object created in each router file is then imported and used in the urls.py file to register the routes in the Django application. For example:

```python
from users.auth_router import api as auth_api
from users.users_router import api as users_api
from configurations.configurations_router import api as configurations_api
from blocks.blocks_router import api as blocks_api

urlpatterns = [
    # Other URL patterns...
    path(r'auth/', auth_api.urls),
    path(r'api/users/', users_api.urls),
    path(r'api/configurations/', configurations_api.urls),
    path(r'api/blocks/', blocks_api.urls),
]
```
