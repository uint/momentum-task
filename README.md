# Recruitment task for Momentum
## Running the server
### Local

Install the requirements and run `fastapi`!

```
pip install -r requirements.txt
fastapi dev main.py --port 80
```

By default the server is run with in-memory storage. If you want to connect to a PostgreSQL database, set the following env variables:

```
POSTGRES_HOST
POSTGRES_DB
POSTGRES_USER
POSTGRES_PASS
```

### Docker Compose
This should get you going, complete with a PostgreSQL database and a persistent volume:

```
docker compose up --build
```

## Usage

Once you have the thing running, you can go to `http://localhost/docs` and play around with the API there.

## Running tests

Install pytest, and then simply run:

```
pytest
```

## TODOs
### Error handling
Right now, if the client does something like add a book with an existing ID, the server responds with `500 Internal Server Error`. We should really respond with something more informative!

### Integration tests
The only tests right now are unit tests. There are unit tests for the `SqlStore` against SQLite, and there are unit tests for the FastAPI server (with an in memory store that **should** be thread safe).

In production, this would ideally include integration tests that