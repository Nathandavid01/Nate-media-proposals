#!/bin/bash
# ============================================================
# NATE MEDIA — GENERADOR DE PROPUESTAS
# Uso: ./generar_propuesta.sh
# ============================================================

TEMPLATE="/Users/torres/NateMedia/propuesta.html"
WORKING="/Users/torres/NateMedia/propuesta_activa.html"
OUTPUT_DIR="/Users/torres/Documents/Propuestas_NateMedia"

mkdir -p "$OUTPUT_DIR"

# Copy template to working file
cp "$TEMPLATE" "$WORKING"

# ---- CLIENT DATA (passed as arguments or prompted) ----
CLIENT_NAME="${1:-}"
BUSINESS_NAME="${2:-}"
CITY="${3:-}"
INDUSTRY="${4:-}"
PAIN="${5:-}"
TIER="${6:-crecimiento}"
CLIENT_EMAIL="${7:-}"

# Prompt if not passed as arguments
if [ -z "$CLIENT_NAME" ]; then
  read -p "Nombre del cliente: " CLIENT_NAME
fi
if [ -z "$BUSINESS_NAME" ]; then
  read -p "Nombre del negocio: " BUSINESS_NAME
fi
if [ -z "$CITY" ]; then
  read -p "Ciudad: " CITY
fi
if [ -z "$INDUSTRY" ]; then
  echo "Industria (automotive/restaurant/food/realestate/airbnb/retail/medical/pharmacy/renovation/sports):"
  read -p "> " INDUSTRY
fi
if [ -z "$PAIN" ]; then
  read -p "Dolor específico del cliente: " PAIN
fi
if [ -z "$TIER" ]; then
  echo "Tier recomendado (lanzamiento/crecimiento/autoridad):"
  read -p "> " TIER
fi
if [ -z "$CLIENT_EMAIL" ]; then
  read -p "Email del cliente (Enter para omitir): " CLIENT_EMAIL
fi

DATE=$(date "+%B %d, %Y")
FILENAME="Propuesta_${CLIENT_NAME// /_}_${BUSINESS_NAME// /_}.pdf"
OUTPUT="$OUTPUT_DIR/$FILENAME"

echo ""
echo "⚡ Generando propuesta para $CLIENT_NAME — $BUSINESS_NAME..."

# ---- REPLACE PLACEHOLDERS ----
sed -i '' "s|\[NOMBRE DEL CLIENTE\]|$CLIENT_NAME|g" "$WORKING"
sed -i '' "s|\[NOMBRE DEL NEGOCIO\]|$BUSINESS_NAME|g" "$WORKING"
sed -i '' "s|\[CIUDAD\]|$CITY|g" "$WORKING"
sed -i '' "s|\[INDUSTRIA\]|$INDUSTRY|g" "$WORKING"
sed -i '' "s|\[FECHA\]|$DATE|g" "$WORKING"
sed -i '' "s|\[DOLOR ESPECÍFICO DEL CLIENTE.*\]|$PAIN|g" "$WORKING"

# ---- ACTIVATE CASE STUDY ----
sed -i '' "s|showCaseStudy('cs-restaurant')|showCaseStudy('cs-$INDUSTRY')|g" "$WORKING"

# ---- SET RECOMMENDED TIER ----
case "$TIER" in
  lanzamiento)
    sed -i '' '0,/class="tier-card"/{s/class="tier-card"/class="tier-card recommended"/}' "$WORKING"
    ;;
  autoridad)
    sed -i '' 's/class="tier-card" style/class="tier-card recommended" style/g' "$WORKING"
    ;;
  *)
    # crecimiento is already recommended by default
    ;;
esac

# ---- SERVE & GENERATE PDF ----
if ! lsof -i :8080 > /dev/null 2>&1; then
  cd /Users/torres/NateMedia && python3 -m http.server 8080 &>/dev/null &
  sleep 2
fi

# Generate PDF with Chrome headless
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless \
  --disable-gpu \
  --no-sandbox \
  --print-to-pdf="$OUTPUT" \
  --print-to-pdf-no-header \
  "http://localhost:8080/propuesta_activa.html" 2>/dev/null

echo ""
echo "✅ Propuesta lista: $FILENAME"
echo "📁 Guardada en: $OUTPUT_DIR"

# ---- SEND EMAIL VIA MAIL.APP ----
if [ -n "$CLIENT_EMAIL" ]; then
  echo "📧 Enviando a $CLIENT_EMAIL..."
  SEND_TO="$CLIENT_EMAIL"
else
  echo "📧 Enviando a tu correo..."
  SEND_TO="Nathantorres@natemediapr.com"
fi

osascript <<EOF
tell application "Mail"
    set theMessage to make new outgoing message with properties {¬
        subject:"Propuesta Estratégica — $BUSINESS_NAME | Nate Media", ¬
        content:"Hola $CLIENT_NAME,

Adjunto encontrarás la propuesta estratégica personalizada que preparamos para $BUSINESS_NAME.

Quedo disponible para cualquier pregunta.

Nathan D. Torres Soto
CEO & Founder — Nate Media
939-292-3934
Nathantorres@natemediapr.com", ¬
        visible:false}
    tell theMessage
        make new to recipient with properties {address:"$SEND_TO"}
        make new attachment with properties {file name:POSIX file "$OUTPUT"}
    end tell
    send theMessage
end tell
EOF

echo "✅ Email enviado a $SEND_TO"
echo ""

# Open PDF
open "$OUTPUT"
