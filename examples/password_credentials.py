import logging
import time

from hazelcast import HazelcastClient

from hzkerberos import TokenProvider


def customize_logger(name):
    lg = logging.getLogger(name)
    lg.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    lg.addHandler(handler)


customize_logger("hazelcast")
customize_logger("hzkerberos")


def main():
    # Create a token provider which uses a principal and its password.
    token_provider = TokenProvider(principal="jduke@EXAMPLE.COM", password="p1")
    # Create a Hazelcast client which connects to the
    # Hazelcast instance at 127.0.0.1 using the given token provider.
    client = HazelcastClient(cluster_members=["127.0.0.1"], token_provider=token_provider)

    my_map = client.get_map("auth-map").blocking()
    for i in range(10):
        key = "key-%s" % i
        value = "value-%s" % i
        v = my_map.put(key, value)
        print("Put result:", v)
        time.sleep(1)

    client.shutdown()


if __name__ == "__main__":
    main()
