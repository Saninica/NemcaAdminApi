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

-- page content body rich text editor olmali.
-- duyurular kısmı olmalı popup olarak ekranda çıkacak
-- website eklenebilir olmalı ve bu sitenin tema ayarlarıda admin panelden yönetilmeli.
-- siteye ait görseller admin panelde eklenebilir olmalı. Gruplanabilir gibi.