# Book Review

## Running project in development

1. Create a .env file in root dir

```
touch .env
```

.env dev variables:

```
DEBUG=True
ALLOWED_HOSTS=localhost 127.0.0.1
CSRF_TRUSTED_ORIGINS=http://localhost.com/ https://localhost.com
SECRET_KEY=123changethis123secret
POSTGRES_HOST=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=postgres
TZ=America/Sao_Paulo
PGTZ=America/Sao_Paulo
REDIS_URL=redis://redis:6379
BROKER_URL=amqp://admin:admin@broker:5672
RABBITMQ_DEFAULT_USER=admin
RABBITMQ_DEFAULT_PASS=admin
```

2. Run the project with docker compose v2

```sh
docker compose build
docker compose up -d
```

## /admin default credentials and docs

Those are the default for development only and should be removed in production!

Once containers are running in dev access the admin login page at http://localhost/admin

| Email | Password |
| ------ | ------ |
| admin@admin.com | admin |


After login with the default admin credentials go to https://locahost/api/docs to interact with swagger generated docs.

Use `/api/auth/token/` to generate new JWT token pairs, copy the access token and use it to authenticate on swagger docs.
