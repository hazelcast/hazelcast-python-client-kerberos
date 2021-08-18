# Hazelcast Python Client Kerberos Authentication Support

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
