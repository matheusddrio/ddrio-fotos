import json,os,html
from PIL import Image
D=json.load(open("_dados.json",encoding='utf-8'))
G=json.load(open("galerias.json",encoding='utf-8'))
for i in D["ativos"]:
    t=f"thumbs/{i}.jpg"
    if os.path.exists(t): continue
    im=Image.open(f"fotos/{i}.jpg"); w,h=im.size; s=420/max(w,h)
    im.resize((round(w*s),round(h*s)),Image.LANCZOS).save(t,"JPEG",quality=72,optimize=True,progressive=True)

gal=G["galerias"]
ORDEM=["Open_Sunset_Panorama","Open_Sunset_Casal","Private_Sunset_Casal","Servico_de_Bordo","Morning",
       "Embarcacoes","Familia_Crianca","Casal_Homoafetivo","Despedida_Veleiro","Despedida_Traineira",
       "Lancha_Perola","Hospitalidade","Operacional_Chegada","Institucional"]
ordem=[g for g in ORDEM if g in gal]+[g for g in gal if g not in ORDEM]

def card(f, destaque=False):
    foco=f.get("foco_principal")
    frase=f.get("frase") or ""
    rascunho = "rascunho" in (f.get("frase_origem") or "")
    tags="".join(f'<em>{html.escape(t)}</em>' for t in (f.get("mostra") or [])[:4])
    top=f'<span class="foco">{html.escape(foco)}</span>' if foco else ''
    fr=f'<p class="frase{" rasc" if rascunho and destaque else ""}">{html.escape(frase)}</p>' if frase else ''
    return f'''<figure class="{'big' if destaque else ''}">{top}
<a href="fotos/{f["id"]}.jpg" target="_blank" rel="noopener"><img src="thumbs/{f["id"]}.jpg" loading="lazy" alt=""></a>
<figcaption><span class="v v{f.get("valor") or "C"}">{f.get("valor") or "-"}</span>
<b>{html.escape(f.get("nome") or "")}</b><code>{f["id"][-5:]}</code></figcaption>
{fr}<div class="tags">{tags}</div></figure>'''

secs=[];nav=""
for g in ordem:
    v=gal[g]; lib=v.get("liberada_para_agente") is True
    prop = g=="Open_Sunset_Panorama"
    badge=('<span class="b live">no ar</span>' if lib else
           ('<span class="b prop">proposta · aguarda você</span>' if prop else '<span class="b pend">pendente de curadoria</span>'))
    nav+=f'<a href="#{g}">{html.escape(v["titulo"] or g)} <b>{len(v["fotos"])}</b></a>'
    cards="".join(card(f,prop) for f in v["fotos"])
    secs.append(f'''<section id="{g}" class="{'destaque' if prop else ''}">
<h2>{html.escape(v["titulo"] or g)} {badge}<span class="n">{len(v["fotos"])} fotos</span></h2>
<p class="prop">{html.escape(v.get("proposito") or "")}</p>
<div class="grid{' g2' if prop else ''}">{cards}</div></section>''')

page=f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex">
<title>DDRio · Patrimônio Visual para atendimento</title><style>
*{{box-sizing:border-box}}
body{{margin:0;background:#0f1216;color:#e8e6e3;font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}}
header{{padding:34px 22px 18px;border-bottom:1px solid #232a32}}
h1{{margin:0 0 6px;font-size:22px;letter-spacing:-.02em}}
header p{{margin:0;color:#8b96a3;font-size:14px;max-width:66ch}}
nav{{position:sticky;top:0;z-index:9;background:#141920ee;backdrop-filter:blur(8px);
border-bottom:1px solid #232a32;padding:10px 16px;display:flex;gap:6px;flex-wrap:wrap}}
nav a{{color:#b9c4d0;text-decoration:none;font-size:13px;padding:5px 10px;border-radius:999px;border:1px solid #2a323c;white-space:nowrap}}
nav a:hover{{background:#1d242d;color:#fff}} nav a b{{color:#6f7c8a;font-weight:600;margin-left:3px}}
section{{padding:30px 22px;border-bottom:1px solid #1c2229;scroll-margin-top:56px}}
section.destaque{{background:#12181f;border-left:3px solid #c9a227}}
h2{{margin:0 0 6px;font-size:19px;display:flex;align-items:center;gap:10px;flex-wrap:wrap}}
.n{{font-size:12px;color:#6f7c8a;font-weight:400}}
.b{{font-size:11px;font-weight:700;padding:2px 8px;border-radius:999px;letter-spacing:.02em}}
.b.live{{background:#1e4620;color:#8ce99a}} .b.prop{{background:#c9a227;color:#1a1408}} .b.pend{{background:#2a323c;color:#8b96a3}}
.prop{{margin:0 0 18px;color:#8b96a3;font-size:13px;max-width:80ch}}
.grid{{display:grid;gap:14px;grid-template-columns:repeat(auto-fill,minmax(190px,1fr))}}
.grid.g2{{grid-template-columns:repeat(auto-fill,minmax(255px,1fr));gap:20px}}
figure{{margin:0}} figure img{{width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:8px;display:block;background:#1b2129}}
figure.big img{{aspect-ratio:3/2}}
.foco{{display:inline-block;font-size:11px;font-weight:700;letter-spacing:.04em;text-transform:uppercase;
color:#c9a227;margin-bottom:5px}}
figcaption{{margin-top:6px;font-size:12px;color:#9aa5b1;display:flex;gap:6px;align-items:baseline}}
figcaption b{{font-weight:500;color:#cdd6df;flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}
figcaption code{{color:#5d6874;font-size:11px}}
.frase{{margin:6px 0 0;font-size:13.5px;color:#dfe6ed;line-height:1.45}}
.frase.rasc{{border-left:2px solid #c9a22766;padding-left:9px}}
.tags{{margin-top:6px;display:flex;gap:4px;flex-wrap:wrap}}
.tags em{{font-style:normal;font-size:10.5px;color:#7d8794;background:#1b2129;border:1px solid #262e38;padding:1px 6px;border-radius:4px}}
.v{{font-size:10px;font-weight:700;padding:1px 5px;border-radius:3px;background:#2a323c;color:#8b96a3}}
.vS{{background:#c9a227;color:#1a1408}} .vA{{background:#3c5a78;color:#dceaf7}}
footer{{padding:26px 22px 60px;color:#6f7c8a;font-size:12.5px;max-width:74ch}} footer code{{color:#8b96a3}}
</style></head><body>
<header><h1>DDRio · Patrimônio Visual para atendimento</h1>
<p>{len(D["ativos"])} fotografias. A <b style="color:#c9a227">Open Sunset — Panorama</b> é uma proposta:
um pico do passeio por foto, mais uma amostra de quem vai a bordo. As frases em destaque são rascunho —
espaço reservado para as suas palavras. Clique numa imagem para ver o arquivo que a Iris envia.</p></header>
<nav>{nav}</nav>
{"".join(secs)}
<footer><p><b>Isto não é o acervo.</b> A fonte da verdade é o <code>catalogo_mestre_hero.json</code> na
Knowledge Base, sob <code>03.10-Z0</code> e <code>03.10-Z1</code>. Estas são derivadas técnicas —
1280&nbsp;px, JPEG q82, EXIF removido — que não substituem o original.</p>
<p>Só entram ativos com <code>apto_publicacao_externa = true</code>. A View <code>Uso_Interno</code> não está aqui.</p>
<p>O rótulo em maiúsculas sobre cada foto do Panorama é o <b>foco</b>: o que ela prova. É por ele que a Iris
pede uma imagem pontual no meio da conversa. Uso pelo agente: <code>CCE-2026-003</code>, Linha 13.</p></footer>
</body></html>'''
open("index.html","w",encoding='utf-8').write(page)
print("vitrine ok |",len(ordem),"galerias |",len(D["ativos"]),"ativos")
