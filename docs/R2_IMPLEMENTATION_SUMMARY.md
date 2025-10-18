# R2 Implementation Summary

This document summarizes the Cloudflare R2 setup for OpenProject file storage and provides next steps.

## What Has Been Completed

### ✅ Phase 1: Preparation & Documentation
- [x] Created GitHub Issue #3: "Configure Cloudflare R2 for File Storage"
- [x] Created comprehensive R2_SETUP_GUIDE.md with:
  - R2 bucket creation steps
  - API token generation with permissions
  - Configuration format and environment variables
  - Local testing procedures
  - Railway deployment instructions
  - Troubleshooting guide

### ✅ Phase 2: Cloudflare R2 Setup (Completed by User)
- [x] Created R2 bucket: `openproject-attachments`
- [x] Generated Account API Token with credentials
  - ⚠️ **Credentials stored in `.env.local` (gitignored for security)**
  - See `.env.local` file for Access Key ID, Secret Key, and Endpoint URL

### ✅ Phase 3: Local Configuration
- [x] Created `.env.local` file with R2 credentials
- [x] Verified `.env.local` is in `.gitignore` (credentials are protected)
- [x] Configuration format follows OpenProject's fog settings structure

## How the Configuration Works

### Environment Variable Format

OpenProject reads the `FOG` environment variable as JSON:

```json
{
  "credentials": {
    "provider": "AWS",
    "aws_access_key_id": "YOUR_KEY",
    "aws_secret_access_key": "YOUR_SECRET",
    "region": "auto",
    "endpoint": "https://YOUR_ACCOUNT_ID.r2.cloudflarestorage.com"
  },
  "directory": "openproject-attachments"
}
```

### How It Works in OpenProject

1. **Rails loads `.env.local`** via the `dotenv-rails` gem during startup
2. **Environment variables are parsed** by `config/initializers/carrierwave.rb`
3. **Configuration helper** (`lib_static/open_project/configuration/helpers.rb`) extracts:
   - `fog_credentials` from the JSON structure
   - `fog_directory` (bucket name)
4. **CarrierWave** is configured to use Fog AWS provider with R2 endpoint
5. **File uploads** go directly to R2 instead of local filesystem

### Key Files

| File | Purpose |
|------|---------|
| `.env.local` | Stores R2 credentials (gitignored) |
| `config/initializers/carrierwave.rb` | Configures CarrierWave with Fog |
| `lib_static/open_project/configuration/helpers.rb` | Parses fog configuration |
| `docs/R2_SETUP_GUIDE.md` | Complete setup instructions |

## Next Steps

### Step 1: Deploy to Railway (Production)

1. **Add environment variables to Railway:**
   - Go to: https://railway.app/project/6ef0f0c6-a251-449e-ba97-2b9a14c17e2c
   - Select the **openproject** service
   - Click **Variables** tab
   - Add the following environment variables:

   ```
   ATTACHMENTS_STORAGE=fog
   FOG={"credentials":{"provider":"AWS","aws_access_key_id":"<YOUR_KEY>","aws_secret_access_key":"<YOUR_SECRET>","region":"auto","endpoint":"https://<YOUR_ACCOUNT_ID>.r2.cloudflarestorage.com"},"directory":"openproject-attachments"}
   ```
   
   ⚠️ **Replace placeholders with your actual R2 credentials from `.env.local`**

   **Note:** Format as single line (no newlines) for environment variable

2. **Trigger deployment:**
   - Click **Deploy** button
   - Monitor deployment logs for errors
   - Wait for deployment to complete

3. **Verify production deployment:**
   - Access your OpenProject instance
   - Create a test work package
   - Upload a test file
   - Check R2 dashboard to confirm file appears there

### Step 2: Local Testing (Optional)

If you have OpenProject running locally:

1. **Verify configuration loads:**
   ```bash
   cd openproject
   bundle exec rails runner 'puts OpenProject::Configuration.attachments_storage'
   # Should output: fog
   ```

2. **Test file upload:**
   - Create a work package
   - Upload a test file
   - Verify file appears in R2 dashboard

3. **Test file download:**
   - Download the file from OpenProject
   - Verify content is correct

4. **Test file deletion:**
   - Delete the attachment from work package
   - Verify file is removed from R2

### Step 3: Create Git Commit

Once everything works in production:

```bash
git add .env.local docs/R2_SETUP_GUIDE.md docs/R2_IMPLEMENTATION_SUMMARY.md
git commit -m "Configure Cloudflare R2 for file storage

- Set up R2 bucket for OpenProject attachments
- Configure fog gem with R2 S3-compatible endpoint
- Update environment variables for R2 credentials
- Create comprehensive R2 setup documentation

Closes #3"
```

### Step 4: Monitor and Validate

- Monitor Railway logs for any errors
- Verify existing functionality still works:
  - Work package creation
  - File uploads
  - File downloads
  - File deletion
- Check R2 storage usage and costs

## Configuration Details

### R2 Endpoint Explanation

The endpoint URL format `https://YOUR_ACCOUNT_ID.r2.cloudflarestorage.com` is:
- **Account-specific**: Your unique Cloudflare R2 account identifier (found in your R2 credentials)
- **S3-compatible**: R2 provides an S3-compatible API, so CarrierWave's AWS provider works without modification
- **Default region**: The `"region": "auto"` tells R2 to handle region routing automatically

### Why This Works

1. **CarrierWave** uses the Fog gem for cloud storage
2. **Fog AWS provider** works with any S3-compatible API
3. **Custom endpoint** configuration allows pointing to R2 instead of AWS S3
4. **No code changes** needed—pure configuration

## Troubleshooting

### Issue: "Credentials not loading"

**Check:**
1. `.env.local` exists in repository root (not in `openproject/` subdirectory)
2. Environment variables are set correctly in Railway dashboard
3. JSON in FOG variable has no syntax errors (verify with JSON validator)

### Issue: "Files not uploading to R2"

**Check:**
1. `ATTACHMENTS_STORAGE=fog` is set
2. `FOG` variable contains valid credentials
3. R2 bucket `openproject-attachments` exists
4. API token has Object Write permissions

### Issue: "Access Denied" error

**Check:**
1. Access Key ID and Secret Access Key are correct
2. API token has correct permissions (Object Read/Write/List/Delete)
3. Endpoint URL matches your R2 account
4. Credentials haven't been revoked in Cloudflare dashboard

## Security Notes

⚠️ **Important:**
- `.env.local` is in `.gitignore` and will never be committed
- Credentials should only be in `.env.local` (local) and Railway Variables (production)
- Never commit credentials to git or share in messages
- If credentials are accidentally exposed, regenerate them in Cloudflare dashboard
- Use scoped API tokens (not account-level tokens) for security

## Rollback Plan

If you need to revert to local file storage:

1. **Remove from Railway:**
   - Delete `ATTACHMENTS_STORAGE` and `FOG` variables from Railway
   - Redeploy

2. **Remove from local:**
   - Delete or comment out variables in `.env.local`
   - Restart OpenProject

3. **Local files (if needed):**
   - Files in R2 will persist
   - To access again, reconfigure R2

## Additional Resources

- [Cloudflare R2 Documentation](https://developers.cloudflare.com/r2/)
- [CarrierWave Fog Documentation](https://github.com/carrierwaveuploader/carrierwave/wiki/How-to-use-Fog)
- [OpenProject Configuration](https://docs.openproject.org/system-admin-guide/files/attachments/)
- GitHub Issue #3: Configure Cloudflare R2 for File Storage

## Support

For issues:
1. Review the R2_SETUP_GUIDE.md troubleshooting section
2. Check Railway deployment logs
3. Verify R2 credentials and permissions in Cloudflare dashboard
4. Create GitHub issue with error messages and logs
