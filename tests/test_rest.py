import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app.exchange.clients.delta_rest_client import DeltaRestClient


def main():

    client = DeltaRestClient()

    print()

    print("=" * 60)

    print("DELTA REST TEST")

    print("=" * 60)

    print()

    connected = client.health_check()

    print()

    print("Connected :", connected)

    print()

    client.close()


if __name__ == "__main__":

    main()