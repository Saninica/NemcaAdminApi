## Starting The Server:

- uvicorn src.main:app --reload

## Alembic
Firstyl run below command:

`alembic init alembic/`


Run initial migrations:

`alembic revision --autogenerate -m "initial migration"`

### Autogenerate Migrations: 
To autogenerate migrations based on your models, you should run:

`alembic upgrade head` # To apply existing migrations

`alembic revision --autogenerate -m "Your migration message"`

`alembic upgrade head` # To apply the new migration