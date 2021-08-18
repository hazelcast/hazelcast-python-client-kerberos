# Hazelcast Python Client Kerberos Authentication Support

## Requirements

* Python 3.5 or better,
* Kerberos 5 shared library (`libkrb5-dev` package on Debian/Ubuntu systems),
* C compiler is required to build the python-gssapi dependency. You may opt to use the system provider
  package (`python3-gssapi` on Debian/Ubuntu systems).

## Install

```
pip install -U hazelcast-kerberos
```

## Usage:

### Hazelcast Setup

Sample configuration:

```xml

<hazelcast xmlns="http://www.hazelcast.com/schema/config"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://www.hazelcast.com/schema/config
            http://www.hazelcast.com/schema/config/hazelcast-config-4.2.xsd"
>
   <security enabled="true">
      <client-permissions>
         <map-permission name="auth-map" principal="*">
            <actions>
               <action>create</action>
               <action>destroy</action>
               <action>put</action>
               <action>read</action>
            </actions>
         </map-permission>
      </client-permissions>
      <member-authentication realm="kerberosRealm"/>
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
                        <property name="principal">PRINCIPAL_HERE</property>
                        <property name="keyTab">KEYTAB_HERE</property>
                     </properties>
                  </login-module>
               </jaas>
            </authentication>
         </realm>
         <realm name="krb5Intitiator">
            <authentication>
               <jaas>
                  <login-module class-name="com.sun.security.auth.module.Krb5LoginModule" usage="REQUIRED">
                     <properties>
                        <property name="isInitiator">true</property>
                        <property name="useTicketCache">false</property>
                        <property name="doNotPrompt">true</property>
                        <property name="useKeyTab">true</property>
                        <property name="storeKey">true</property>
                        <property name="principal">PRINCIPAL_HERE</property>
                        <property name="keyTab">KEYTAB_HERE</property>
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
            <identity>
               <kerberos>
                  <realm>EXAMPLE.COM</realm>
                  <security-realm>krb5Initiator</security-realm>
               </kerberos>
            </identity>
         </realm>
      </realms>
   </security>
</hazelcast>

```

### Creating the Token Provider

#### Initializing Credentials Externally

If Kerberos credentials are initialized externally, all you need to provide is the service principal name:

```python
token_provider = hzkerberos.TokenProvider(spn="hz/172.17.0.2@EXAMPLE.COM")
```

#### Authentication using a Keytab File

```python
token_provider = hzkerberos.TokenProvider(
   spn="hz/172.17.0.2@EXAMPLE.COM",
   keytab="/etc/krb5.keytab"
)
```

#### Authentication using a Password

```python
token_provider = hzkerberos.TokenProvider(
   spn="hz/172.17.0.2@EXAMPLE.COM",
   password="s3cr3t"
)
```

### Creating the Hazelcast Python Client

```python

client = hazelcast.HazelcastClient(token_provider=token_provider)
```

## Running the Tests

1. Build the Docker image:
    ```
    cd docker
    docker build -t hazelcast/pykerb:latest --build-arg HAZELCAST_ENTERPRISE_KEY="..." .
    ```
2. Run the Docker image:
    ```
    docker run -it --rm --name pykerb -v `pwd`/..:/home/hz/app --env HAZELCAST_ENTERPRISE_KEY="..."  hazelcast/pykerb:latest
    ```
