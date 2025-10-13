#!/usr/bin/env python3
"""
Railway Log Fetcher
Fetch deployment, build, and application logs from Railway for troubleshooting.
"""

import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Railway API configuration
RAILWAY_API_URL = "https://backboard.railway.com/graphql/v2"
RAILWAY_API_TOKEN = os.getenv("RAILWAY_API_TOKEN")
RAILWAY_PROJECT_ID = os.getenv("RAILWAY_PROJECT_ID")
RAILWAY_ENVIRONMENT_ID = os.getenv("RAILWAY_ENVIRONMENT_ID")
RAILWAY_SERVICE_ID = os.getenv("RAILWAY_SERVICE_ID")


class RailwayAPI:
    """Railway GraphQL API client"""

    def __init__(self, api_token):
        if not api_token:
            raise ValueError("RAILWAY_API_TOKEN not found in environment variables")

        self.api_token = api_token
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }

    def execute_query(self, query, variables=None):
        """Execute a GraphQL query"""
        payload = {"query": query}
        if variables:
            payload["variables"] = variables

        try:
            response = requests.post(
                RAILWAY_API_URL,
                json=payload,
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()

            data = response.json()

            if "errors" in data:
                print(f"GraphQL Errors: {json.dumps(data['errors'], indent=2)}")
                return None

            return data.get("data")

        except requests.exceptions.RequestException as e:
            print(f"API Request Error: {e}")
            return None

    def list_projects(self):
        """List all projects"""
        query = """
        query {
          projects {
            edges {
              node {
                id
                name
                description
              }
            }
          }
        }
        """

        result = self.execute_query(query)
        if result and "projects" in result:
            return result["projects"]["edges"]
        return []

    def list_environments(self, project_id):
        """List environments for a project"""
        query = """
        query getProject($projectId: String!) {
          project(id: $projectId) {
            id
            name
            environments {
              edges {
                node {
                  id
                  name
                }
              }
            }
          }
        }
        """

        result = self.execute_query(query, {"projectId": project_id})
        if result and "project" in result and result["project"]:
            return result["project"]["environments"]["edges"]
        return []

    def list_services(self, project_id):
        """List services for a project"""
        query = """
        query getProject($projectId: String!) {
          project(id: $projectId) {
            id
            name
            services {
              edges {
                node {
                  id
                  name
                }
              }
            }
          }
        }
        """

        result = self.execute_query(query, {"projectId": project_id})
        if result and "project" in result and result["project"]:
            return result["project"]["services"]["edges"]
        return []

    def get_deployments(self, project_id, environment_id, service_id, limit=10):
        """Get recent deployments for a service"""
        query = """
        query getDeployments($projectId: String!, $environmentId: String!, $serviceId: String!, $first: Int) {
          deployments(
            first: $first
            input: {
              projectId: $projectId
              environmentId: $environmentId
              serviceId: $serviceId
            }
          ) {
            edges {
              node {
                id
                status
                createdAt
                staticUrl
              }
            }
          }
        }
        """

        variables = {
            "projectId": project_id,
            "environmentId": environment_id,
            "serviceId": service_id,
            "first": limit
        }

        result = self.execute_query(query, variables)
        if result and "deployments" in result:
            return result["deployments"]["edges"]
        return []

    def get_deployment_logs(self, deployment_id, limit=1000, debug=False):
        """Get logs for a specific deployment - tries multiple query approaches"""

        # Approach 1: Try deploymentLogs query
        print("🔍 Attempt 1: Querying deploymentLogs...")
        query1 = """
        query getDeploymentLogs($deploymentId: String!, $limit: Int) {
          deploymentLogs(deploymentId: $deploymentId, limit: $limit) {
            logs
          }
        }
        """
        variables = {"deploymentId": deployment_id, "limit": limit}

        if debug:
            print(f"Query: {query1}")
            print(f"Variables: {variables}")

        result = self.execute_query(query1, variables)
        if result and "deploymentLogs" in result:
            print("✓ Success with deploymentLogs query")
            return result["deploymentLogs"]["logs"]

        # Approach 2: Try querying deployment node with logs field
        print("🔍 Attempt 2: Querying deployment node with logs field...")
        query2 = """
        query getDeployment($id: String!) {
          deployment(id: $id) {
            id
            logs
          }
        }
        """
        variables = {"id": deployment_id}

        if debug:
            print(f"Query: {query2}")
            print(f"Variables: {variables}")

        result = self.execute_query(query2, variables)
        if result and "deployment" in result and result["deployment"]:
            deployment = result["deployment"]
            if "logs" in deployment:
                print("✓ Success with deployment.logs query")
                return deployment["logs"]

        # Approach 3: Try querying deployment node with buildLogs field
        print("🔍 Attempt 3: Querying deployment node with buildLogs field...")
        query3 = """
        query getDeployment($id: String!) {
          deployment(id: $id) {
            id
            buildLogs
          }
        }
        """

        if debug:
            print(f"Query: {query3}")

        result = self.execute_query(query3, variables)
        if result and "deployment" in result and result["deployment"]:
            deployment = result["deployment"]
            if "buildLogs" in deployment:
                print("✓ Success with deployment.buildLogs query")
                return deployment["buildLogs"]

        # Approach 4: Try node interface query
        print("🔍 Attempt 4: Querying via node interface...")
        query4 = """
        query getNode($id: ID!) {
          node(id: $id) {
            ... on Deployment {
              id
              logs
            }
          }
        }
        """

        if debug:
            print(f"Query: {query4}")

        result = self.execute_query(query4, variables)
        if result and "node" in result and result["node"]:
            node = result["node"]
            if "logs" in node:
                print("✓ Success with node interface query")
                return node["logs"]

        print("❌ All query approaches failed")
        return None


def save_logs_to_file(logs, log_type, output_dir="logs"):
    """Save logs to a timestamped file"""
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{output_dir}/{log_type}_{timestamp}.log"

    with open(filename, "w") as f:
        if isinstance(logs, str):
            f.write(logs)
        elif isinstance(logs, list):
            for log in logs:
                f.write(json.dumps(log) if isinstance(log, dict) else str(log))
                f.write("\n")
        else:
            f.write(json.dumps(logs, indent=2))

    print(f"✓ Logs saved to: {filename}")
    return filename


def main():
    parser = argparse.ArgumentParser(
        description="Fetch logs from Railway for troubleshooting OpenProject"
    )

    parser.add_argument(
        "--list-projects",
        action="store_true",
        help="List all projects"
    )

    parser.add_argument(
        "--list-environments",
        action="store_true",
        help="List environments for a project"
    )

    parser.add_argument(
        "--list-services",
        action="store_true",
        help="List services for a project"
    )

    parser.add_argument(
        "--list-deployments",
        action="store_true",
        help="List recent deployments"
    )

    parser.add_argument(
        "--fetch-deployment-logs",
        metavar="DEPLOYMENT_ID",
        help="Fetch logs for a specific deployment"
    )

    parser.add_argument(
        "--project-id",
        help="Railway project ID (overrides .env)"
    )

    parser.add_argument(
        "--environment-id",
        help="Railway environment ID (overrides .env)"
    )

    parser.add_argument(
        "--service-id",
        help="Railway service ID (overrides .env)"
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Number of items to fetch (default: 10)"
    )

    parser.add_argument(
        "--output-dir",
        default="logs",
        help="Output directory for log files (default: logs)"
    )

    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)"
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode to see full query details"
    )

    args = parser.parse_args()

    # Initialize API client
    try:
        api = RailwayAPI(RAILWAY_API_TOKEN)
    except ValueError as e:
        print(f"Error: {e}")
        print("Please set RAILWAY_API_TOKEN in your .env file")
        sys.exit(1)

    # Use command line args or environment variables
    project_id = args.project_id or RAILWAY_PROJECT_ID
    environment_id = args.environment_id or RAILWAY_ENVIRONMENT_ID
    service_id = args.service_id or RAILWAY_SERVICE_ID

    # List projects
    if args.list_projects:
        print("📋 Fetching projects...")
        projects = api.list_projects()

        if projects:
            print(f"\nFound {len(projects)} project(s):\n")
            for edge in projects:
                project = edge["node"]
                print(f"  ID: {project['id']}")
                print(f"  Name: {project['name']}")
                if project.get('description'):
                    print(f"  Description: {project['description']}")
                print()
        else:
            print("No projects found or error occurred")

        return

    # List environments
    if args.list_environments:
        if not project_id:
            print("Error: --project-id required or set RAILWAY_PROJECT_ID in .env")
            sys.exit(1)

        print(f"📋 Fetching environments for project {project_id}...")
        environments = api.list_environments(project_id)

        if environments:
            print(f"\nFound {len(environments)} environment(s):\n")
            for edge in environments:
                env = edge["node"]
                print(f"  ID: {env['id']}")
                print(f"  Name: {env['name']}")
                print()
        else:
            print("No environments found or error occurred")

        return

    # List services
    if args.list_services:
        if not project_id:
            print("Error: --project-id required or set RAILWAY_PROJECT_ID in .env")
            sys.exit(1)

        print(f"📋 Fetching services for project {project_id}...")
        services = api.list_services(project_id)

        if services:
            print(f"\nFound {len(services)} service(s):\n")
            for edge in services:
                service = edge["node"]
                print(f"  ID: {service['id']}")
                print(f"  Name: {service['name']}")
                print()
        else:
            print("No services found or error occurred")

        return

    # List deployments
    if args.list_deployments:
        if not all([project_id, environment_id, service_id]):
            print("Error: --project-id, --environment-id, and --service-id required")
            print("Or set RAILWAY_PROJECT_ID, RAILWAY_ENVIRONMENT_ID, and RAILWAY_SERVICE_ID in .env")
            sys.exit(1)

        print(f"📋 Fetching deployments...")
        deployments = api.get_deployments(
            project_id, environment_id, service_id, args.limit
        )

        if deployments:
            print(f"\nFound {len(deployments)} deployment(s):\n")
            for edge in deployments:
                deployment = edge["node"]
                print(f"  ID: {deployment['id']}")
                print(f"  Status: {deployment['status']}")
                print(f"  Created: {deployment['createdAt']}")
                if deployment.get('staticUrl'):
                    print(f"  URL: {deployment['staticUrl']}")
                print()
        else:
            print("No deployments found or error occurred")

        return

    # Fetch deployment logs
    if args.fetch_deployment_logs:
        deployment_id = args.fetch_deployment_logs

        print(f"📥 Fetching logs for deployment {deployment_id}...\n")
        logs = api.get_deployment_logs(deployment_id, args.limit, args.debug)

        if logs:
            save_logs_to_file(
                logs,
                f"deployment_{deployment_id[:8]}",
                args.output_dir
            )
        else:
            print("\n" + "="*70)
            print("⚠️  Unable to fetch logs through GraphQL API")
            print("="*70)
            print("\n📝 Alternative Options:\n")
            print("1. Railway Dashboard (Recommended):")
            print(f"   https://railway.app/project/{RAILWAY_PROJECT_ID}")
            print("   → Click OpenProject service → Click deployment → View logs\n")
            print("2. Railway CLI:")
            print("   npm install -g @railway/cli")
            print("   railway login")
            print(f"   railway link {RAILWAY_PROJECT_ID}")
            print("   railway logs\n")
            print("3. GraphiQL Playground:")
            print("   https://railway.com/graphiql")
            print("   → Add Authorization header with your token")
            print("   → Explore schema for correct log query structure\n")
            print("💡 Tip: Use --debug flag to see detailed query attempts")

        return

    # If no action specified, show help
    parser.print_help()


if __name__ == "__main__":
    main()
