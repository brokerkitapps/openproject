# R2 Setup Completion Checklist

## What Has Been Completed ✅

### Phase 1: Planning & Documentation
- ✅ Created GitHub Issue #3: "Configure Cloudflare R2 for File Storage"
- ✅ Created comprehensive guides in `docs/` folder:
  - `R2_SETUP_GUIDE.md` - Complete setup instructions (bucket creation, API token, testing)
  - `R2_IMPLEMENTATION_SUMMARY.md` - Implementation details and configuration explanation
  - `RAILWAY_R2_DEPLOYMENT.md` - Quick reference for Railway deployment

### Phase 2: Cloudflare R2 Setup (Completed by User)
- ✅ Created R2 bucket: `openproject-attachments`
- ✅ Generated Scoped API Token with credentials

### Phase 3: Local Configuration
- ✅ Created `.env.local` file with R2 credentials (properly gitignored)
- ✅ Verified configuration format matches OpenProject requirements

### Phase 4: Git Commits
- ✅ Committed documentation to repository
- ✅ All commits related to GitHub Issue #3

---

## What's Pending 📋

### Next Step 1: Railway Deployment
1. Go to Railway dashboard: https://railway.app/project/6ef0f0c6-a251-449e-ba97-2b9a14c17e2c
2. Select the **openproject** service
3. Click **Variables** tab
4. Add two environment variables:
   - `ATTACHMENTS_STORAGE=fog`
   - `FOG=<your R2 JSON from .env.local>`
5. Click **Deploy**
6. Monitor deployment logs

**See `docs/RAILWAY_R2_DEPLOYMENT.md` for detailed steps**

### Next Step 2: Production Testing
1. Log into production OpenProject: https://projects.brokerkit.app
2. Create test work package
3. Upload a test file
4. Verify file appears in R2 dashboard
5. Test download and delete

### Next Step 3: Validation
- [ ] Files upload successfully to R2
- [ ] Files download correctly from R2
- [ ] Files delete from R2 when removed
- [ ] No errors in production logs
- [ ] Performance is acceptable

---

## File Locations

### Configuration
- **Local credentials**: `.env.local` (gitignored, contains plaintext credentials)
- **Railway credentials**: To be added to Railway Variables tab

### Documentation
- `docs/R2_SETUP_GUIDE.md` - Comprehensive setup guide
- `docs/R2_IMPLEMENTATION_SUMMARY.md` - Implementation details
- `docs/RAILWAY_R2_DEPLOYMENT.md` - Quick deployment reference
- `docs/RAILWAY_R2_DEPLOYMENT.md` - Troubleshooting guide

### Source Code
- `openproject/config/initializers/carrierwave.rb` - CarrierWave configuration (no changes needed)
- `openproject/lib_static/open_project/configuration/helpers.rb` - Configuration parsing (no changes needed)

---

## Key Information

### R2 Configuration in `.env.local`

Your `.env.local` file contains:
```
ATTACHMENTS_STORAGE=fog
FOG=<JSON with your credentials>
```

This configuration:
- ✅ Is gitignored (credentials never committed)
- ✅ Uses S3-compatible R2 API with Fog gem
- ✅ Points to `openproject-attachments` bucket
- ✅ Works without any code changes to OpenProject

### How It Works

1. Rails loads `.env.local` via dotenv-rails gem
2. CarrierWave reads FOG environment variable
3. CarrierWave configures Fog AWS provider
4. Fog connects to R2 using S3-compatible endpoint
5. File uploads go to R2 instead of local filesystem

### Security

⚠️ **Important:**
- `.env.local` is in `.gitignore` and will never be committed
- Credentials are only stored in:
  - `.env.local` on local machine (gitignored)
  - Railway Variables in production (encrypted)
- Never share credentials in messages or documentation

---

## Deployment Checklist

Before deploying to production:

- [ ] Reviewed `docs/RAILWAY_R2_DEPLOYMENT.md`
- [ ] Gathered R2 credentials from `.env.local`
- [ ] Accessed Railway dashboard
- [ ] Added environment variables to openproject service
- [ ] Verified JSON syntax is correct
- [ ] Clicked Deploy button
- [ ] Monitored deployment logs

After deployment:

- [ ] Logged into production OpenProject
- [ ] Created test work package
- [ ] Uploaded test file
- [ ] Verified file in R2 dashboard
- [ ] Downloaded file to verify content
- [ ] Deleted file to verify removal from R2
- [ ] Checked application logs for errors

---

## Rollback Plan

If anything goes wrong:

1. Remove `ATTACHMENTS_STORAGE` and `FOG` variables from Railway
2. Click **Deploy** to redeploy with local file storage
3. OpenProject reverts to using local filesystem
4. Existing R2 files remain in R2 for future access

---

## Support Resources

- **R2 Setup Guide**: `docs/R2_SETUP_GUIDE.md`
- **Deployment Guide**: `docs/RAILWAY_R2_DEPLOYMENT.md`
- **Implementation Details**: `docs/R2_IMPLEMENTATION_SUMMARY.md`
- **GitHub Issue**: #3 - Configure Cloudflare R2 for File Storage
- **Cloudflare Docs**: https://developers.cloudflare.com/r2/

---

## Timeline

**Completed:**
- Initial documentation and planning
- R2 bucket creation
- API token generation
- Local configuration
- Git commits

**Next:**
- Railway deployment
- Production testing
- Validation and monitoring

---

## Questions?

Refer to the troubleshooting sections in:
- `docs/R2_SETUP_GUIDE.md#troubleshooting`
- `docs/RAILWAY_R2_DEPLOYMENT.md#troubleshooting-deployment`
