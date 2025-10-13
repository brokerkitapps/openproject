# Railway Log Fetcher

Python script to fetch deployment, build, and application logs from Railway for troubleshooting OpenProject.

## Prerequisites

- Python 3.7 or higher
- Railway API token (created from [Railway account settings](https://railway.app/account/tokens))
- Access to the OpenProject Railway project

## Setup

### 1. Install Dependencies

```bash
cd scripts
pip install -r requirements.txt
```

Or using a virtual environment (recommended):

```bash
cd scripts
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment Variables

The `.env` file in the root directory should contain:

```bash
RAILWAY_API_TOKEN=your-api-token-here
RAILWAY_PROJECT_ID=your-project-id
RAILWAY_ENVIRONMENT_ID=your-environment-id
RAILWAY_SERVICE_ID=your-service-id
```

**Note**: The project, environment, and service IDs can be found using the script's list commands (see below).

## Usage

### List Projects

Find your Railway project ID:

```bash
python fetch_logs.py --list-projects
```

Output example:
```
📋 Fetching projects...

Found 2 project(s):

  ID: 8df3b1d6-2317-4400-b267-56c4a42eed06
  Name: openproject
  Description: OpenProject management system

  ID: abc123...
  Name: other-project
```

### List Environments

Find environment IDs for your project:

```bash
python fetch_logs.py --list-environments --project-id YOUR_PROJECT_ID
```

### List Services

Find service IDs in your project:

```bash
python fetch_logs.py --list-services --project-id YOUR_PROJECT_ID
```

Output example:
```
📋 Fetching services for project...

Found 2 service(s):

  ID: 4bd252dc-c4ac-4c2e-a52f-051804292035
  Name: OpenProject

  ID: xyz789...
  Name: postgres
```

### List Recent Deployments

View recent deployments for troubleshooting:

```bash
python fetch_logs.py --list-deployments --project-id YOUR_PROJECT_ID --environment-id YOUR_ENV_ID --service-id YOUR_SERVICE_ID
```

Or if IDs are set in `.env`:

```bash
python fetch_logs.py --list-deployments
```

Output example:
```
📋 Fetching deployments...

Found 5 deployment(s):

  ID: abc123-deployment-id
  Status: SUCCESS
  Created: 2025-01-15T10:30:00Z
  URL: https://openproject-production-6f30.up.railway.app

  ID: def456-deployment-id
  Status: FAILED
  Created: 2025-01-15T09:15:00Z
```

### Fetch Deployment Logs

Fetch logs for a specific deployment:

```bash
python fetch_logs.py --fetch-deployment-logs DEPLOYMENT_ID
```

Options:
- `--limit N` - Number of log lines to fetch (default: 1000)
- `--output-dir DIR` - Output directory for log files (default: logs)
- `--format FORMAT` - Output format: text or json (default: text)

Example:
```bash
python fetch_logs.py --fetch-deployment-logs abc123-deployment-id --limit 5000 --output-dir troubleshooting
```

## Log Types

The script can fetch three types of logs useful for troubleshooting:

### 1. Deployment Logs
- Shows the deployment process
- Indicates if deployment succeeded or failed
- Contains startup errors

**Use for**: Deployment failures, startup issues

### 2. Build Logs
- Shows Docker image build process
- Contains build errors and warnings

**Use for**: Build failures, dependency issues

### 3. Application/Runtime Logs
- Live application logs (stdout/stderr)
- OpenProject errors and warnings
- SMTP connection issues
- Database connection problems
- HTTP request logs

**Use for**: Runtime errors, SMTP issues, database problems

## Common Troubleshooting Scenarios

### Email Not Sending (SMTP Issues)

```bash
# Get recent deployments
python fetch_logs.py --list-deployments

# Fetch logs from the latest deployment
python fetch_logs.py --fetch-deployment-logs LATEST_DEPLOYMENT_ID --limit 2000

# Look for SMTP errors in the saved log file
grep -i smtp logs/deployment_*.log
grep -i "email" logs/deployment_*.log
```

### Application Crashes or Errors

```bash
# Fetch recent deployment logs
python fetch_logs.py --fetch-deployment-logs DEPLOYMENT_ID --limit 5000

# Search for errors
grep -i error logs/deployment_*.log
grep -i exception logs/deployment_*.log
```

### Deployment Failures

```bash
# List recent deployments to find failed ones
python fetch_logs.py --list-deployments --limit 20

# Fetch logs for the failed deployment
python fetch_logs.py --fetch-deployment-logs FAILED_DEPLOYMENT_ID
```

## Tips

1. **Save IDs in .env**: After finding your project/environment/service IDs, save them in `.env` to avoid repeating them in commands

2. **Check Railway Dashboard**: The script complements the Railway dashboard. Use the dashboard's log viewer for real-time logs and the script for historical analysis

3. **GraphiQL Playground**: If log queries fail, verify the correct query structure using Railway's GraphiQL playground:
   https://railway.com/graphiql

4. **Log Retention**: Railway retains logs for a limited time. Fetch and save important logs locally for long-term storage

5. **Rate Limits**: The Railway API has rate limits. If you encounter rate limit errors, wait a few minutes before retrying

## Troubleshooting the Script

### "RAILWAY_API_TOKEN not found"

Ensure the `.env` file exists in the project root (not in scripts/) and contains:
```bash
RAILWAY_API_TOKEN=your-token-here
```

### "No projects/services/deployments found"

- Verify your API token has access to the project
- Check the token hasn't expired
- Ensure you're using the correct project/service/environment IDs

### "GraphQL Errors"

The Railway GraphQL schema may have changed. Use the GraphiQL playground to verify query structures:
1. Go to https://railway.com/graphiql
2. Click "Headers" and add: `{"Authorization": "Bearer YOUR_TOKEN"}`
3. Test queries and adjust the script accordingly

## File Structure

```
openproject/
├── .env                          # Environment variables (not committed)
├── scripts/
│   ├── fetch_logs.py            # Main log fetching script
│   ├── requirements.txt         # Python dependencies
│   └── README.md               # This file
└── logs/                        # Output directory for fetched logs (created automatically)
    ├── deployment_abc123_20250115_103000.log
    └── deployment_def456_20250115_091500.log
```

## Railway API Resources

- **Public API Docs**: https://docs.railway.com/reference/public-api
- **GraphiQL Playground**: https://railway.com/graphiql
- **Log Viewing Guide**: https://docs.railway.com/guides/logs
- **API Token Management**: https://railway.app/account/tokens

## Support

For issues with:
- **This script**: Create an issue in the brokerkitapps/openproject repository
- **Railway API**: Join Railway's Discord at https://discord.gg/railway
- **OpenProject**: See OpenProject documentation in `/openproject/docs/`
