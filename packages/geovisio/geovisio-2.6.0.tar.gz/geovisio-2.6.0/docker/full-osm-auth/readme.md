# A complete GeoVisio deployment with OpenStreetMap authentication

Here is a simple example on how to host a GeoVisio instance based on a simple docker compose, and using OSM OAuth2 so the users only need an OSM account to be able to upload pictures.

Note that, for a production grade deployment, you might need to adapt some things:

- Tune PostgreSQL configuration to suit your needs, and at the very least backup it 💾.
- Think about the storage of the pictures, see what disks you'll need, you'll likely need a lot of storage. And as the very least backup them 💾.
- Maybe split the services between several hosts (pictures workers separate from HTTP API).
- Add cache in Nginx to speed up some responses.
- ...

Some documentation on how to fine tune GeoVisio's API is available [here](https://gitlab.com/panoramax/server/api/-/blob/develop/docs/11_Server_settings.md).

As a requirement for this example, you'll need a Linux server (this should also work with other OS, but not tested here), with [docker](https://www.docker.com/) and [docker compose](https://docs.docker.com/compose/) installed.
Note: If you have the legacy `docker-compose` installed, you might need to replace the `docker compose` commands with `docker-compose`. Also note that, depending on you docker installation, you might need `sudo` rights to run docker commands.

Having nice `https` urls is mandatory to use the OAuth2 on OpenStreetMap, you'll also need a domain, and in this tutorial, I'll use [caddy](https://caddyserver.com) as a reverse proxy to handle https because that's what I have, but setting up [nginx](https://www.nginx.com/) should also be quite easy.

## Creating our OSM OAuth2 client

First, we'll configure our OSM OAuth2 client.

You can follow [the documentation](https://wiki.openstreetmap.org/wiki/OAuth) for this, here is a simple walkthrough.

Go to "My settings" > "OAuth 2 applications"

And register a new client, giving it a nice name, a redirect uri with `https://{your_domain}/api/auth/redirect` (like `https://your.panoramax.org/api/auth/redirect`) and the permission "Read user preferences".
![OSM OAuth2 client configration](osm_oauth_client.png).

Make sure to save the client ID/secret given when registering the client, you'll need both of them in the configuration of the next section.

## Running docker compose

### Configuration

Some key variables can be changed by providing a `.env` file or environment variables to docker compose. Feel free to also adapt the docker-compose.yml file if more changes are needed.

The easiest way is to copy the `env.example` file:

```bash
cp env.example .env
```

And change all the required configuration in the file.

At least you'll need to fill:

- The OSM OAuth2 client ID and secret.
- The domain name you plan to expose the service on (the same you used in the redirect of the OAuth2 client).
- A secret key to sign the cookies.

Following the [Flask documentation](https://flask.palletsprojects.com/en/3.0.x/config/#SECRET_KEY), you can generate the secret key with:

```bash
python -c 'import secrets; print(secrets.token_hex())'
```

### Running the docker compose

We'll run the docker compose in detached mode, giving it a nice name (it will use our `.env` by default).

```bash
docker compose --project-name geovisio-osm up -d
```

You can check the services state with the command:

```bash
docker compose -p geovisio-osm ps
```

And the logs with

```bash
docker compose -p geovisio-osm logs -f
```

You can check that the API is working by querying on the host:

```bash
curl --fail http://localhost:8080/api
```

Note that everything will not be working using http://localhost:8080, as we set some configuration telling the API it will be served on a custom domain.

## Domain configuration

You need to set up your domain and must use https as it is mandatory for OAuth2. There are many ways to do this, maybe the easiest way for this is to use a reverse proxy, and let it handle TLS for you.

You can use [nginx](https://www.nginx.com/) + [letsencrypt](https://letsencrypt.org/fr/) (maybe using [certbot](https://certbot.eff.org/)), [caddy](https://caddyserver.com) or anything you want.

### Caddy

Here is a simple Caddy configuration for this:

```
my.domain.org {
    reverse_proxy :8080
}
```

## Updating the instance

If at one point you want to update your GeoVisio version (and you should, we try to add nice functionalities ofter!), you can run:

```bash
docker compose -p geovisio-osm up --pull=always -d
```

## Using GeoVisio

After all this, you should be able to go to your custom domain 🌐, log in using your osm account 🔎, upload some pictures 📸 and enjoy GeoVisio 🎉

If everything does not work as intended, feel free to open an [issue on the gitlab repository](https://gitlab.com/panoramax/server/api/-/issues), contact us in the [Matrix room](https://matrix.to/#/#panoramax-general:matrix.org) or on [community.openstreetmap.org, with the panoramax tag](https://community.openstreetmap.org/tag/panoramax).
