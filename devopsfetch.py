import argparse
import subprocess
import psutil
import pwd
import docker
from prettytable import PrettyTable
from datetime import datetime, timedelta

def get_active_ports():
    result = []
    for conn in psutil.net_connections(kind='inet'):
        laddr = f"{conn.laddr.ip}:{conn.laddr.port}"
        if conn.raddr:
            raddr = f"{conn.raddr.ip}:{conn.raddr.port}"
        else:
            raddr = "-"
        result.append([laddr, raddr, conn.status, conn.pid])
    return result

def get_docker_info():
    client = docker.from_env()
    images = client.images.list()
    containers = client.containers.list(all=True)
    return images, containers

def get_nginx_info():
    output = subprocess.check_output(['nginx', '-T']).decode('utf-8')
    return output

def get_users_info():
    users = []
    for user in pwd.getpwall():
        last_login = "-"
        try:
            last_login = subprocess.check_output(['lastlog', '-u', user.pw_name]).decode('utf-8').strip().split('\n')[-1]
        except:
            pass
        users.append([user.pw_name, user.pw_uid, user.pw_gid, user.pw_dir, last_login])
    return users

def display_ports():
    table = PrettyTable(['Local Address', 'Remote Address', 'Status', 'PID'])
    for row in get_active_ports():
        table.add_row(row)
    print(table)

def display_port_detail(port_number):
    table = PrettyTable(['Local Address', 'Remote Address', 'Status', 'PID'])
    for conn in psutil.net_connections(kind='inet'):
        if conn.laddr.port == port_number:
            laddr = f"{conn.laddr.ip}:{conn.laddr.port}"
            raddr = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "-"
            table.add_row([laddr, raddr, conn.status, conn.pid])
    print(table)

def display_docker():
    table_images = PrettyTable(['Image ID', 'Tags'])
    table_containers = PrettyTable(['Container ID', 'Name', 'Status'])
    images, containers = get_docker_info()
    for image in images:
        table_images.add_row([image.id, ', '.join(image.tags)])
    for container in containers:
        table_containers.add_row([container.id, container.name, container.status])
    print("Docker Images:")
    print(table_images)
    print("Docker Containers:")
    print(table_containers)

def display_docker_container(container_name):
    client = docker.from_env()
    try:
        container = client.containers.get(container_name)
        print(container.attrs)
    except docker.errors.NotFound:
        print(f"Container {container_name} not found")

def display_nginx():
    print(get_nginx_info())

def display_nginx_domain(domain):
    output = subprocess.check_output(['nginx', '-T']).decode('utf-8')
    domain_conf = [line for line in output.split('\n') if domain in line]
    for line in domain_conf:
        print(line)

def display_users():
    table = PrettyTable(['Username', 'UID', 'GID', 'Home Directory', 'Last Login'])
    for row in get_users_info():
        table.add_row(row)
    print(table)

def display_user(username):
    table = PrettyTable(['Username', 'UID', 'GID', 'Home Directory', 'Last Login'])
    for user in pwd.getpwall():
        if user.pw_name == username:
            last_login = "-"
            try:
                last_login = subprocess.check_output(['lastlog', '-u', username]).decode('utf-8').strip().split('\n')[-1]
            except:
                pass
            table.add_row([user.pw_name, user.pw_uid, user.pw_gid, user.pw_dir, last_login])
    print(table)

def display_time_range(start_time, end_time):
    start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
    logs = []
    # This assumes that logs are stored in a file named /var/log/devopsfetch.log
    with open('/var/log/devopsfetch.log', 'r') as log_file:
        for line in log_file:
            log_time = datetime.strptime(line.split(' - ')[0], '%Y-%m-%d %H:%M:%S')
            if start_time <= log_time <= end_time:
                logs.append(line)
    for log in logs:
        print(log)

def main():
    parser = argparse.ArgumentParser(description='DevOps system information fetch tool.')
    parser.add_argument('-p', '--port', type=int, help='Display information about a specific port')
    parser.add_argument('-d', '--docker', nargs='?', const=True, help='List all Docker images and containers or provide detailed information about a specific container')
    parser.add_argument('-n', '--nginx', nargs='?', const=True, help='Display Nginx configurations or provide detailed configuration information for a specific domain')
    parser.add_argument('-u', '--users', nargs='?', const=True, help='List all users and their last login times or provide detailed information about a specific user')
    parser.add_argument('-t', '--time', nargs=2, metavar=('start_time', 'end_time'), help='Display activities within a specified time range')
    args = parser.parse_args()

    if args.port:
        display_port_detail(args.port)
    elif args.docker:
        if isinstance(args.docker, str):
            display_docker_container(args.docker)
        else:
            display_docker()
    elif args.nginx:
        if isinstance(args.nginx, str):
            display_nginx_domain(args.nginx)
        else:
            display_nginx()
    elif args.users:
        if isinstance(args.users, str):
            display_user(args.users)
        else:
            display_users()
    elif args.time:
        display_time_range(args.time[0], args.time[1])
    else:
        display_ports()

if __name__ == '__main__':
    main()
