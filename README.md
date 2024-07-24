# DevOpsFetch

## Description
DevOpsFetch is a tool for DevOps that collects and displays system information including active ports, user logins, Nginx configurations, Docker images, and container statuses. It can also continuously monitor and log these activities.

## Installation

Run the provided installation script to install dependencies and set up the systemd service:

```sh
./install_devopsfetch.sh
```

## Usage

```sh
devopsfetch [OPTIONS]
```

#### #Options

- -p, --port [PORT_NUMBER]: Display information about a specific port.
- -d, --docker [CONTAINER_NAME]: List all Docker images and containers or provide detailed information about a specific container.
- -n, --nginx [DOMAIN]: Display Nginx configurations or provide detailed configuration information for a specific domain.
- -u, --users [USERNAME]: List all users and their last login times or provide detailed information about a specific user.
- -t, --time [START_TIME] [END_TIME]: Display activities within a specified time range.
- -h, --help: Show this help message and exit.

### Logs

- Logs are stored in /var/log/devopsfetch.log and rotated regularly. Error logs are stored in /var/log/devopsfetch_error.log.