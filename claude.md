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
- AWS S3 for file attachments storage

## AWS S3 File Storage

OpenProject is configured to store file attachments in AWS S3 using the fog storage adapter.

### Configuration

**S3 Bucket:**
- **Bucket Name**: openproject-attachments-brokerkit
- **Region**: us-east-2 (US East Ohio)
- **IAM User**: openproject-s3-user
- **Required Permissions**: PutObject, GetObject, ListBucket, DeleteObject

**Railway Environment Variables:**
```bash
OPENPROJECT_ATTACHMENTS__STORAGE=fog
OPENPROJECT_FOG_CREDENTIALS_PROVIDER=AWS
OPENPROJECT_FOG_CREDENTIALS_AWS__ACCESS__KEY__ID=<access-key>
OPENPROJECT_FOG_CREDENTIALS_AWS__SECRET__ACCESS__KEY=<secret-key>
OPENPROJECT_FOG_CREDENTIALS_REGION=us-east-2
OPENPROJECT_FOG_DIRECTORY=openproject-attachments-brokerkit
OPENPROJECT_DIRECT__UPLOADS=false
```

### Direct Uploads

**Current Setting:** `OPENPROJECT_DIRECT__UPLOADS=false`

With direct uploads disabled, files are uploaded through the OpenProject server to S3. This is the recommended configuration for most use cases.

**Why Direct Uploads are Disabled:**
- ✅ Simpler configuration (no CORS complexity)
- ✅ All uploads validated by OpenProject server
- ✅ Works reliably for standard file sizes
- ✅ No browser CORS issues

**When to Enable Direct Uploads:**
- Uploading very large files (>100MB regularly)
- Many concurrent users uploading simultaneously
- Server resources are constrained

**To Enable Direct Uploads:**
1. S3 bucket CORS is already configured (see `s3-cors-config.json`)
2. Set `OPENPROJECT_DIRECT__UPLOADS=true` or remove the variable
3. Redeploy the application
4. Test browser-to-S3 uploads work correctly

### CORS Configuration

CORS is pre-configured on the S3 bucket to support direct uploads if needed in the future. Configuration file: `s3-cors-config.json`

```json
{
  "CORSRules": [
    {
      "AllowedOrigins": ["https://projects.brokerkit.app"],
      "AllowedMethods": ["GET", "PUT", "POST", "HEAD"],
      "AllowedHeaders": ["*"],
      "ExposeHeaders": ["ETag"],
      "MaxAgeSeconds": 3000
    }
  ]
}
```

**Apply CORS Configuration:**
```bash
export AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
export AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
export AWS_DEFAULT_REGION=us-east-2
aws s3api put-bucket-cors --bucket openproject-attachments-brokerkit --cors-configuration file://s3-cors-config.json
```

### Troubleshooting S3 Storage

**Verify S3 credentials work:**
```bash
source .env
aws s3 ls s3://openproject-attachments-brokerkit/
```

**Check uploaded files:**
```bash
aws s3 ls s3://openproject-attachments-brokerkit/uploads/ --recursive
```

**Test file upload:**
```bash
echo "test" | aws s3 cp - s3://openproject-attachments-brokerkit/test.txt
```

**View Railway logs for S3 errors:**
```bash
railway logs --service OpenProject --lines 200 | grep -i "s3\|fog\|upload\|attachment"
```

## Database Backups

Railway native backups are enabled for the PostgreSQL database to ensure data protection and recovery capabilities.

### Backup Configuration
- **Schedule**: Daily backups (every 24 hours)
- **Retention**: 6 days
- **Volume**: postgres-volume (`/var/lib/postgresql/data`)
- **Type**: Incremental, copy-on-write backups
- **Cost**: Charged only for incremental backup data (per GB/minute)

### Accessing Backups
1. Navigate to the Railway project dashboard: https://railway.app/project/$RAILWAY_PROJECT_ID
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

The Railway CLI is the primary tool for managing your OpenProject deployment on Railway. Use it for infrastructure troubleshooting, log review, and deployment diagnostics.

**Best Practice**: Use Railway CLI for all Railway operations when possible (instead of the UI) to automate changes, ensure consistency, and enable scripting.

### Setup & Authentication

**Option 1: Browser-based Login (Recommended)**
```bash
# One-time browser authentication
railway login
# This opens your browser and securely connects your account

# Verify authentication
railway whoami
```

**Option 2: API Token Authentication (for CI/CD & Scripts)**
```bash
# Get token from https://railway.app/account/tokens
# Store in .env file with key RAILWAY_API_TOKEN
# Use in commands: RAILWAY_TOKEN=$RAILWAY_API_TOKEN railway whoami
```

**Environment Setup (Recommended)**
```bash
# Add RAILWAY_API_TOKEN to .env file, then load it:
source .env
# Use the token in commands by referencing the environment variable
```

### Project Linking

Link the CLI to your specific Railway project (required for most operations):

```bash
# Link to the OpenProject deployment
railway link --project $RAILWAY_PROJECT_ID

# Verify you're linked to the correct project
railway list  # Shows all services in the project

# Check linked environment and service
railway status
```

**Project IDs for Reference** (stored in .env file)
- **Project ID**: From `.env` file as `$RAILWAY_PROJECT_ID`
- **Environment ID**: From `.env` file as `$RAILWAY_ENVIRONMENT_ID`
- **OpenProject Service ID**: From `.env` file as `$RAILWAY_SERVICE_ID`
- **PostgreSQL Service**: Available via `railway service`

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

**Redeploy after variable changes (with auto-confirmation):**
```bash
railway deployment redeploy -y
```

### Local Environment File (.env)

The `.env` file stores all local configuration and credentials. It is **gitignored** to prevent accidental credential exposure.

**Contents of .env**:
```bash
# Railway API token for CLI authentication
RAILWAY_API_TOKEN=<your_token>
RAILWAY_PROJECT_ID=<your_project_id>
RAILWAY_ENVIRONMENT_ID=<your_environment_id>
RAILWAY_SERVICE_ID=<your_service_id>

# AWS credentials for S3 operations
AWS_ACCESS_KEY_ID=<your_access_key>
AWS_SECRET_ACCESS_KEY=<your_secret_key>
AWS_REGION=us-east-2

# OpenProject file storage (AWS S3)
OPENPROJECT_ATTACHMENTS__STORAGE=fog
OPENPROJECT_FOG_CREDENTIALS_PROVIDER=AWS
OPENPROJECT_FOG_CREDENTIALS_AWS__ACCESS__KEY__ID=<your_access_key>
OPENPROJECT_FOG_CREDENTIALS_AWS__SECRET__ACCESS__KEY=<your_secret_key>
OPENPROJECT_FOG_CREDENTIALS_REGION=us-east-2
OPENPROJECT_FOG_DIRECTORY=openproject-attachments-brokerkit
```

**Loading .env**:
```bash
# Load environment variables from .env
source .env

# Verify they're loaded
echo $RAILWAY_API_TOKEN
echo $AWS_ACCESS_KEY_ID
```

**Important**: `.env` is in `.gitignore` and will never be committed. Keep it safe locally and never share credentials.

### Why Railway CLI Works for Droid

Railway CLI stores authentication locally and persists across shell sessions. This means:
- Each Execute call runs in a new isolated shell, but Railway CLI's cached authentication is available
- No need to re-authenticate between commands
- Droid can use Railway CLI directly without managing tokens in environment variables

This enables fast, automated Railway management without interactive browser logins.

### Using Railway CLI for Droid (Proven Workflow)

When I (Droid) use Railway CLI, I follow this proven pattern:

1. **Check status**: `railway status` (verifies authentication and project link)
2. **Set variables**: `railway variables --set "KEY=VALUE"` (supports JSON values)
3. **Monitor logs**: `railway logs --lines 200` (view deployment progress)
4. **Redeploy**: `railway deployment redeploy -y` (auto-confirm without prompts)
5. **Verify success**: Check logs for service startup messages

**Complete workflow example (S3 deployment):**
```bash
# Verify we're linked to the correct project
railway status

# Set S3 storage configuration
railway variables --set 'OPENPROJECT_ATTACHMENTS__STORAGE=fog'
railway variables --set 'OPENPROJECT_FOG_CREDENTIALS_PROVIDER=AWS'
railway variables --set 'OPENPROJECT_FOG_CREDENTIALS_AWS__ACCESS__KEY__ID=<key>'
railway variables --set 'OPENPROJECT_FOG_CREDENTIALS_AWS__SECRET__ACCESS__KEY=<secret>'
railway variables --set 'OPENPROJECT_FOG_CREDENTIALS_REGION=us-east-2'
railway variables --set 'OPENPROJECT_FOG_DIRECTORY=<bucket-name>'

# Verify variables were set
railway variables | grep OPENPROJECT

# Trigger redeploy with auto-confirmation
railway deployment redeploy -y

# Monitor startup (wait 30+ seconds for full boot)
sleep 30
railway logs --lines 100

# Filter for errors or success
railway logs --lines 200 | grep -i "listening\|success\|error"
```

**Key command syntax:**
- Set variables: `railway variables --set "KEY=VALUE"` (NOT `set` alone)
- Redeploy: `railway deployment redeploy -y` (NOT `railway deploy`)
- Auto-confirm: Add `-y` flag to skip interactive prompts
- View logs: `railway logs --lines <N>` or `railway logs --service <name>`
- List deployments: `railway deployment list`

### Best Practices

- **Use CLI over UI**: Automate operations, reduce errors, enable scripting
- **Load .env first**: `source .env` before running Railway CLI commands
- **Link projects**: Use `railway link` in project directories
- **Monitor logs regularly**: Use `railway logs` to catch issues early
- **Document changes**: Reference CLI commands in commit messages for reproducibility
- **Test before pushing**: Use CLI to verify changes before remote deployment
- **Keep .env safe**: Never commit, never share, store securely locally only

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
