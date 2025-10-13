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

## Railway CLI

The Railway CLI is used for infrastructure troubleshooting and log review. It provides direct access to your Railway deployment for monitoring and debugging.

### Authentication

Authenticate with your Railway API token:

```bash
export RAILWAY_TOKEN=your_api_token_here
railway whoami  # Verify authentication
```

### Common Commands

**View real-time logs:**
```bash
railway logs
```

**Check service status:**
```bash
railway status
```

**Link to your project:**
```bash
railway link
```

**List available services:**
```bash
railway service
```

**Get help:**
```bash
railway --help
```

### Troubleshooting

Use the Railway CLI for:
- Monitoring application logs in real-time
- Debugging deployment issues
- Checking service health and status
- Viewing environment variables
- Investigating connectivity problems

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
