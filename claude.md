# OpenProject Management

This repository is a management wrapper for the OpenProject application.

## Getting Started

Clone this repository with submodules to get the full OpenProject source code:

```bash
git clone --recurse-submodules https://github.com/brokerkitapps/openproject.git
```

Or if you've already cloned without submodules:

```bash
git clone https://github.com/brokerkitapps/openproject.git
cd openproject
git submodule init
git submodule update
```

## Structure

- `openproject/` - The OpenProject repository (tracked as a git submodule)
- `claude.md` - This documentation file
- Root level contains management scripts and documentation

## OpenProject Repository

The OpenProject source code is tracked as a git submodule from: https://github.com/opf/openproject

This approach keeps the management repository lightweight while providing access to the full OpenProject codebase for analysis and development.

## Management

This wrapper repository allows you to manage and customize the OpenProject installation while keeping the original source separate.

## Railway Deployment

This OpenProject instance is deployed on Railway using the official template:
- **Template URL**: https://railway.com/deploy/_Ozucr
- **OpenProject Version**: 14.4.2
- **Custom Domain**: projects.brokerkit.app
- **Port Configuration**: TCP port 80 (OpenProject Docker image default)

The deployment includes:
- PostgreSQL database service
- OpenProject application (openproject/openproject:14.4.2)
- Environment variables configured for HTTPS and database connection

## Database Backups

Railway native backups are enabled for the PostgreSQL database to ensure data protection and recovery capabilities.

### Backup Configuration
- **Schedule**: Daily backups (every 24 hours)
- **Retention**: 6 days
- **Volume**: postgres-volume (`/var/lib/postgresql/data`)
- **Type**: Incremental, copy-on-write backups
- **Cost**: Charged only for incremental backup data (per GB/minute)

### Accessing Backups
1. Navigate to the Railway project dashboard: https://railway.app/project/6ef0f0c6-a251-449e-ba97-2b9a14c17e2c
2. Select the **postgres** service
3. Go to the **Volumes** tab
4. Click on **postgres-volume**
5. View backup history and restore options in the **Backups** section

### Restoring from Backup
To restore a backup:
1. Locate the desired backup by date stamp
2. Click the **Restore** button
3. Review the staged changes
4. A new volume will be mounted with the backup data
5. The original volume is preserved but unmounted

**Note**: Backups can only be restored within the same project and environment. Wiping a volume will delete all associated backups.

## Railway CLI

The Railway CLI is used for infrastructure troubleshooting and log review. It provides direct access to your Railway deployment for monitoring and debugging.

**Best Practice**: Use Railway CLI for all Railway operations when possible (instead of the UI) to automate changes, ensure consistency, and enable scripting.

### Authentication

Authenticate with your Railway API token:

```bash
# Set your Railway API token (get from https://railway.app/account/tokens)
export RAILWAY_TOKEN=your_api_token_here
railway whoami  # Verify authentication
```

### Linking to Project

```bash
# Link to your specific project (one-time setup in the directory)
railway link --project 6ef0f0c6-a251-449e-ba97-2b9a14c17e2c

# Verify you're linked to the correct project
railway list  # Shows services in the project
```

### Common Commands

**View application logs:**
```bash
# Stream real-time logs from openproject service
railway logs --service openproject

# Fetch last 50 lines of logs
railway logs --service openproject --lines 50

# View logs from specific deployment
railway logs DEPLOYMENT_ID
```

**View deployment/build logs:**
```bash
# Show build logs
railway logs --build

# Show deployment logs
railway logs --deployment
```

**Check service status and details:**
```bash
railway status
railway service  # List all services
railway service --help  # Service management
```

**Manage environment variables:**
```bash
# View all variables for current service
railway variables

# Set a variable
railway variables set ATTACHMENTS_STORAGE fog

# View specific variable
railway variables get FOG
```

**View logs with filtering:**
```bash
# Search for specific errors in logs
railway logs --service openproject --lines 100 | grep -i error

# View JSON formatted logs
railway logs --service openproject --json | head -20
```

### Troubleshooting Workflow

**Step 1: Check if service is running**
```bash
railway status
```

**Step 2: View recent logs for errors**
```bash
railway logs --service openproject --lines 100
```

**Step 3: Check environment variables are loaded**
```bash
railway variables  # Verify ATTACHMENTS_STORAGE and FOG are set
```

**Step 4: View build/deployment logs if app won't start**
```bash
railway logs --deployment --lines 50
railway logs --build --lines 50
```

**Step 5: Check specific service**
```bash
railway service --status  # Check postgres, openproject services
```

### Common Issues & CLI Commands

**App not responding - Check logs:**
```bash
railway logs --service openproject --lines 200 | grep -i "error\|fail\|exception"
```

**Environment variables not loading:**
```bash
railway variables  # List all set variables
railway variables get ATTACHMENTS_STORAGE
railway variables get FOG
```

**Check database connection:**
```bash
railway service postgres  # Switch to postgres service
railway logs --service postgres --lines 50
```

**Redeploy after variable changes:**
```bash
railway deploy --service openproject
```

### Best Practices

- **Use CLI over UI**: Automate operations, reduce errors, enable scripting
- **Set RAILWAY_TOKEN**: Store in `.env` or shell profile for convenience
- **Link projects**: Use `railway link` in project directories
- **Monitor logs regularly**: Use `railway logs` to catch issues early
- **Document changes**: Reference CLI commands in commit messages for reproducibility
- **Test before pushing**: Use CLI to verify changes before remote deployment

## Documentation Standards

To keep the repository clean and organized:

### GitHub Issues for Project Tracking
- Use **GitHub Issues** to track project tasks, features, and implementations
- Update issues with "What's Completed" and "What's Next" sections
- Use issue comments for ongoing updates during implementation
- Reference related issues in commit messages with `Relates to #<issue-number>`

### Repository Documentation
- Keep repository docs minimal and focused on architecture/setup decisions
- Avoid duplicating project tracking information in separate doc files
- Example: R2 integration status tracked in Issue #3 instead of separate docs
- Document significant decisions and configurations that affect the repo structure

### Configuration Files
- Use `.env.local` for local secrets (gitignored)
- Use environment variables in production (Railway Variables)
- Never commit credentials, keys, or sensitive data
- Document the format of environment variables in code comments

### When to Document in Repository
- Architecture decisions and design patterns
- Setup instructions that are unlikely to change frequently
- Scripts and automation procedures
- External service integrations and configurations

### When to Use GitHub Issues
- Feature implementations and their progress
- Bug fixes and their status
- Configuration changes and deployment steps
- Project tracking and status updates

## Usage

Add your management scripts, configuration files, and documentation at the root level.

## Updating OpenProject

To update the OpenProject submodule to the latest version:

```bash
cd openproject
git pull origin dev
cd ..
git add openproject
git commit -m "Update OpenProject submodule"
git push
```
