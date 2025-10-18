# Cloudflare R2 Setup Guide for OpenProject

This guide provides step-by-step instructions for configuring Cloudflare R2 as the object storage backend for OpenProject file attachments.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [R2 Bucket Creation](#r2-bucket-creation)
3. [API Token Generation](#api-token-generation)
4. [Local Configuration](#local-configuration)
5. [Configuration Details](#configuration-details)
6. [Testing the Setup](#testing-the-setup)
7. [Railway Deployment](#railway-deployment)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

- Cloudflare account with R2 access
- OpenProject repository cloned locally
- Text editor for configuration files
- Railway account (for production deployment)

---

## R2 Bucket Creation

### Step 1: Create the R2 Bucket

1. Log in to [Cloudflare Dashboard](https://dash.cloudflare.com)
2. Navigate to **R2** in the left sidebar (under Storage)
3. Click **Create Bucket**
4. Enter bucket name: `openproject-attachments`
5. Choose region closest to your deployment:
   - Recommended: `wnam` (Western North America) for US-based deployments
   - Or `apac` (Asia-Pacific) for Asian deployments
6. Click **Create Bucket**
7. Note the bucket name for later use

### Step 2: Verify Bucket Creation

- You should see the new bucket listed in your R2 dashboard
- Note the **Bucket Details** section which shows the endpoint information

---

## API Token Generation

### Step 1: Generate Scoped API Token

1. In Cloudflare Dashboard, go to **R2**
2. In the top-right corner, click **Settings** (or navigate to Account Settings → R2)
3. Go to the **API Tokens** tab
4. Click **Create API Token**

### Step 2: Configure Token Permissions

1. Select **Scoped API Token** (recommended for security)
2. Set the following permissions:

**Object Permissions:**
- ✓ `Object Read` (for downloading attachments)
- ✓ `Object Write` (for uploading attachments)
- ✓ `Object List` (for verifying files exist)
- ✓ `Object Delete` (for removing attachments)

**Bucket Permissions:**
- ✓ `Bucket Read` (for listing bucket contents)

Leave **Account** permissions unchecked.

### Step 3: Restrict Token to Specific Bucket

1. In the **Bucket Access** section, select **Specific buckets**
2. Select `openproject-attachments` from the dropdown
3. Leave **TTL (Time To Live)** blank for no expiration, or set an expiration date

### Step 4: Create and Save Credentials

1. Click **Create Token**
2. You'll see three values displayed (shown once only):
   - **Access Key ID** - Save this securely
   - **Secret Access Key** - Save this securely (last shown)
   - **Endpoint URL** - Format: `https://<account-id>.r2.cloudflarestorage.com`

⚠️ **Important:** Save these credentials in a secure location. The Secret Access Key is only shown once.

---

## Local Configuration

### Step 1: Update `.env.local`

1. Open `.env.local` file in the repository root
2. Replace the placeholder values with your actual R2 credentials:

```bash
ATTACHMENTS_STORAGE=fog

FOG='
{
  "credentials": {
    "provider": "AWS",
    "aws_access_key_id": "YOUR_ACCESS_KEY_ID",
    "aws_secret_access_key": "YOUR_SECRET_ACCESS_KEY",
    "region": "auto",
    "endpoint": "https://YOUR_ACCOUNT_ID.r2.cloudflarestorage.com"
  },
  "directory": "openproject-attachments"
}'
```

3. Replace:
   - `YOUR_ACCESS_KEY_ID` with your R2 Access Key ID
   - `YOUR_SECRET_ACCESS_KEY` with your R2 Secret Access Key
   - `YOUR_ACCOUNT_ID` with your Cloudflare account ID (from the endpoint URL)

### Step 2: Verify `.gitignore`

Ensure `.env.local` is in `.gitignore` to prevent credential exposure:

```bash
# Should already be in .gitignore
.env.local
.env.*.local
```

---

## Configuration Details

### Environment Variables Explained

| Variable | Description | Example |
|----------|-------------|---------|
| `ATTACHMENTS_STORAGE` | Storage backend type | `fog` |
| `FOG` | JSON configuration for fog gem | See JSON structure below |
| `credentials.provider` | Cloud provider type | `AWS` (R2 uses S3-compatible API) |
| `credentials.aws_access_key_id` | R2 API access key | From R2 token generation |
| `credentials.aws_secret_access_key` | R2 API secret key | From R2 token generation |
| `credentials.region` | R2 region code | `auto` (R2 handles regions automatically) |
| `credentials.endpoint` | R2 endpoint URL | `https://<account-id>.r2.cloudflarestorage.com` |
| `directory` | Bucket name | `openproject-attachments` |

### How OpenProject Reads Configuration

OpenProject uses the following precedence for loading configuration:

1. Environment variables (highest priority)
2. `config/settings.yml` file
3. Default values from `config/constants/settings/definition.rb`

The `.env.local` file is loaded by Rails during initialization via the `dotenv-rails` gem.

### CarrierWave Integration

OpenProject uses CarrierWave with the Fog gem for S3-compatible storage:

- **Initializer:** `openproject/config/initializers/carrierwave.rb`
- **Configuration Helper:** `openproject/lib_static/open_project/configuration/helpers.rb`
- **Settings Definition:** `openproject/config/constants/settings/definition.rb`

The configuration is automatically applied when:
1. `ATTACHMENTS_STORAGE=fog` is set
2. `FOG` environment variable contains valid credentials

---

## Testing the Setup

### Test 1: Verify Configuration Loading

```bash
cd openproject

# Check if Rails can load the configuration
bundle exec rails runner 'puts OpenProject::Configuration.attachments_storage'
# Should output: fog

bundle exec rails runner 'puts OpenProject::Configuration.fog_directory'
# Should output: openproject-attachments
```

### Test 2: Upload Test File

1. Start OpenProject locally (if not already running)
2. Create a new work package or open an existing one
3. In the **Files** tab, try uploading a test file
4. If successful, the file should be stored in R2 (not locally)

### Test 3: Verify File in R2 Dashboard

1. Go to Cloudflare R2 Dashboard
2. Click on `openproject-attachments` bucket
3. You should see the uploaded file listed
4. Verify file size matches the uploaded file

### Test 4: Download Test File

1. In OpenProject, click the file to download it
2. Verify the file downloads correctly
3. Check file contents match the original

### Test 5: Delete Test File

1. In OpenProject, delete the test file attachment
2. Verify the file is removed from R2 dashboard

---

## Railway Deployment

### Step 1: Add Environment Variables to Railway

1. Go to Railway project dashboard: https://railway.app/project/6ef0f0c6-a251-449e-ba97-2b9a14c17e2c
2. Select the **openproject** service
3. Go to the **Variables** tab
4. Add the following environment variables:

```
ATTACHMENTS_STORAGE=fog

FOG={
  "credentials": {
    "provider": "AWS",
    "aws_access_key_id": "YOUR_ACCESS_KEY_ID",
    "aws_secret_access_key": "YOUR_SECRET_ACCESS_KEY",
    "region": "auto",
    "endpoint": "https://YOUR_ACCOUNT_ID.r2.cloudflarestorage.com"
  },
  "directory": "openproject-attachments"
}
```

### Step 2: Redeploy Service

1. Click **Deploy** to trigger a new deployment
2. Monitor the deployment logs for any errors
3. Wait for deployment to complete

### Step 3: Verify Production Setup

1. Go to your production OpenProject instance (https://projects.brokerkit.app)
2. Create a test work package and upload a file
3. Verify the file uploads successfully
4. Check R2 dashboard to confirm file was stored there

---

## Troubleshooting

### Issue: "Fog credentials are empty"

**Cause:** `FOG` environment variable not set or malformed JSON

**Solution:**
- Verify `FOG` variable is set correctly in `.env.local` or Railway variables
- Check JSON syntax is valid (use JSON validator)
- Ensure credentials are enclosed in single quotes in shell

### Issue: "Invalid endpoint URL"

**Cause:** Endpoint URL is incorrect or missing `/`

**Solution:**
- Verify endpoint format: `https://<account-id>.r2.cloudflarestorage.com`
- Do not include trailing slash
- Ensure account ID matches your Cloudflare account

### Issue: "Access Denied" errors

**Cause:** API token permissions insufficient or credentials incorrect

**Solution:**
- Verify API token has Object Read, Write, List, Delete permissions
- Verify API token is restricted to `openproject-attachments` bucket
- Ensure Access Key ID and Secret are correct and not swapped
- Generate new token if unsure

### Issue: Files not appearing in R2

**Cause:** Configuration is pointing to local storage instead of R2

**Solution:**
- Verify `ATTACHMENTS_STORAGE=fog` is set
- Run `bundle exec rails runner 'puts OpenProject::Configuration.attachments_storage'`
- Should output `fog`, not `file`
- Restart Rails/OpenProject after changing environment variables

### Issue: "Region code invalid"

**Cause:** Region field must be set to `auto` for R2

**Solution:**
- Ensure `"region": "auto"` in FOG configuration
- R2 handles region routing automatically

### Issue: Deployment fails after configuration changes

**Cause:** JSON syntax error in environment variable

**Solution:**
- Validate JSON syntax separately
- Check Railway logs for detailed error messages
- Ensure all quotes are properly escaped
- Try deploying with minimal test configuration first

---

## Rollback Plan

If you need to revert to local file storage:

1. Remove `ATTACHMENTS_STORAGE` and `FOG` environment variables
2. Set `ATTACHMENTS_STORAGE=file` (or leave unset for default)
3. Redeploy OpenProject
4. **Note:** Existing files in R2 will not be accessible unless you configure R2 again

### Migrating Files Back to Local

Contact support if you need to migrate files from R2 back to local storage.

---

## Additional Resources

- [Cloudflare R2 Documentation](https://developers.cloudflare.com/r2/)
- [CarrierWave Fog Documentation](https://github.com/carrierwaveuploader/carrierwave/wiki/How-to-use-Fog)
- [OpenProject Storage Configuration](https://docs.openproject.org/system-admin-guide/files/attachments/)

---

## Support

For issues or questions about this setup:
1. Check the Troubleshooting section above
2. Review Railway deployment logs
3. Create an issue in the GitHub repository referencing this guide
