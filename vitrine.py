import json,os,html
from PIL import Image
D=json.load(open("_dados.json",encoding='utf-8'))
G=json.load(open("galerias.json",encoding='utf-8'))
# thumbs 420px
for i in D["ativos"]:
    d=f"thumbs/{i}.jpg"
    if os.path.exists(d): continue
    im=Image.open(f"fotos/{i}.jpg"); w,h=im.size; s=420/max(w,h)
    im.resize((round(w*s),round(h*s)),Image.LANCZOS).save(d,"JPEG",quality=72,optimize=True,progressive=True)
ORDEM=["Open_Sunset_Casal","Private_Sunset_Casal","Servico_de_Bordo","Morning","Embarcacoes",
       "Familia_Crianca","Casal_Homoafetivo","Despedida_Veleiro","Despedida_Traineira",
       "Lancha_Perola","Hospitalidade","Operacional_Chegada","Institucional"]
gal=G["galerias"]; ordem=[g for g in ORDEM if g in gal]+[g for g in gal if g not in ORDEM]
nav="".join(f'<a href="#{g}">{html.escape(gal[g]["titulo"] or g)} <b>{len(gal[g]["fotos"])}</b></a>' for g in ordem)
secs=[]
for g in ordem:
    v=gal[g]
    cards=""
    for f in v["fotos"]:
        m=D["ativos"][f["id"]]
        cards+=f'''<figure><a href="fotos/{f["id"]}.jpg" target="_blank" rel="noopener">
<img src="thumbs/{f["id"]}.jpg" loading="lazy" alt="{html.escape(f["nome"] or "")}"></a>
<figcaption><span class="v v{f["valor"] or "C"}">{f["valor"] or "-"}</span>
<b>{html.escape(f["nome"] or "")}</b><code>{f["id"][-5:]}</code></figcaption></figure>'''
    secs.append(f'''<section id="{g}"><h2>{html.escape(v["titulo"] or g)}
<span class="n">{len(v["fotos"])} fotos</span></h2>
<p class="prop">{html.escape(v["proposito"] or "")}</p>
<div class="grid">{cards}</div></section>''')
page=f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex">
<title>DDRio · Patrimônio Visual para atendimento</title><style>
*{{box-sizing:border-box}}
body{{margin:0;background:#0f1216;color:#e8e6e3;font:16px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}}
header{{padding:34px 22px 18px;border-bottom:1px solid #232a32}}
h1{{margin:0 0 6px;font-size:22px;letter-spacing:-.02em}}
header p{{margin:0;color:#8b96a3;font-size:14px;max-width:62ch}}
nav{{position:sticky;top:0;z-index:9;background:#141920ee;backdrop-filter:blur(8px);
border-bottom:1px solid #232a32;padding:10px 16px;display:flex;gap:6px;flex-wrap:wrap}}
nav a{{color:#b9c4d0;text-decoration:none;font-size:13px;padding:5px 10px;border-radius:999px;
border:1px solid #2a323c;white-space:nowrap}}
nav a:hover{{background:#1d242d;color:#fff}}
nav a b{{color:#6f7c8a;font-weight:600;margin-left:3px}}
section{{padding:30px 22px;border-bottom:1px solid #1c2229;scroll-margin-top:56px}}
h2{{margin:0 0 4px;font-size:19px;display:flex;align-items:baseline;gap:10px}}
.n{{font-size:12px;color:#6f7c8a;font-weight:400}}
.prop{{margin:0 0 18px;color:#8b96a3;font-size:13px}}
.grid{{display:grid;gap:14px;grid-template-columns:repeat(auto-fill,minmax(190px,1fr))}}
figure{{margin:0}}
figure img{{width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:8px;display:block;background:#1b2129}}
figcaption{{margin-top:6px;font-size:12px;color:#9aa5b1;display:flex;gap:6px;align-items:baseline}}
figcaption b{{font-weight:500;color:#cdd6df;flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}
figcaption code{{color:#5d6874;font-size:11px}}
.v{{font-size:10px;font-weight:700;padding:1px 5px;border-radius:3px;background:#2a323c;color:#8b96a3}}
.vS{{background:#c9a227;color:#1a1408}} .vA{{background:#3c5a78;color:#dceaf7}}
footer{{padding:26px 22px 60px;color:#6f7c8a;font-size:12.5px;max-width:70ch}}
footer code{{color:#8b96a3}}
</style></head><body>
<header><h1>DDRio · Patrimônio Visual para atendimento</h1>
<p>{len(D["ativos"])} fotografias em {len(gal)} galerias homologadas. Clique numa imagem para ver o arquivo
que a Iris envia ao cliente. Selo <span class="v vS">S</span> ícone · <span class="v vA">A</span> principal ·
<span class="v">B/C</span> secundária.</p></header>
<nav>{nav}</nav>
{"".join(secs)}
<footer><p><b>Isto não é o acervo.</b> A fonte da verdade é o <code>catalogo_mestre_hero.json</code>
na Knowledge Base, sob as normas <code>03.10-Z0</code> e <code>03.10-Z1</code>. Estas são derivadas
técnicas — 1280&nbsp;px, JPEG q82, metadados EXIF removidos — que não substituem o original.</p>
<p>Só entram ativos com <code>apto_publicacao_externa = true</code>. A View <code>Uso_Interno</code>
não está aqui, e não deve estar.</p>
<p>Uso pelo agente <code>ATD-2026-001</code>: contrato <code>CCE-2026-003</code>, Linha 13.</p></footer>
</body></html>'''
open("index.html","w",encoding='utf-8').write(page)
print("vitrine gerada |", len(ordem), "galerias | thumbs:", len(os.listdir("thumbs")))
