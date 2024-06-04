#### To run backend
```shell
make run-dev
```


### After changing the database schema
Make your changes in the models.py, then run
```shell
alembic revision --autogenerate -m "add sodium to product"
alembic upgrade head
```
