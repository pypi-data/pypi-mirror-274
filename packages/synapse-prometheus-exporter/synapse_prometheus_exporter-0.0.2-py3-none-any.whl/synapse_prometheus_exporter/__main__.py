import yaml
from prometheus_client import start_http_server, Gauge
import psycopg2
import time
import argparse
import pathlib
import shutil
import sys

# Gauge for local users by state (active, disabled)
LOCAL_USERS_STATE = Gauge(
    "synapse_local_users_state", "Number of local users by state", ["state", "host"]
)

# Gauge for local users by type (guest, user, appservice)
LOCAL_USERS_TYPE = Gauge(
    "synapse_local_users_type", "Number of local users by type", ["type", "host"]
)

# Gauge for local users by moderation status (active, shadow_banned, locked
LOCAL_USERS_MODERATION = Gauge(
    "synapse_local_users_moderation",
    "Number of local users by moderation status",
    ["status", "host"],
)

# Gauge for appservice users by appservice ID
LOCAL_USERS_APPSERVICE = Gauge(
    "synapse_local_users_appservice",
    "Number of local users by appservice ID",
    ["appservice_id", "host"],
)

# Gauge for total number of devices, rooms, and events
TOTAL_DEVICES = Gauge(
    "synapse_total_devices", "Total number of devices in the database", ["host"]
)
TOTAL_ROOMS = Gauge(
    "synapse_total_rooms", "Total number of rooms in the database", ["host"]
)
TOTAL_EVENTS = Gauge(
    "synapse_total_events", "Total number of events in the database", ["host"]
)

# Gauge for known remote servers
FEDERATION_DESTINATIONS = Gauge(
    "synapse_federation_destinations",
    "Number of federation destinations known to the server",
    ["host"],
)


def load_config(config_file="config.yaml"):
    with open(config_file, "r") as f:
        return yaml.safe_load(f)


def get_synapse_stats(db_config):
    try:
        print(f"Retrieving data from {db_config['host']}")
        host_identifier = db_config.get("name") or db_config["host"]

        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            dbname=db_config["database"],
            user=db_config["user"],
            password=db_config["password"],
            host=db_config["host"],
            port=db_config["port"],
        )
        cursor = conn.cursor()

        # Get the number of local users by state
        cursor.execute(
            """
            SELECT is_guest, appservice_id, approved, deactivated, shadow_banned, locked FROM users
            """
        )

        local_users = cursor.fetchall()
        local_users_state = {
            "active": sum([1 for user in local_users if user[3] == 0]),
            "disabled": sum([1 for user in local_users if user[3] == 1]),
        }
        local_users_type = {
            "guest": sum([1 for user in local_users if user[0] == 1]),
            "user": sum([1 for user in local_users if user[0] == 0 and not user[1]]),
            "appservice": sum([1 for user in local_users if user[1]]),
        }
        local_users_moderation = {
            "active": sum(
                [1 for user in local_users if user[4] is False and user[5] is False]
            ),
            "shadow_banned": sum([1 for user in local_users if user[4] is True]),
            "locked": sum([1 for user in local_users if user[5] is True]),
        }
        local_users_appservice = {}

        for user in local_users:
            if user[1]:
                local_users_appservice[user[1]] = (
                    local_users_appservice.get(user[1], 0) + 1
                )

        LOCAL_USERS_STATE.labels(state="active", host=host_identifier).set(
            local_users_state["active"]
        )
        LOCAL_USERS_STATE.labels(state="disabled", host=host_identifier).set(
            local_users_state["disabled"]
        )

        LOCAL_USERS_TYPE.labels(type="guest", host=host_identifier).set(
            local_users_type["guest"]
        )
        LOCAL_USERS_TYPE.labels(type="user", host=host_identifier).set(
            local_users_type["user"]
        )
        LOCAL_USERS_TYPE.labels(type="appservice", host=host_identifier).set(
            local_users_type["appservice"]
        )

        LOCAL_USERS_MODERATION.labels(status="active", host=host_identifier).set(
            local_users_moderation["active"]
        )
        LOCAL_USERS_MODERATION.labels(status="shadow_banned", host=host_identifier).set(
            local_users_moderation["shadow_banned"]
        )
        LOCAL_USERS_MODERATION.labels(status="locked", host=host_identifier).set(
            local_users_moderation["locked"]
        )

        for appservice_id, count in local_users_appservice.items():
            LOCAL_USERS_APPSERVICE.labels(
                appservice_id=appservice_id, host=host_identifier
            ).set(count)

        # Get the total number of devices, rooms, and events
        cursor.execute(
            """
            SELECT COUNT(*) FROM devices
            """
        )

        total_devices = cursor.fetchone()[0]
        TOTAL_DEVICES.labels(host=host_identifier).set(total_devices)

        cursor.execute(
            """
            SELECT COUNT(*) FROM rooms
            """
        )

        total_rooms = cursor.fetchone()[0]
        TOTAL_ROOMS.labels(host=host_identifier).set(total_rooms)

        cursor.execute(
            """
            SELECT COUNT(*) FROM events
            """
        )

        total_events = cursor.fetchone()[0]
        TOTAL_EVENTS.labels(host=host_identifier).set(total_events)

        # Get the number of known federation destinations
        cursor.execute(
            """
            SELECT COUNT(*) FROM destinations
            """
        )

        federation_destinations = cursor.fetchone()[0]
        FEDERATION_DESTINATIONS.labels(host=host_identifier).set(
            federation_destinations
        )

        cursor.close()
        conn.close()
        print(f"Data retrieved from {db_config['host']}")
    except Exception as e:
        print(f"Error retrieving data from {db_config['host']}: {e}")


def main():
    parser = argparse.ArgumentParser(description="PostgreSQL connection exporter")
    parser.add_argument(
        "--config", "-c", help="Path to the configuration file", default="config.yaml"
    )
    parser.add_argument(
        "--create", "-C", help="Create a new configuration file", action="store_true"
    )
    parser.add_argument(
        "--port",
        "-p",
        help="Port for the exporter to listen on (default: 8999, or the port specified in the configuration file)",
        type=int,
    )
    parser.add_argument(
        "--host",
        help="Host for the exporter to listen on (default: localhost, or the host specified in the configuration file)",
    )
    args = parser.parse_args()

    if args.create:
        config_file = pathlib.Path(args.config)
        if config_file.exists():
            print("Configuration file already exists.")
            sys.exit(1)

        template = pathlib.Path(__file__).parent / "config.dist.yaml"
        try:
            shutil.copy(template, config_file)
            print(f"Configuration file created at {config_file}")
            sys.exit(0)
        except Exception as e:
            print(f"Error creating configuration file: {e}")
            sys.exit(1)

    config = load_config(args.config)

    if not ("hosts" in config and config["hosts"]):
        print("No database hosts specified in the configuration file.")
        sys.exit(1)

    databases_to_query = []

    for host in config["hosts"]:
        if not all(
            key in host for key in ["user", "password", "host", "port", "database"]
        ):
            print("Database configuration is missing required fields.")
            exit(1)

        db_config = {
            "name": host.get("name"),
            "user": host["user"],
            "password": host["password"],
            "host": host["host"],
            "port": host["port"],
            "database": host["database"],
        }

        databases_to_query.append(db_config)

    if not databases_to_query:
        print("No databases to query.")
        exit(1)

    exporter_port = (
        args.port
        if args.port
        else (
            config["exporter"]["port"]
            if "exporter" in config and "port" in config["exporter"]
            else 8999
        )
    )

    exporter_host = (
        args.host
        if args.host
        else (
            config["exporter"]["host"]
            if "exporter" in config and "host" in config["exporter"]
            else "localhost"
        )
    )

    start_http_server(exporter_port, exporter_host)
    print(f"Prometheus exporter started on {exporter_host}:{exporter_port}")

    while True:
        for db in databases_to_query:
            get_synapse_stats(db)
        time.sleep(15)


if __name__ == "__main__":
    main()
