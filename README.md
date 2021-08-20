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

On the client side, a Kerberos token provider is created and passed to Hazelcast Python Client. The token provider
authenticates to KDC using the given credentials, receives and caches the Kerberos ticket and retrieves a token. The
token is passed to the server-side by Hazelcast Python Client for authenticating to the server.

#### Using a Cached Ticket

If a Kerberos ticket was already cached, probably using the `kinit` command, then token provider only needs the
principal:

```python
token_provider = hzkerberos.TokenProvider(principal="hz/172.17.0.2@EXAMPLE.COM")
```

#### Authentication using a Keytab File

You can use a keytab file for retrieving the Kerberos ticket. In this case, full path of the keytab file must be
specififed:

```python
token_provider = hzkerberos.TokenProvider(
    principal="hz/172.17.0.2@EXAMPLE.COM",
    keytab="/etc/krb5.keytab"
)
```

#### Authentication using a Password

It is possible to use a password instead of a keytab file if the pricipal was created with a password:

```python
token_provider = hzkerberos.TokenProvider(
    principal="hz/172.17.0.2@EXAMPLE.COM",
    password="s3cr3t"
)
```

### Creating the Hazelcast Python Client

Once the token provider is created, you can pass it to the Hazelcast Python Client constructor. The token provider will
be used by the client during authentication to the server.

```python
client = hazelcast.HazelcastClient(token_provider=token_provider)
```

### Server Configuration

Server security configuration (starting with 4.1) is documented in
the [Security](https://docs.hazelcast.com/imdg/latest/security/security.html) section of the main Hazelcast
documentation. Kerberos authentication is documented in
the [Security Reams](https://docs.hazelcast.com/imdg/latest/security/security-realms.html#kerberos-authentication)
sub-section.

The Kerberos support in Hazelcast has 2 configuration parts: identity and authentication. The identity part is
responsible for retrieving the service ticket from Kerberos KDC (Key Distribution Center). The authentication part
verifies the service tickets.

The following XML fragment can be used as an example of a working server configuration. However, it is recommended to
read the completed documentation in order to fully understand the security aspects of Kerberos.

```xml

<security enabled="true">
    <client-authentication realm="kerberosRealm"/>
    <realms>
        <realm name="krb5Acceptor">
            <authentication>
                <jaas>
                    <login-module class-name="com.sun.security.auth.module.Krb5LoginModule" usage="REQUIRED">
                        <properties>
                            <property name="isInitiator">false</property>
                            <property name="useTicketCache">false</property>
                            <property name="doNotPrompt">true</property>
                            <property name="useKeyTab">true</property>
                            <property name="storeKey">true</property>
                            <property name="principal">{principal}</property>
                            <property name="keyTab">{keytab}</property>
                        </properties>
                    </login-module>
                </jaas>
            </authentication>
        </realm>
        <realm name="kerberosRealm">
            <authentication>
                <kerberos>
                    <relax-flags-check>true</relax-flags-check>
                    <use-name-without-realm>false</use-name-without-realm>
                    <security-realm>krb5Acceptor</security-realm>
                </kerberos>
            </authentication>
        </realm>
    </realms>
</security>            
```

## Running the Tests

Running the tests requires Docker.

1. Build the Docker image, this is required only once:
    ```
    cd docker
    docker build -t hazelcast/pykerberos:latest \
       --build-arg HAZELCAST_ENTERPRISE_KEY="..." .
    ```
2. Run the container to run the tests whenever the code changes:
    ```
    docker run -it --rm --name pykerberos \
       -v `pwd`/..:/home/hz/app \
       --env HAZELCAST_ENTERPRISE_KEY="..." \
       hazelcast/pykerberos:latest
    ```
