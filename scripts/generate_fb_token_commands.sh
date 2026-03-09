#!/bin/bash
# Script para generar los comandos wrangler para configurar los FB tokens
# Ejecutar desde el directorio src/

cd /mnt/c/Users/soluc/cloudflare-news-project/src

echo "=========================================="
echo "Configuración de Facebook Tokens"
echo "=========================================="
echo ""

# Tokens para nuevos sitios (extraídos del User Token)
echo "Estos son los tokens para los NUEVOS sitios:"
echo ""

echo "1. mexicantimes (Mexican Times)"
echo "   wrangler secret put FB_TOKEN_MEXICANTIMES --name news-api"
echo "   Token: EAAmv1Puxa7wBQ6cYjgpntD2DQt9OQoDfr9lhcP0GeYvOc1ER6um1WHd9bcmP9J1Nl7nX4WUZBWsFaCPRFZCPkeX0iCLRp795IkCHOKeijeUtJa82NRlkkaxeB9GEuKCrrzn4nPf0TtM6eqJy4qwLBwpwn2ZASfqwMMEZBafxJuVXZBrmYsmZCPuHwTAU499BdxYtqLimVilUpeQhZBPxhWHIeF0"
echo ""

echo "2. televisionabc (ABC Television)"
echo "   wrangler secret put FB_TOKEN_TELEVISIONABC --name news-api"
echo "   Token: EAAmv1Puxa7wBQ4RhPiEM1ZCn8rZCYwZCKQk5RlVXAa3T94sLxWoRjODqCCJDY961gFdihqFSQ1IZCaYeBHl627Pimk9UeMSvp3ZCrZAQ9LhiIUf9xpXgCsuAWBCV4Jl94TG9ZCGplZAWUp9CfkqcwmH5bPPWi1os0rumx6SMpodJvapT6ZCAFmDAHWVlFZCQYVZAqh86wXZCyzlCrZAngsIyRSLTKdcUu"
echo ""

echo "3. capitalpress (Capital Press)"
echo "   wrangler secret put FB_TOKEN_CAPITALPRESS --name news-api"
echo "   Token: EAAmv1Puxa7wBQ6cYjgpntD2DQt9OQoDfr9lhcP0GeYvOc1ER6um1WHd9bcmP9J1Nl7nX4WUZBWsFaCPRFZCPkeX0iCLRp795IkCHOKeijeUtJa82NRlkkaxeB9GEuKCrrzn4nPf0TtM6eqJy4qwLBwpwn2ZASfqwMMEZBafxJuVXZBrmYsmZCPuHwTAU499BdxYtqLimVilUpeQhZBPxhWHIeF0"
echo ""

echo "4. mradio (M radio)"
echo "   wrangler secret put FB_TOKEN_MRADIO --name news-api"
echo "   Token: EAAmv1Puxa7wBQzVMK1vCknwZAOPgtFAcajt39R85lpGaAuitWbEZCOnh53rPahcIRsgaK6gAYWwxZBZBWvheAQAJiAmQCYcZAQtdXo2v8CvHIVaPAEWDRPyQZA2ebfLWU2uOkZABZCzNwsdSBQkJapTS9vOMuR12ZBhVCCLzkmxiJRGFBcIT8gqQie8VXYGmSH2SDM9zQgtAoDPp1BLYdKL3QpokK"
echo ""

echo "5. formulacdmx (Formula CDMX)"
echo "   wrangler secret put FB_TOKEN_FORMULACDMX --name news-api"
echo "   Token: EAAmv1Puxa7wBQzgcpCloTFckjHW8iMBCrRPkiZAI1JJZCHs3lFuWIOowgrRZBMyyZCpygbxeyntI4gUOKZBRjxajhrN6ZBM9MUjuSRsYjS6yvvehtkFWmLNDCdMngdWJjpEOOluyuvdX2w8ae6JYdmiIZA16Pz5BunZAu9x0HGj18nQn53xiShOW8KiVZCjsWIz0s7lBZBWgE03KMiZC4iYHRHZBCZCcZA"
echo ""

echo "6. enfoquecapital (Enfoque capital)"
echo "   wrangler secret put FB_TOKEN_ENFOQUECAPITAL --name news-api"
echo "   Token: EAAmv1Puxa7wBQ7LjrdPqWTewrCsr6zVJCdTuvYbcrXct6zZB2cKEWBxR9XBXFNLsr6x8s3vzumQW4DW5PtffgjrsUShwxYNE3C2KfWEwZCZCXmH2PSAPDbejSJisIkSjubHg9DVCZAYKoEjjzs5uDGjGZBEy0SYIX7elRIIRFVdw2kGdfDMbae8z8YZBq6PaLooTEmEaVojxPWFNsLlXL9fJJ5"
echo ""

echo "7. boominformativo (Boom Informativo)"
echo "   wrangler secret put FB_TOKEN_BOOMINFORMATIVO --name news-api"
echo "   Token: EAAmv1Puxa7wBQwU6SAoc0xuYNMyYHKrybgFzSSu28sWjpZAEI8hI5AQkBZCoUBt6ZBbLVcZCQSDERbErwUxo1ph9VHpet4P5QZA4krS5XIrsxsOjuTRLx1nSZCjNZCg5DOsHV7XQHrZAZC3Kh2d3uAgpl3mWAGXcHijdkIpHVt8Li8NOjCJX6nTAf1ZBsjO3Gdu1Ax8xxuZAvrZB2zogBkt3HcnMuCH8"
echo ""

echo "8. puntoclave (Punto Clave)"
echo "   wrangler secret put FB_TOKEN_PUNTOCLAVE --name news-api"
echo "   Token: EAAmv1Puxa7wBQ5N9Q4ltG5BAHzLSLViwD9iykOe5tAp5GZCijhfGzeaT6hi9BhfOFesZB1SB7FdhcaPMsfYyrx0lWM4fpcFdAJde6KDtSZCVjStVCDuZAYA7iv1leZC7NzcLHlNaPUZBmGkaoFn9OAZBYmeI5xcnVGyepyJpIMKYNUMYbgdcbOERZAjOlfLu40CdyCp4eOYgzYu2Os8S2LGGBIO0"
echo ""

echo "=========================================="
echo "Sitios sin página encontrada (necesitas generar los tokens manualmente):"
echo "=========================================="
echo "- diarioexpress (FB_TOKEN_DIARIOEXPRESS)"
echo "- elpulsomexicano (FB_TOKEN_ELPULSOMEXICANO)"
echo "- enfoquedirecto (FB_TOKEN_ENFOQUEDIRECTO)"
echo "- mexico360noticias (FB_TOKEN_MEXICO360NOTICIAS)"
echo "- noticiashorizonte (FB_TOKEN_NOTICIASHORIZONTE)"
echo "- pulsodiario (FB_TOKEN_PULSODIARIO)"
echo "- puntonoticias (FB_TOKEN_PUNTONOTICIAS)"
echo "- radarinformativo (FB_TOKEN_RADARINFORMATIVO)"
echo "- reportediario (FB_TOKEN_REPORTEDIARIO)"
echo ""

echo "=========================================="
echo "Instrucciones:"
echo "=========================================="
echo "1. Copia cada comando y ejecútalo en la terminal"
echo "2. Pega el token cuando se solicite"
echo "3. Presiona Enter"
echo ""
echo "Ejemplo:"
echo "  wrangler secret put FB_TOKEN_MEXICANTIMES --name news-api"
echo "  [pega el token y presiona Enter]"
echo ""
