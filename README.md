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
3. Start the Remote Controller:
    ```
    bash rc.sh start
    ```
4. Activate the venv:
    ```
   source venv/bin/activate
    ```
5. CD to the test directory:
    ```
    cd ~/app
    ```
6. Run tests:
    ```
    make test-all
    ```
