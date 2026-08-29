#!/usr/bin/env python3
# Build the El Vivi & Arecibo Lab proposal from the Nate Media template.
# Uso: python3 scripts/build_elvivi.py <precio1> <precio2> <precio3> [tier_recomendado]
# Ej:  python3 scripts/build_elvivi.py 750 900 1200 crecimiento
import sys, re, pathlib

SRC = pathlib.Path("/home/user/Nate-media-proposals/propuesta.html")
DST = pathlib.Path("/home/user/Nate-media-proposals/propuesta_ElVivi_AreciboLab.html")

# ---- CLIENT DATA -------------------------------------------------
CLIENTS   = "Heriberto Morales &amp; Kareni Pérez"
BUSINESS  = "El Vivi &amp; Arecibo Lab"
CITY      = "Arecibo y Utuado"
DATE      = "29 de agosto de 2026"
CASE      = "cs-medical"
# Prices (per month, covers BOTH accounts)
P1, P2, P3 = sys.argv[1], sys.argv[2], sys.argv[3]
RECOMMENDED = sys.argv[4] if len(sys.argv) > 4 else "crecimiento"

h = SRC.read_text(encoding="utf-8")

def sub(old, new, count=0):
    """Replace, asserting the anchor actually existed."""
    global h
    if old not in h:
        raise SystemExit("ANCHOR NOT FOUND:\n" + old[:200])
    h = h.replace(old, new) if count == 0 else h.replace(old, new, count)

def region(start, end, new):
    """Replace everything from `start` up to (not including) `end`."""
    global h
    i = h.index(start); j = h.index(end, i)
    h = h[:i] + new + h[j:]

# ---- 1. PLACEHOLDERS ---------------------------------------------
sub("[NOMBRE DEL CLIENTE]", CLIENTS)
sub("[NOMBRE DEL NEGOCIO]", BUSINESS)
sub("[CIUDAD]", CITY)
sub("[FECHA]", DATE)
sub("Caso de Éxito — [INDUSTRIA]", "Caso de Éxito — Salud")

# Cover subtitle reads better with the labs spelled out
sub('<div class="cover-business">El Vivi &amp; Arecibo Lab · Arecibo y Utuado, Puerto Rico</div>',
    '<div class="cover-business">Laboratorios Clínicos El Vivi &amp; Arecibo Lab<br>Arecibo y Utuado, Puerto Rico</div>')

# ---- 2. VOICE: tú -> ustedes (two owners, two labs) --------------
V = [
 ('"La mayoría de agencias te venden <span class="gold">posts.</span><br>',
  '"La mayoría de agencias les venden <span class="gold">posts.</span><br>'),
 ('Nosotros te vendemos <span class="gold">clientes nuevos.</span>"',
  'Nosotros les vendemos <span class="gold">pacientes nuevos.</span>"'),
 ('para negocios como el tuyo — sin depender', 'para negocios como los de ustedes — sin depender'),
 ('<div class="section-label">Personalizado para ti</div>',
  '<div class="section-label">Personalizado para ustedes</div>'),
 ('Lo que escuchamos<br><span class="gold">de ti.</span>',
  'Lo que escuchamos<br><span class="gold">de ustedes.</span>'),
 ('<strong>pensada para tu industria y tu mercado.</strong>',
  '<strong>pensada para su industria y su mercado.</strong>'),
 ('<span class="red">Nadie te ve.</span><br>Nadie te compra.',
  '<span class="red">Nadie los ve.</span><br>Nadie los visita.'),
 ('Si no te ven a ti, van a ver a tu competencia. Y una vez que se vuelven leales a tu competencia, ya los perdiste.',
  'Si no los ven a ustedes, van a ver a su competencia. Y una vez que un paciente se vuelve leal a otro laboratorio, ya lo perdieron.'),
 ('Es pérdida de dinero directa para tu negocio.', 'Es pérdida de dinero directa para sus laboratorios.'),
 ('El problema<br><span class="red">no eres tú.</span>', 'El problema<br><span class="red">no son ustedes.</span>'),
 ('<strong>Comunicación directa</strong> — Tienes acceso a Nathan y su equipo, siempre. Sin intermediarios.',
  '<strong>Comunicación directa</strong> — Tienen acceso a Nathan y su equipo, siempre. Sin intermediarios.'),
 ('No en 6 meses. Verás movimiento desde el primer mes.', 'No en 6 meses. Verán movimiento desde el primer mes.'),
 ('<strong>Vamos a ti</strong> — Siempre vamos a tu negocio. Tú no tienes que ir a ningún lado.',
  '<strong>Vamos a ustedes</strong> — Grabamos en Arecibo y en Utuado. Ustedes no tienen que ir a ningún lado.'),
 ('<strong>Tú solo apareces</strong>', '<strong>Ustedes solo aparecen</strong>'),
 ('<span style="color: var(--gold); font-weight: 800;">Somos tu equipo de marketing.</span>',
  '<span style="color: var(--gold); font-weight: 800;">Somos su equipo de marketing.</span>'),
 ('Las personas detrás<br><span class="gold">de tu crecimiento.</span>',
  'Las personas detrás<br><span class="gold">de su crecimiento.</span>'),
 ('<strong>El mismo equipo. La misma dedicación. Disponible para tu negocio.</strong>',
  '<strong>El mismo equipo. La misma dedicación. Disponible para ambos laboratorios.</strong>'),
 ('Resultados reales.<br><span class="gold">Negocio como el tuyo.</span>',
  'Resultados reales.<br><span class="gold">Un negocio como el de ustedes.</span>'),
 ('<p>Conocemos tu negocio a fondo — tu visión, tu cliente ideal, tu competencia y lo que te hace único.</p>',
  '<p>Conocemos ambos laboratorios a fondo — su visión, su paciente ideal, su competencia y lo que los hace únicos.</p>'),
 ('<p>Investigamos tu industria, tu competencia y las palabras clave que tu cliente usa para encontrarte en Google, Facebook e Instagram.</p>',
  '<p>Investigamos su industria, su competencia y las palabras clave que sus pacientes usan para encontrarlos en Google, Facebook e Instagram.</p>'),
 ('<p>Creamos tu plan de contenido personalizado', '<p>Creamos un plan de contenido para cada laboratorio'),
 ('<p>Vamos a tu local. Filmamos. Tú solo apareces — nosotros nos encargamos de todo lo demás.</p>',
  '<p>Vamos a sus laboratorios. Filmamos. Ustedes solo aparecen — nosotros nos encargamos de todo lo demás.</p>'),
 ('Todo esto está<br><span class="gold">incluido en tu plan.</span>',
  'Todo esto está<br><span class="gold">incluido en su plan.</span>'),
 ('<div class="service-item">Grabación en tu negocio</div>',
  '<div class="service-item">Grabación en ambos laboratorios</div>'),
 ('Contamos con un equipo de 5 personas dedicadas a tu cuenta.<br>',
  'Contamos con un equipo de 5 personas dedicadas a sus dos cuentas.<br>'),
 ('Elige tu nivel<br><span class="gold">de crecimiento.</span>',
  'Elijan su nivel<br><span class="gold">de crecimiento.</span>'),
 ('negocios en Puerto Rico — negocios como el tuyo.<br>',
  'negocios en Puerto Rico — negocios como los de ustedes.<br>'),
 ('Lo hicimos para ellos. Podemos hacerlo para ti.', 'Lo hicimos para ellos. Podemos hacerlo para ustedes.'),
 ('<p><strong>Selecciona tu plan</strong> — Lanzamiento, Crecimiento o Autoridad</p>',
  '<p><strong>Seleccionen su plan</strong> — Lanzamiento, Crecimiento o Autoridad</p>'),
 ('<p><strong>Llama a Nathan</strong> para confirmar tu selección e iniciar el proceso</p>',
  '<p><strong>Llamen a Nathan</strong> para confirmar su selección e iniciar el proceso</p>'),
 ('<p><strong>Onboarding</strong> — Nos sumergimos en tu negocio, tu visión y tus metas</p>',
  '<p><strong>Onboarding</strong> — Nos sumergimos en ambos laboratorios, su visión y sus metas</p>'),
 ('<p><strong>Agendamos tu primera grabación</strong> — vamos a tu negocio</p>',
  '<p><strong>Agendamos su primera grabación</strong> — vamos a Arecibo y a Utuado</p>'),
 ('<p><strong>Comenzamos a crear clientes nuevos</strong> para tu negocio</p>',
  '<p><strong>Comenzamos a atraer pacientes nuevos</strong> para ambos laboratorios</p>'),
 ('<div class="contact-sign-off">Espero tu llamada,</div>',
  '<div class="contact-sign-off">Espero su llamada,</div>'),
]
for old, new in V:
    sub(old, new)

# ---- 2b. CSS for per-account pricing lines -----------------------
sub("</style>", """.tier-per-account {
  text-align: center;
  font-size: 7.5pt;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  color: rgba(255,255,255,0.45);
  margin-top: 2px;
}
.tier-total {
  text-align: center;
  font-size: 8.5pt;
  color: rgba(255,255,255,0.7);
  margin-top: 0.05in;
}
.tier-total strong { color: var(--gold); font-weight: 800; }
</style>""")

# ---- 3. "LO QUE ESCUCHAMOS" — their actual words ------------------
sub('queremos que sepas que escuchamos con atención.', 'queremos que sepan que escuchamos con atención.')
sub('Esto es lo que nos compartiste sobre', 'Esto es lo que nos compartieron sobre')

region('    <ul class="heard-list">', '    </ul>', '''    <ul class="heard-list">
      <li><span class="heard-icon">🎯</span><span>No tienen visibilidad digital — la gente de <strong>Arecibo y Utuado</strong> no sabe que ustedes existen ni qué servicios ofrecen.</span></li>
      <li><span class="heard-icon">⚔️</span><span>Compiten en un mercado saturado — <strong>muchos laboratorios clínicos</strong> en la misma región peleando por el mismo paciente.</span></li>
      <li><span class="heard-icon">🏥</span><span>Son <strong>dos laboratorios con dos audiencias distintas</strong> — El Vivi y Arecibo Lab necesitan presencia propia, no un mensaje genérico.</span></li>
      <li><span class="heard-icon">⚡</span><span>Quieren resultados medibles — pacientes entrando por la puerta diciendo <em>"los vi en redes"</em>, no solo likes.</span></li>
''')

sub('Cada número, cada caso de estudio, cada estrategia — <strong>pensada para su industria y su mercado.</strong>',
    'Cada número, cada caso de estudio, cada estrategia — <strong>pensada para laboratorios clínicos en su región.</strong>')

# ---- 4. PAIN BOX -------------------------------------------------
sub('<p>[DOLOR ESPECÍFICO DEL CLIENTE — ej: "Actualmente [NEGOCIO] está publicando solo gráficas sin estrategia y no está convirtiendo seguidores en clientes."]</p>',
    '<p>Hoy, cuando alguien en Arecibo o Utuado necesita hacerse un laboratorio, <strong>no piensa en El Vivi ni en Arecibo Lab</strong> — porque no los ve en ningún lado. Mientras tanto, la competencia en la región sí está frente a ese paciente todos los días.</p>')

# ---- 5. CASE STUDY: activate medical in the markup (not just JS) --
sub('<div class="case-study" id="cs-medical">', '<div class="case-study active" id="cs-medical">')
sub("showCaseStudy('cs-restaurant');", "showCaseStudy('%s');" % CASE)
sub('// Default: show restaurant on load (change as needed)', '// Default for this proposal: medical / clinical lab')

# ---- 6. TIERS: per-account deliverables, Meta Ads in, no setup fee -
def card(name, tagline, price, reels, monthly, rec):
    cls = "tier-card recommended" if rec else "tier-card"
    badge = '\n        <div class="tier-recommended-badge">⭐ Recomendado</div>' if rec else ''
    return f'''      <div class="{cls}">{badge}
        <div class="tier-header">
          <span class="tier-name">{name}</span>
          <span class="tier-tagline">{tagline}</span>
        </div>
        <div class="tier-body">
          <div class="tier-price">${int(price):,}<span class="per">/mes</span></div>
          <div class="tier-per-account">por laboratorio</div>
          <div class="tier-total">Los dos: <strong>${int(price)*2:,}/mes</strong></div>
          <div class="tier-divider"></div>
          <ul class="tier-features">
            <li><strong>{reels}</strong></li>
            <li><strong>2 Artes semanales</strong> por cuenta</li>
            <li>{monthly}</li>
            <li>Publicación en FB, IG y TikTok</li>
            <li>Optimización de perfiles (SEO)</li>
            <li>Estrategia por laboratorio</li>
            <li><strong>Meta Ads incluido</strong></li>
            <li>Holiday content</li>
            <li>Onboarding sin costo</li>
          </ul>
          <div class="tier-commitment">Compromiso: 3-6 meses</div>
        </div>
      </div>'''

tiers = "\n\n".join([
    card("Lanzamiento", "Para poner ambos labs en el mapa", P1,
         "1 Reel semanal por cuenta", "8 Reels + 16 artes al mes en total", RECOMMENDED == "lanzamiento"),
    card("Crecimiento", "Para ganar terreno en la región", P2,
         "2 Reels semanales por cuenta", "16 Reels + 16 artes al mes en total", RECOMMENDED == "crecimiento"),
    card("Autoridad", "Para dominar el mercado del área", P3,
         "3 Reels semanales por cuenta", "24 Reels + 16 artes al mes en total", RECOMMENDED == "autoridad"),
])

region('    <div class="tiers-grid">', '<!-- ============================================================\n  PAGE 11:', f'''    <div class="tiers-grid">

{tiers}

    </div>

    <!-- TWO ACCOUNTS + NO SETUP FEE -->
    <div style="margin-top: 0.18in; background: rgba(255,191,0,0.07); border: 1px solid rgba(255,191,0,0.25); border-radius: 8px; padding: 0.18in 0.25in; display: flex; justify-content: space-between; align-items: center;">
      <div>
        <div style="font-size: 8pt; font-weight: 700; text-transform: uppercase; letter-spacing: 2px; color: var(--gold); margin-bottom: 4px;">El precio es por laboratorio</div>
        <div style="font-size: 9.5pt; color: rgba(255,255,255,0.7); line-height: 1.5;">Cada laboratorio se factura por separado a la tarifa de su plan. <strong style="color:#fff;">El Vivi y Arecibo Lab</strong> reciben contenido, estrategia y publicación independientes — no se comparte ni se recicla contenido entre cuentas. Meta Ads incluido en los tres planes.</div>
      </div>
      <div style="text-align: center; flex-shrink: 0; margin-left: 0.25in;">
        <div style="font-size: 22pt; font-weight: 900; color: var(--gold); line-height: 1;">$0</div>
        <div style="font-size: 7.5pt; color: rgba(255,255,255,0.4); text-transform: uppercase; letter-spacing: 1px;">Iniciación</div>
      </div>
    </div>

  </div>
  <div class="page-footer" style="border-top-color: rgba(255,255,255,0.1);">
    <span class="footer-brand">Nate Media</span>
    <span class="footer-confidential" style="color: rgba(255,255,255,0.2);">Confidencial</span>
  </div>
</div>


''')

# ---- 7. META ADS: now included, not a $400 add-on -----------------
region('<!-- ============================================================\n  PAGE 11:',
       '<!-- ============================================================\n  PAGE 12:',
'''<!-- ============================================================
  PAGE 11: META ADS (INCLUDED)
  ============================================================ -->
<div class="page">
  <div class="page-header">
    <img src="logo.jpg" alt="Nate Media">
    <span class="header-client">El Vivi &amp; Arecibo Lab</span>
  </div>
  <div class="page-content">
    <div class="section-label">Incluido en su plan</div>
    <h2 class="page-title">Meta Ads,<br><span class="gold">sin costo adicional.</span></h2>
    <div class="gold-bar"></div>
    <p class="body-text">La mayoría de agencias cobran el manejo de Meta Ads aparte. Nosotros lo incluimos en los tres planes — porque en un mercado con tanta competencia como el de Arecibo y Utuado, el orgánico solo no alcanza para ganar terreno rápido.</p>

    <div class="addon-box">
      <div class="addon-price-circle">
        <span class="addon-price-num">$0</span>
        <span class="addon-price-label">Incluido</span>
      </div>
      <div class="addon-text">
        <h3>Manejo de Meta Ads — incluido</h3>
        <p>Estrategia, creación, optimización y seguimiento de campañas en Facebook e Instagram para <strong>ambos laboratorios</strong>. El presupuesto publicitario es inversión directa de ustedes y se paga a Meta — nosotros no cobramos por manejarlo.</p>
      </div>
    </div>

    <div class="divider"></div>

    <ul class="checklist">
      <li><span class="icon">✅</span><span><strong>Orgánico primero</strong> — Solo escalamos con ads el contenido que ya demostró funcionar</span></li>
      <li><span class="icon">✅</span><span><strong>Cada dólar cuenta</strong> — No quemamos presupuesto probando — ya tenemos los datos</span></li>
      <li><span class="icon">✅</span><span><strong>Segmentación por pueblo</strong> — Campañas separadas para Arecibo y para Utuado, cada una a su propia audiencia</span></li>
      <li><span class="icon">✅</span><span><strong>Audiencia probada</strong> — El contenido orgánico nos dice exactamente a quién targetear</span></li>
    </ul>

    <p class="body-text" style="margin-top: 0.15in; font-size: 9pt; color: var(--gray);">
      El presupuesto de Meta Ads es inversión directa del cliente y no está incluido en la tarifa mensual. Recomendamos comenzar con $150-$300 al mes por laboratorio.
    </p>
  </div>
  <div class="page-footer">
    <span class="footer-brand">Nate Media</span>
    <span class="footer-confidential">Confidencial</span>
  </div>
</div>


''')

# ---- 8. SERVICES PAGE: reflect the two-account structure ----------
sub('''      <strong>Lo único que cambia entre planes es el volumen de contenido semanal.</strong><br>
      Todos los servicios aplican a todos los planes.''',
    '''      <strong>Lo único que cambia entre planes es el volumen de Reels por cuenta.</strong><br>
      Todos los servicios aplican a los tres planes — y a los dos laboratorios.''')

sub('<div class="service-item">Promoción pagada (Meta Ads)</div>',
    '<div class="service-item">Meta Ads incluido</div>')
sub('<div class="service-item">Colaboración entre cuentas</div>',
    '<div class="service-item">Colaboración El Vivi ↔ Arecibo Lab</div>')

# ---- 9. Clean the template's customization comment ---------------
region('<!-- ============================================================\n  ⚡ CUSTOMIZATION VARIABLES',
       '<!-- ============================================================\n  PAGE 1: COVER',
'''<!-- ============================================================
  PROPUESTA — El Vivi & Arecibo Lab
  Heriberto Morales & Kareni Pérez · Arecibo y Utuado
  Generada desde propuesta.html — no editar a mano;
  regenerar con scripts/build_elvivi.py
  ============================================================ -->


''')

# ---- 10. Second-person misses (capitalized / enclitic) -----------
sub('Antes de presentarte nuestra propuesta', 'Antes de presentarles nuestra propuesta')
sub('Tu cliente ideal está ahí — desplazándose por su feed, buscando exactamente lo que tú ofreces.',
    'Su paciente ideal está ahí — desplazándose por su feed, buscando exactamente lo que ustedes ofrecen.')
sub('<h3>Grabación en Tu Negocio</h3>', '<h3>Grabación en Sus Laboratorios</h3>')


DST.write_text(h, encoding="utf-8")
leftovers = re.findall(r'\[[A-ZÁÉÍÓÚÑ][^\]]*\]', h)
print("Escrito:", DST)
print("Placeholders sin resolver:", leftovers if leftovers else "ninguno")
