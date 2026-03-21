#!/bin/bash

# Generate password setup links for all CMS users
# Requires CMS_ORIGINAUX_TOKEN, CMS_NUEVOS_TOKEN, CMS_NUEVOS2_TOKEN environment variables

echo "=== Generating Password Setup Links ==="
echo ""

# Function to generate password link for a user
generate_link() {
    local cms_name=$1
    local cms_url=$2
    local token=$3
    local username=$4
    
    echo "Generating link for $username on $cms_name..."
    
    response=$(curl -s -X POST \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $token" \
        -d "{\"username\":\"$username\"}" \
        "$cms_url/api/auth/generate-password-token")
    
    if echo "$response" | grep -q "setupUrl"; then
        setup_url=$(echo "$response" | grep -o '"setupUrl":"[^"]*"' | cut -d'"' -f4)
        echo "✅ $username: $setup_url"
        echo ""
    else
        echo "❌ $username: Failed - $response"
        echo ""
    fi
}

echo "=== CMS ORIGINAUX (cms-originaux) ==="
echo "URL: https://cms-originaux.sebastianvernis.workers.dev"
echo ""
generate_link "cms-originaux" "https://cms-originaux.sebastianvernis.workers.dev" "$CMS_ORIGINAUX_TOKEN" "Respaldo"
generate_link "cms-originaux" "https://cms-originaux.sebastianvernis.workers.dev" "$CMS_ORIGINAUX_TOKEN" "Rodrigo"
generate_link "cms-originaux" "https://cms-originaux.sebastianvernis.workers.dev" "$CMS_ORIGINAUX_TOKEN" "SebastianVernis"
generate_link "cms-originaux" "https://cms-originaux.sebastianvernis.workers.dev" "$CMS_ORIGINAUX_TOKEN" "azeem"
generate_link "cms-originaux" "https://cms-originaux.sebastianvernis.workers.dev" "$CMS_ORIGINAUX_TOKEN" "demo_user"

echo ""
echo "=== CMS NUEVOS (cms-nuevos) ==="
echo "URL: https://cms-nuevos.sebastianvernis.workers.dev"
echo ""
# Get users from cms-nuevos
users_nuevos=$(curl -s -H "Authorization: Bearer $CMS_NUEVOS_TOKEN" "https://cms-nuevos.sebastianvernis.workers.dev/api/auth/users" | grep -o '"NOMBRE":"[^"]*"' | cut -d'"' -f4)
for user in $users_nuevos; do
    generate_link "cms-nuevos" "https://cms-nuevos.sebastianvernis.workers.dev" "$CMS_NUEVOS_TOKEN" "$user"
done

echo ""
echo "=== CMS NUEVOS2 (cms-nuevos2) ==="
echo "URL: https://cms-nuevos2.sebastianvernis.workers.dev"
echo ""
# Get users from cms-nuevos2
users_nuevos2=$(curl -s -H "Authorization: Bearer $CMS_NUEVOS2_TOKEN" "https://cms-nuevos2.sebastianvernis.workers.dev/api/auth/users" | grep -o '"NOMBRE":"[^"]*"' | cut -d'"' -f4)
for user in $users_nuevos2; do
    generate_link "cms-nuevos2" "https://cms-nuevos2.sebastianvernis.workers.dev" "$CMS_NUEVOS2_TOKEN" "$user"
done

echo ""
echo "=== Instructions ==="
echo "1. Share the setup URLs with each user"
echo "2. Each URL is valid for 24 hours"
echo "3. Users should visit the URL and set their password"
echo "4. After setting password, they can log in normally"
echo ""
echo "Note: If a user already has a password set, this will create a new setup link anyway."
