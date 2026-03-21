#!/bin/bash

# Directly set passwords for all CMS users using ADMIN_TOKEN
# This bypasses the token flow and sets passwords directly

echo "=== Setting Passwords for All CMS Users ==="
echo ""

# Function to set password for a user
set_password() {
    local cms_name=$1
    local cms_url=$2
    local token=$3
    local username=$4
    local password=$5
    
    echo "Setting password for $username on $cms_name..."
    
    # Create SHA-256 hash of password
    password_hash=$(echo -n "$password" | sha256sum | cut -d' ' -f1)
    
    response=$(curl -s -X POST \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $token" \
        -d "{\"username\":\"$username\",\"passwordHash\":\"$password_hash\"}" \
        "$cms_url/api/auth/setup-password")
    
    if echo "$response" | grep -q "success"; then
        echo "✅ $username: Password set successfully"
    else
        echo "❌ $username: Failed - $response"
    fi
}

# Set a common password for all users
DEFAULT_PASSWORD="NewsCMS2025!"

echo "=== CMS ORIGINAUX (cms-originaux) ==="
set_password "cms-originaux" "https://cms-originaux.sebastianvernis.workers.dev" "$CMS_ORIGINAUX_TOKEN" "Respaldo" "$DEFAULT_PASSWORD"
set_password "cms-originaux" "https://cms-originaux.sebastianvernis.workers.dev" "$CMS_ORIGINAUX_TOKEN" "Rodrigo" "$DEFAULT_PASSWORD"
set_password "cms-originaux" "https://cms-originaux.sebastianvernis.workers.dev" "$CMS_ORIGINAUX_TOKEN" "SebastianVernis" "$DEFAULT_PASSWORD"
set_password "cms-originaux" "https://cms-originaux.sebastianvernis.workers.dev" "$CMS_ORIGINAUX_TOKEN" "azeem" "$DEFAULT_PASSWORD"
set_password "cms-originaux" "https://cms-originaux.sebastianvernis.workers.dev" "$CMS_ORIGINAUX_TOKEN" "demo_user" "$DEFAULT_PASSWORD"

echo ""
echo "=== CMS NUEVOS (cms-nuevos) ==="
set_password "cms-nuevos" "https://cms-nuevos.sebastianvernis.workers.dev" "$CMS_NUEVOS_TOKEN" "Respaldo" "$DEFAULT_PASSWORD"
set_password "cms-nuevos" "https://cms-nuevos.sebastianvernis.workers.dev" "$CMS_NUEVOS_TOKEN" "Rodrigo" "$DEFAULT_PASSWORD"
set_password "cms-nuevos" "https://cms-nuevos.sebastianvernis.workers.dev" "$CMS_NUEVOS_TOKEN" "SebastianVernis" "$DEFAULT_PASSWORD"
set_password "cms-nuevos" "https://cms-nuevos.sebastianvernis.workers.dev" "$CMS_NUEVOS_TOKEN" "azeem" "$DEFAULT_PASSWORD"
set_password "cms-nuevos" "https://cms-nuevos.sebastianvernis.workers.dev" "$CMS_NUEVOS_TOKEN" "demo_user" "$DEFAULT_PASSWORD"

echo ""
echo "=== CMS NUEVOS2 (cms-nuevos2) ==="
set_password "cms-nuevos2" "https://cms-nuevos2.sebastianvernis.workers.dev" "$CMS_NUEVOS2_TOKEN" "Respaldo" "$DEFAULT_PASSWORD"
set_password "cms-nuevos2" "https://cms-nuevos2.sebastianvernis.workers.dev" "$CMS_NUEVOS2_TOKEN" "Rodrigo" "$DEFAULT_PASSWORD"
set_password "cms-nuevos2" "https://cms-nuevos2.sebastianvernis.workers.dev" "$CMS_NUEVOS2_TOKEN" "SebastianVernis" "$DEFAULT_PASSWORD"
set_password "cms-nuevos2" "https://cms-nuevos2.sebastianvernis.workers.dev" "$CMS_NUEVOS2_TOKEN" "azeem" "$DEFAULT_PASSWORD"
set_password "cms-nuevos2" "https://cms-nuevos2.sebastianvernis.workers.dev" "$CMS_NUEVOS2_TOKEN" "demo_user" "$DEFAULT_PASSWORD"

echo ""
echo "=== Summary ==="
echo "Password for all users: $DEFAULT_PASSWORD"
echo ""
echo "Users can now log in with:"
echo "- Username: [their username]"
echo "- Password: $DEFAULT_PASSWORD"
echo ""
echo "CMS URLs:"
echo "- cms-originaux: https://cms-originaux.sebastianvernis.workers.dev/admin/"
echo "- cms-nuevos: https://cms-nuevos.sebastianvernis.workers.dev/admin/"
echo "- cms-nuevos2: https://cms-nuevos2.sebastianvernis.workers.dev/admin/"
