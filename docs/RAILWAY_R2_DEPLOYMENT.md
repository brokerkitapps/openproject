# Railway R2 Deployment Quick Reference

This guide provides quick steps to deploy R2 storage configuration to Railway.

## Quick Start

### Step 1: Navigate to Railway Dashboard

1. Go to https://railway.app/project/6ef0f0c6-a251-449e-ba97-2b9a14c17e2c
2. Click on the **openproject** service

### Step 2: Add Environment Variables

1. Click the **Variables** tab
2. Click **+ Add Variable** (or raw editor)
3. Add these two variables:

**Variable 1:**
```
ATTACHMENTS_STORAGE
fog
```

**Variable 2:**
```
FOG
{"credentials":{"provider":"AWS","aws_access_key_id":"YOUR_ACCESS_KEY_ID","aws_secret_access_key":"YOUR_SECRET_ACCESS_KEY","region":"auto","endpoint":"https://YOUR_ACCOUNT_ID.r2.cloudflarestorage.com"},"directory":"openproject-attachments"}
```

Replace:
- `YOUR_ACCESS_KEY_ID` with your R2 Access Key ID
- `YOUR_SECRET_ACCESS_KEY` with your R2 Secret Access Key  
- `YOUR_ACCOUNT_ID` with your Cloudflare account ID

4. Click **Deploy** to trigger a new deployment

### Step 3: Monitor Deployment

1. Click **Deployments** tab
2. Watch the deployment progress
3. Check logs for any errors
4. Wait for green checkmark (deployment complete)

### Step 4: Test in Production

1. Go to your OpenProject instance: https://projects.brokerkit.app
2. Create a new work package
3. Upload a test file in the Files tab
4. Verify file uploads successfully
5. Check R2 dashboard to confirm file appears there

## Troubleshooting Deployment

### Issue: Deployment fails immediately

**Check:**
1. FOG variable syntax is correct (no line breaks)
2. JSON is valid (use online JSON validator)
3. All quotes are present and matching

### Issue: Deployment succeeds but files don't upload

**Check:**
1. Log into production OpenProject
2. Try uploading a file
3. Check Railway logs for errors:
   - Click **Logs** tab in Railway
   - Search for "fog" or "S3" keywords
4. Verify R2 credentials are correct

### Issue: "Invalid endpoint" error

**Check:**
1. Endpoint URL format is: `https://YOUR_ACCOUNT_ID.r2.cloudflarestorage.com`
2. Replace `YOUR_ACCOUNT_ID` with your actual Cloudflare R2 account ID
3. No trailing slash at the end
4. Account ID matches your Cloudflare account

## Environment Variables Explained

| Variable | Value | Purpose |
|----------|-------|---------|
| `ATTACHMENTS_STORAGE` | `fog` | Enable remote object storage |
| `FOG` | JSON config | R2 credentials and endpoint |

The `FOG` JSON contains:
- **provider**: Always "AWS" (R2 is S3-compatible)
- **aws_access_key_id**: Your R2 access key
- **aws_secret_access_key**: Your R2 secret key
- **region**: Always "auto" (R2 handles regions automatically)
- **endpoint**: Your R2 account endpoint URL
- **directory**: The bucket name "openproject-attachments"

## If You Need to Rollback

1. Remove or comment out both variables in Railway
2. Click **Deploy**
3. Wait for redeployment
4. OpenProject will revert to local file storage

## Verifying Configuration

### Via Railway Dashboard

1. Click the **openproject** service
2. Click **Variables** tab
3. Both variables should be visible
4. Click **Show** to see the values

### Via OpenProject Interface

1. Log in as administrator
2. Go to System Admin → Files → Attachments
3. You should see attachment settings
4. Upload a test file to verify it works

### Via R2 Dashboard

1. Go to Cloudflare R2 dashboard
2. Click **openproject-attachments** bucket
3. You should see uploaded files there
4. Verify file sizes and dates match your uploads

## Common Issues & Solutions

### Files upload but don't appear in R2

**Solution:**
- Verify `ATTACHMENTS_STORAGE=fog` is set correctly
- Restart the service (redeploy)
- Check Rails logs for configuration errors

### "Invalid credentials" error

**Solution:**
- Double-check Access Key ID and Secret Key
- Verify they weren't accidentally swapped
- Regenerate token in Cloudflare if unsure

### Deployment hangs or times out

**Solution:**
- Check Railway logs
- Verify endpoint URL is reachable (no typos)
- Try simpler deployment first (just set one variable)

## Next Steps After Successful Deployment

1. ✅ Test file uploads in production
2. ✅ Test file downloads
3. ✅ Test file deletion
4. ✅ Commit configuration to git
5. ✅ Update deployment documentation
6. ✅ Monitor R2 costs and usage

## Support

See **R2_SETUP_GUIDE.md** for comprehensive troubleshooting and setup information.
