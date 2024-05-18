# Synapse Exporter for Prometheus

This is an exporter for Prometheus that collects metrics from a Synapse PostgreSQL database. SQLite is not supported.

It is designed to be used with the Synapse Matrix server and provides some additional metrics that are not exported by the internal Prometheus exporter.

## Metrics

The exporter currently provides the following metrics:

- `synapse_local_users_state`: Number of local users by state (active, disabled)
- `synapse_local_users_type`: Number of local users by type (guest, user, appservice)
- `synapse_local_users_moderation`: Number of local users by moderation status (active, shadow_banned, locked)
- `synapse_local_users_appservice`: Number of local users by appservice ID
- `synapse_total_devices`: Total number of devices
- `synapse_total_rooms`: Total number of rooms
- `synapse_total_events`: Total number of events
- `synapse_federation_destinations`: Number of federation destinations (i.e. federated servers)

## Installation

You can install the exporter from PyPI. Within a virtual environment, run:

```bash
pip install synapse-prometheus-exporter
```

## Configuration

The exporter is configured using a `config.yaml`. You can create a default configuration file in the current working directory with:

```bash
synapse-prometheus-exporter --create-config
```

Now, edit the `config.yaml` file to match your PostgreSQL connection settings. Here is an example configuration:

```yaml
hosts:
  - host: localhost
    port: 5432
    user: postgres
    password: postgres
    database: synapse
```

## Usage

After you have created your `config.yaml`, you can start the exporter with:

```bash
synapse-prometheus-exporter
```

By default, the exporter listens on `localhost:8999`. You can change the address in the `config.yaml` file, or using the `--host` and `--port` flags:

```bash
synapse-prometheus-exporter --host 0.0.0.0 --port 9899
```

You can also specify a different configuration file with the `--config` flag:

```bash
synapse-prometheus-exporter --config /path/to/config.yaml
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.