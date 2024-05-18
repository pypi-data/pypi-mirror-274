# Install and run GeoVisio using Docker

The [Docker](https://docs.docker.com/get-docker/) deployment is a really convenient way to have a Geovisio instance running in an easy and fast way. If you prefer to not use Docker, you can see how to [install](./10_Install_Classic.md) then [run](./14_Running_Classic.md) a classic instance.

Available Docker configuration files are :

- [Dockerfile](https://gitlab.com/panoramax/server/api/-/blob/main/Dockerfile) : contains only API. An **external** PostgreSQL database must be provided.
- [docker-compose.yml](https://gitlab.com/panoramax/server/api/-/blob/main/docker-compose.yml) : offers API and database using **Docker Hub** `geovisio/api:develop` image by default, but can also be built using local files.
- [docker-compose-full.yml](https://gitlab.com/panoramax/server/api/-/blob/main/docker/docker-compose-full.yml) : offers a **full fledged** GeoVisio (Website, API, database, Keycloak). Note that this does not include a blurring API. If a blurring API is needed, the [docker-compose-blurring.yml](https://gitlab.com/panoramax/server/api/-/blob/main/docker/docker-compose-blurring.yml) file can be used alongside it with: `docker compose -f docker/docker-compose-full.yml -f docker/docker-compose-blurring.yml up`. Note that for the moment it will use the old GeoVisio blurring service since the newest one, [SGBlur](https://github.com/cquest/sgblur) is not yet dockerized.

A [full example](https://gitlab.com/panoramax/server/api/-/blob/main/docker/full-osm-auth/readme.md) of a geovisio configured with OpenStreetMap OAuth2 is also available.

## Run with Dockerfile

In this setup, only API and a demo website are offered. A database must be available somewhere, see [database setup documentation](./07_Database_setup.md) to set it up, or use one of the Docker compose setup offered below.

You can use the provided **Docker Hub** `geovisio/api:develop` image directly:

```bash
docker run \
	-e DB_URL=<database connection string> \
	-p 5000:5000 \
	--name geovisio \
	-v <path where to persist pictures>:/data/geovisio \
	geovisio/api:develop \
	<command>
```

This will run a container bound on port 5000 and store uploaded images in the provided folder.

You can also build the image from the local source with:

```bash
docker build -t geovisio/api:latest .
```

## Run with Docker Compose

Many variants of the Docker Compose are available. The straightforward solution is to use the [docker-compose.yml](https://gitlab.com/panoramax/server/api/-/blob/main/docker-compose.yml) file, which embeds both database and GeoVisio API, without the hassle of authentication and blurring (you can use [docker-compose-full.yml](https://gitlab.com/panoramax/server/api/-/blob/main/docker/docker-compose-full.yml) for that).

You can run using **Docker Hub** images for a faster set-up with this command:

```bash
docker-compose -f docker-compose.yml up
```

If you want to work with local files instead, add a `--build` option:

```bash
docker-compose -f docker-compose.yml up --build
```

Once all services are running, you can also run other commands for launching various chore tasks:

```bash
docker-compose -f docker-compose.yml run --rm backend <COMMAND TO RUN>
```

Note that if you use complete [docker-compose-full.yml](https://gitlab.com/panoramax/server/api/-/blob/main/docker/docker-compose-full.yml) file, the provided Keycloak configuration **should not be used in production**, it's only for testing.

If you're running Docker using an [Apple M Series CPU (M1/M2/M3)](https://en.wikipedia.org/wiki/Apple_silicon#M_series), you may need to add an extra environment variable before the Docker compose command:

```bash
export DOCKER_DEFAULT_PLATFORM=linux/amd64 docker-compose -f docker-compose.yml up
```

## Available commands

```
api                 Starts web API for production
ssl-api             Starts web API for production with SSL enabled
dev-api             Starts web API for development
db-upgrade          Database migration
cleanup             Cleans database and remove Geovisio derivated files
```

### Start API

Commands `api`, `ssl-api` and `dev-api` allows you to start Geovisio API, either on HTTP, HTTPS or development mode.

### Database migration

As GeoVisio is actively developed, when updating from a previous version, some database migration could be necessary. If so, when starting GeoVisio, an error message will show up and warn about necessary migration. The `db-upgrade` command has to be ran then.

### Clean-up

Eventually, if you want to clear database and delete derivate versions of pictures (it **doesn't** delete original pictures), you can use the `cleanup` command. You can also run some partial cleaning with the same cleanup command and one of the following options:

```bash
<DOCKER COMMAND> cleanup \
    --database \ # Removes entries from database
    --cache \ # Removes picture derivates (tiles, SD and thumbnail)
    --permanent-pictures # Removes permanent (original) pictures
```

### Other commands

Additional commands can be available (as documented in [classic instance running doc](./14_Running_Classic.md)). These commands can also be launched on a Docker instance using the following syntax:

```bash
# Docker container
docker exec \
	<CONTAINER NAME> \
	flask <GEOVISIO COMMAND>

# Docker compose
docker-compose -f <COMPOSE YML FILE> \
	exec \
	backend \
	flask <GEOVISIO COMMAND>
```

## Background worker

For a production grade instance, don't forget to also run some [pictures background workers](./13_Pictures_processing.md).

## Next step

Your server is up and running, you may want to:

- [Work with the HTTP API](./16_Using_API.md)
- [Fine tune your server settings](./11_Server_settings.md).
- [Organize your pictures and sequences](./15_Pictures_requirements.md)
