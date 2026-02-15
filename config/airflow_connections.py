#!/usr/bin/env python3
"""
Airflow Connections Configuration Script

This script centralizes connection configurations for Airflow DAGs.
It supports both:
1. CLI deployment: Run this script directly to create connections
2. Manual setup: Use the connection definitions in Airflow UI (Admin > Connections)

Environment Variables Required:
- MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE, MYSQL_PORT
- MONGODB_URI
- KAFKA_BOOTSTRAP_SERVERS

Usage:
    python config/airflow_connections.py
"""

import os
import sys
from typing import Dict, List


class AirflowConnection:
    """Represents an Airflow connection with all necessary parameters"""
    
    def __init__(self, conn_id: str, conn_type: str, host: str = None, 
                 login: str = None, password: str = None, schema: str = None,
                 port: int = None, extra: str = None):
        self.conn_id = conn_id
        self.conn_type = conn_type
        self.host = host
        self.login = login
        self.password = password
        self.schema = schema
        self.port = port
        self.extra = extra
    
    def to_cli_command(self) -> str:
        """Generate Airflow CLI command to create this connection"""
        cmd_parts = [
            f"airflow connections add '{self.conn_id}'",
            f"--conn-type '{self.conn_type}'"
        ]
        
        if self.host:
            cmd_parts.append(f"--conn-host '{self.host}'")
        if self.login:
            cmd_parts.append(f"--conn-login '{self.login}'")
        if self.password:
            cmd_parts.append(f"--conn-password '{self.password}'")
        if self.schema:
            cmd_parts.append(f"--conn-schema '{self.schema}'")
        if self.port:
            cmd_parts.append(f"--conn-port {self.port}")
        if self.extra:
            cmd_parts.append(f"--conn-extra '{self.extra}'")
        
        return " ".join(cmd_parts)
    
    def to_ui_format(self) -> Dict:
        """Format connection for display/manual entry in Airflow UI"""
        return {
            'Conn Id': self.conn_id,
            'Conn Type': self.conn_type,
            'Host': self.host or '',
            'Schema': self.schema or '',
            'Login': self.login or '',
            'Password': '***' if self.password else '',
            'Port': self.port or '',
            'Extra': self.extra or ''
        }


def get_connections_from_env() -> List[AirflowConnection]:
    """
    Load connection configurations from environment variables.
    No hardcoded credentials - all values come from environment.
    """
    connections = []
    
    # MySQL Connection
    mysql_host = os.getenv('MYSQL_HOST', 'mysql')
    mysql_user = os.getenv('MYSQL_USER', 'user')
    mysql_password = os.getenv('MYSQL_PASSWORD', '')
    mysql_database = os.getenv('MYSQL_DATABASE', 'mydatabase')
    mysql_port = int(os.getenv('MYSQL_PORT', '3306'))
    
    connections.append(AirflowConnection(
        conn_id='mysql_default',
        conn_type='mysql',
        host=mysql_host,
        login=mysql_user,
        password=mysql_password,
        schema=mysql_database,
        port=mysql_port
    ))
    
    # MongoDB Connection
    mongodb_uri = os.getenv('MONGODB_URI', 'mongodb://mongodb:27017/')
    # Parse MongoDB URI to extract components
    # Format: mongodb://[host]:[port]/[database]
    mongodb_host = os.getenv('MONGODB_HOST', 'mongodb')
    mongodb_port = int(os.getenv('MONGODB_PORT', '27017'))
    
    connections.append(AirflowConnection(
        conn_id='mongodb_default',
        conn_type='mongo',
        host=mongodb_host,
        port=mongodb_port,
        extra=f'{{"uri": "{mongodb_uri}"}}'
    ))
    
    # Kafka Connection (stored as generic connection with extra config)
    kafka_bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092')
    
    connections.append(AirflowConnection(
        conn_id='kafka_default',
        conn_type='generic',
        extra=f'{{"bootstrap_servers": "{kafka_bootstrap_servers}"}}'
    ))
    
    return connections


def deploy_connections():
    """Deploy connections using Airflow CLI"""
    print("=" * 80)
    print("Airflow Connections Deployment")
    print("=" * 80)
    print()
    
    connections = get_connections_from_env()
    
    print("Loaded connection configurations from environment variables:")
    print()
    
    for conn in connections:
        print(f"Connection ID: {conn.conn_id}")
        print(f"  Type: {conn.conn_type}")
        if conn.host:
            print(f"  Host: {conn.host}")
        if conn.port:
            print(f"  Port: {conn.port}")
        print()
    
    print("=" * 80)
    print("CLI Commands to Create Connections:")
    print("=" * 80)
    print()
    
    for conn in connections:
        print(f"# {conn.conn_id}")
        print(conn.to_cli_command())
        print()
    
    print("=" * 80)
    print("Attempting to create connections...")
    print("=" * 80)
    print()
    
    try:
        import subprocess
        for conn in connections:
            cmd = conn.to_cli_command()
            print(f"Executing: {conn.conn_id}...")
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"  ✓ Successfully created {conn.conn_id}")
            else:
                print(f"  ✗ Failed to create {conn.conn_id}")
                if result.stderr:
                    print(f"    Error: {result.stderr}")
            print()
    except Exception as e:
        print(f"Error executing CLI commands: {e}")
        print("You may need to run these commands manually.")


def print_ui_instructions():
    """Print instructions for manual connection setup via Airflow UI"""
    print("=" * 80)
    print("Manual Setup via Airflow UI")
    print("=" * 80)
    print()
    print("To set up connections manually in Airflow UI:")
    print("1. Navigate to Admin > Connections")
    print("2. Click the '+' button to add a new connection")
    print("3. Fill in the following details for each connection:")
    print()
    
    connections = get_connections_from_env()
    
    for conn in connections:
        print(f"--- {conn.conn_id} ---")
        ui_format = conn.to_ui_format()
        for key, value in ui_format.items():
            print(f"  {key}: {value}")
        print()


def main():
    """Main entry point for the script"""
    if len(sys.argv) > 1 and sys.argv[1] == '--ui-instructions':
        print_ui_instructions()
    else:
        deploy_connections()
        print()
        print("=" * 80)
        print("Note: You can also view UI instructions by running:")
        print("  python config/airflow_connections.py --ui-instructions")
        print("=" * 80)


if __name__ == '__main__':
    main()
