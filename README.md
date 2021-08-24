# Hazelcast Python Client Kerberos Authentication Support

## Requirements

* Hazelcast Enterprise 4.1 and up,
* Hazelcast Python Client 4.2.1 and up,
* Python 3.5 or better,
* Linux with a recent Kernel (tested on Debian Stretch and Buster),
* Kerberos 5 shared library (`libkrb5-dev` package on Debian/Ubuntu systems),
* C compiler is required to build the python-gssapi dependency. You may opt to use the system provided
  package (`python3-gssapi` on Debian/Ubuntu systems),

## Install

```
pip install -U hazelcast-kerberos hazelcast-python-client
```

## Usage

Enabling Kerberos authentication for Hazelcast involves server and client configuration.

### Client Configuration

On the client side, a Kerberos token provider is created and passed to Hazelcast Python Client. The token provider authenticates to KDC using the given credentials, receives and caches the Kerberos ticket and retrieves a token. The token is passed to the server-side by Hazelcast Python Client for authenticating to the server.

#### Using a Cached Ticket

If a Kerberos ticket was already cached, probably using the `kinit` command, then token provider only needs the principal:

```python
token_provider = hzkerberos.TokenProvider()
```

#### Authentication using a Keytab File

You can use a keytab file for retrieving the Kerberos ticket. In this case, full path of the keytab file must be specififed:

```python
token_provider = hzkerberos.TokenProvider(keytab="/etc/krb5.keytab")
```

### Creating the Hazelcast Python Client

Once the token provider is created, you can pass it to the Hazelcast Python Client constructor. The token provider will be used by the client during authentication to the server.

```python
client = hazelcast.HazelcastClient(token_provider=token_provider)
```

### Server Configuration

Server security configuration (starting with 4.1) is documented in the [Security](https://docs.hazelcast.com/imdg/latest/security/security.html) section of the main Hazelcast documentation. Kerberos authentication is documented in the [Security Reams](https://docs.hazelcast.com/imdg/latest/security/security-realms.html#kerberos-authentication) sub-section.

The Kerberos support in Hazelcast has 2 configuration parts: identity and authentication. The identity part is responsible for retrieving the service ticket from Kerberos KDC (Key Distribution Center). The authentication part verifies the service tickets.

The following XML fragment can be used as an example of a working server configuration. However, it is recommended to read the completed documentation in order to fully understand the security aspects of Kerberos.

```xml
<security enabled="true">
    <member-authentication realm="kerberosRealm"/>
    <client-authentication realm="kerberosRealm"/>
    <realms>
        <realm name="kerberosRealm">
            <authentication>
                <kerberos>
                    <relax-flags-check>true</relax-flags-check>
                    <use-name-without-realm>false</use-name-without-realm>
                    <keytab-file>/common/krb5.keytab</keytab-file>
                    <principal>hz/${ip}@EXAMPLE.COM</principal>
                </kerberos>
            </authentication>
            <identity>
                <kerberos>
                    <realm>EXAMPLE.COM</realm>
                    <keytab-file>/common/krb5.keytab</keytab-file>
                    <principal>hz/${ip}@EXAMPLE.COM</principal>
                </kerberos>
            </identity>
        </realm>
    </realms>
</security>
```

## Notes

1. Only the default cache is supported for storing/loading the Kerberos ticket. The default cache name is resolved using `krb5_cc_default_name` call.

## Running the Tests

**The Docker setup in this setup is strictly for test purposes.**

Running the tests requires Docker Compose.

1. Create an `.env` file with the Hazelcast Enterprise license key in the root of the project:
    ```
    HZ_LICENSEKEY=...
    ```
2. Run docker compose, which creates KDC/KAdmin and two Hazelcast Enterprise containers:
    ```    
    docker-compose up
    ```
3. Build the Docker image for tests, this is required only once:
    ```
    docker build -t hazelcast-python-client-kerberos_app:latest -f app.Dockerfile .
    ```
5. Run the app container to run the tests whenever the code changes:
    ```
    docker run --name hzkerberos_test \
        --env-file .env \
        --network=hazelcast-python-client-kerberos_hz \
        -v `pwd`:/home/hz/app
        -v hazelcast-python-client-kerberos_common:/common \
        hazelcast-python-client-kerberos_app:latest test
    ```

When a container runs, it executes the corresponding default action, e.g., `test` for the app container.
In order to get a shell instead of the default action, you can use the `/bin/bash` command.

### Accessing KDC

When the docker compose setup is running, you can access KDC by accessing its container:
```
docker-compose exec kdc /bin/bash
```

And starting `kadmin.local`:
```
rlwrap kadmin.local
```
