# 🔐 Security Fix: Remove API Keys from Git

## ❌ **CRITICAL SECURITY ISSUE DETECTED**

The file `scripts/wp-setup.sh` contains sensitive credentials:
- WordPress username
- WordPress Application Password (API key)

**These credentials MUST NOT be committed to Git!**

## 🛡️ **Immediate Security Actions Required**

### 1. **Check Git Status**
```bash
git status
```

### 2. **If NOT yet committed - Add to .gitignore**
```bash
# Add to .gitignore to prevent accidental commits
echo "scripts/wp-setup.sh" >> .gitignore
echo "**/*wp-setup*" >> .gitignore
echo "**/*.env" >> .gitignore
echo "**/config.local.*" >> .gitignore
```

### 3. **If ALREADY committed - Remove from Git History**
```bash
# Remove from Git tracking (keeps local file)
git rm --cached scripts/wp-setup.sh

# Commit the removal
git commit -m "Remove sensitive credentials file from tracking"

# Add to .gitignore
echo "scripts/wp-setup.sh" >> .gitignore
git add .gitignore
git commit -m "Add credentials file to .gitignore"
```

### 4. **If ALREADY pushed to GitHub - URGENT ACTION**
```bash
# 1. Change WordPress Application Password immediately
# 2. Consider the current password compromised
# 3. Remove from Git history using git-filter-branch or BFG
# 4. Force push to overwrite history (if possible)
```

## 🔧 **Secure Solution Implementation**

### Option 1: Environment Variables (Recommended)
```bash
# Create secure setup script
cat > scripts/wp-setup-secure.sh << 'EOF'
#!/bin/bash
# Secure WordPress setup script

# Check if environment variables are set
if [ -z "$WP_SITE" ] || [ -z "$WP_USER" ] || [ -z "$WP_APP_PASS" ]; then
    echo "❌ Error: WordPress credentials not set"
    echo "Please set the following environment variables:"
    echo "export WP_SITE='https://spherevista360.com'"
    echo "export WP_USER='your_username'"
    echo "export WP_APP_PASS='your_app_password'"
    exit 1
fi

echo "✅ WordPress credentials loaded from environment"
echo "🌐 Site: $WP_SITE"
echo "👤 User: $WP_USER"
echo "🔑 Password: [HIDDEN]"

# Run the WordPress agent
python wp_agent_bulk.py /absolute/path/to/posts_to_upload
EOF

chmod +x scripts/wp-setup-secure.sh
```

### Option 2: Local Configuration File
```bash
# Create local config file (not tracked by Git)
cat > scripts/wp-config.local.sh << 'EOF'
#!/bin/bash
# Local WordPress configuration (DO NOT COMMIT)
export WP_SITE="https://spherevista360.com"
export WP_USER="JK"
export WP_APP_PASS="R8sj tOZG 8ORr ntSZ XlPt qTE9"
EOF

# Create secure setup script that sources the local config
cat > scripts/wp-setup-with-config.sh << 'EOF'
#!/bin/bash
# WordPress setup with local configuration

# Source local configuration
CONFIG_FILE="$(dirname "$0")/wp-config.local.sh"
if [ -f "$CONFIG_FILE" ]; then
    source "$CONFIG_FILE"
    echo "✅ Loaded configuration from $CONFIG_FILE"
else
    echo "❌ Configuration file not found: $CONFIG_FILE"
    echo "Please create wp-config.local.sh with your credentials"
    exit 1
fi

# Run the WordPress agent
python wp_agent_bulk.py /absolute/path/to/posts_to_upload
EOF

chmod +x scripts/wp-setup-with-config.sh
```

### Option 3: Interactive Setup
```bash
# Create interactive setup script
cat > scripts/wp-setup-interactive.sh << 'EOF'
#!/bin/bash
# Interactive WordPress setup

echo "🔐 WordPress Setup - Secure Credential Input"
echo "============================================"

# Get site URL
read -p "WordPress Site URL [https://spherevista360.com]: " wp_site
WP_SITE=${wp_site:-https://spherevista360.com}

# Get username
read -p "WordPress Username: " WP_USER

# Get password (hidden input)
echo -n "WordPress App Password: "
read -s WP_APP_PASS
echo

# Verify inputs
echo ""
echo "Configuration Summary:"
echo "Site: $WP_SITE"
echo "User: $WP_USER"
echo "Password: [HIDDEN]"
echo ""

read -p "Proceed with WordPress operations? (y/N): " confirm
if [[ $confirm == [yY] || $confirm == [yY][eE][sS] ]]; then
    export WP_SITE WP_USER WP_APP_PASS
    python wp_agent_bulk.py /absolute/path/to/posts_to_upload
else
    echo "Operation cancelled"
    exit 1
fi
EOF

chmod +x scripts/wp-setup-interactive.sh
```

## 📋 **Updated .gitignore**

Add these entries to your `.gitignore`:
```
# WordPress credentials and sensitive files
scripts/wp-setup.sh
scripts/wp-config.local.sh
scripts/*.local.*
**/*credentials*
**/*.env
**/*.env.local
**/config.local.*

# API keys and tokens
**/*api*key*
**/*secret*
**/*token*
**/*password*

# Temporary and cache files
temp_images/
**/.cache/
**/node_modules/
**/__pycache__/
```

## 🚨 **Immediate Action Plan**

1. **Check if already committed**:
   ```bash
   git log --oneline --grep="wp-setup"
   git log --oneline -- scripts/wp-setup.sh
   ```

2. **If committed but not pushed**:
   ```bash
   git reset --soft HEAD~1  # Undo last commit
   echo "scripts/wp-setup.sh" >> .gitignore
   git add .gitignore
   git commit -m "Add security .gitignore rules"
   ```

3. **If already pushed**:
   - **IMMEDIATELY** change WordPress Application Password
   - Consider current credentials compromised
   - Remove from Git history using advanced Git techniques

4. **Implement secure solution**:
   - Choose one of the three options above
   - Test the secure setup
   - Update documentation

## 🔒 **Security Best Practices**

- **Never commit credentials** to version control
- **Use environment variables** for sensitive data
- **Create local config files** excluded from Git
- **Implement interactive prompts** for credentials
- **Regularly rotate API keys** and passwords
- **Use dedicated service accounts** for automation
- **Enable 2FA** where possible

---

**Status**: 🚨 URGENT - Secure credentials before any Git operations!