# FastAPI ODM Helper

FastAPI ODM Helper helps us to work with beanie easier with lots of useful functions

## How to use

1. BaseRepository

```python
from fastapi_odm_helper import BaseRepository
from users.entities.user import UserEntity

class UserRepository(BaseRepository[UserEntity]):
    _entity = UserEntity
```

2. @Entity decorator

```python
from fastapi_odm_helper import Entity

@Entity()
class UserEntity(BaseEntity):
    id: UUID


```
