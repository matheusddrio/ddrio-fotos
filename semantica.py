import json,os,glob
FOTOS=os.path.expanduser("~/mnt/DDRio Knowlage Base/03 - Comercial/03.10 - Fichas Mestre de Produto/Fotos")
cat=json.load(open(os.path.join(FOTOS,"catalogo_mestre_hero.json"),encoding='utf-8'))
it={a['id']:a for a in cat['itens']}
d=json.load(open("_dados.json",encoding='utf-8'))
USER="matheusddrio"; REPO="ddrio-fotos"
base=f"https://raw.githubusercontent.com/{USER}/{REPO}/main/fotos/"

# ---- vocabulario de foco (o que a foto PROVA) ----
VOCAB=["embarque","vela","paisagem","niteroi","banho","servico-de-bordo","tripulacao",
       "por-do-sol","casal","familia","crianca","grupo","celebracao","embarcacao"]

MOM={"antes_embarque":["embarque"],"velejando":["vela"],"mergulho":["banho"],
     "servico_bordo":["servico-de-bordo"],"por_do_sol":["por-do-sol"],
     "paisagem":["paisagem"],"celebracao":["celebracao"],"pedido_casamento":["celebracao","casal"]}
CONF={"casal":["casal"],"familia":["familia"],"criancas":["crianca"],
      "grupo_grande":["grupo"],"3a5":["grupo"],"tripulacao":["tripulacao"],
      "sem_pessoas":["embarcacao"],"solo":["paisagem"]}
CENA={"cais":["embarque"],"mergulho":["banho"],"servico_bordo":["servico-de-bordo"],
      "brinde":["servico-de-bordo","celebracao"],"paisagem":["paisagem"]}
LUZ={"por_do_sol":["por-do-sol"],"golden_hour":["por-do-sol"]}

def tags(i):
    a=it.get(i) or {}
    t=set()
    for src,mapa in ((a.get("momento_experiencia"),MOM),(a.get("configuracao_humana"),CONF),(a.get("luz_periodo"),LUZ)):
        t.update(mapa.get(src,[]))
    for c in (a.get("cena") or []): t.update(CENA.get(c,[]))
    n=(a.get("nome_comercial") or "").lower()+" "+(a.get("promessa_visual") or "").lower()
    if "mac" in n or "niter" in n or "contempor" in n: t.add("niteroi")
    if "marina" in n or "pier" in n or "píer" in n: t.add("embarque")
    return sorted(t & set(VOCAB))

# ---- PANORAMA: 12 posicoes, uma funcao cada ----
PANORAMA=[
 ("00120","embarque",       "É aqui que a gente se encontra: Marina da Glória, Píer A0."),
 ("00069","vela",           "Vela aberta e barco navegando de verdade — não é passeio de motor."),
 ("00027","paisagem",       "Os dois cartões-postais do Rio na mesma foto."),
 ("00042","niteroi",        "E do outro lado da baía tem o MAC de Niterói. Quase ninguém espera por essa."),
 ("00039","banho",          "No meio do passeio a gente para uns 20 minutos para cair na água."),
 ("00064","servico-de-bordo","Espumante, frutas e petiscos servidos a bordo — tudo incluso."),
 ("00140","tripulacao",     "Quem leva o barco é tripulação profissional, e conta a história do caminho."),
 ("00054","por-do-sol",     "E aí o sol cai, e todo mundo fica em silêncio."),
 ("00071","casal",          "A proa é de vocês dois."),
 ("00033","familia",        "A família inteira acomodada, com o Rio do lado."),
 ("00043","crianca",        "Criança a bordo é rotina aqui."),
 ("00063","grupo",          "Brindar com quem você gosta, com o Rio atrás."),
]

g=json.load(open("galerias.json",encoding='utf-8'))

# enriquece TODAS as fotos de todas as galerias com mostra + frase de catalogo
for gal in g["galerias"].values():
    for f in gal["fotos"]:
        a=it.get(f["id"]) or {}
        f["mostra"]=tags(f["id"])
        f.setdefault("frase", a.get("promessa_visual") or "")
        f["frase_origem"]="catalogo (promessa_visual)"

# monta a View proposta
fotos=[]
for suf,foco,frase in PANORAMA:
    i="DDRIO-HERO-"+suf; a=it[i]; m=d["ativos"][i]
    t=sorted(set(tags(i)+[foco]))
    fotos.append({"id":i,"url":base+i+".jpg","nome":a.get("nome_comercial"),
                  "valor":a.get("valor_estrategico"),"foco_principal":foco,
                  "mostra":t,"frase":frase,"frase_origem":"rascunho Claude — aguarda as palavras do Matheus",
                  "produtos":a.get("produtos") or []})
g["galerias"]["Open_Sunset_Panorama"]={
 "titulo":"Open Sunset — Panorama",
 "proposito":"Roteiro visual das 3 horas: um pico por foto, mais uma amostra de quem vai a bordo. Para o cliente que sabe o produto e ainda nao revelou quem e.",
 "homologada_por":"PROPOSTA de 28/08/2026 — aguardando curadoria do fundador",
 "versao":"0.1",
 "liberada_para_agente":False,
 "estado_curadoria":"PROPOSTA - nao enviavel ate aprovacao humana (CCE-2026-003 §10)",
 "legenda":"Open Sunset Tour — Baía de Guanabara, Rio de Janeiro ⛵️",
 "fotos":fotos}

g["controle"]["vocabulario_foco"]=VOCAB
g["controle"]["atualizado_em"]="2026-08-28"
g["controle"]["nota_foco"]="O campo 'mostra' diz o que a foto PROVA. A Iris pode pedir um foco; o codigo filtra dentro da galeria ja liberada. A curadoria continua sendo humana."
json.dump(g,open("galerias.json","w",encoding='utf-8'),ensure_ascii=False,indent=1)

print("Panorama montado com",len(fotos),"fotos")
for f in fotos:
    a1 = "A1" in f["produtos"]
    print(f'  {f["id"][-5:]} {f["foco_principal"]:17s} {"A1 " if a1 else "!! "} {f["nome"][:52]}')
print("\nfocos cobertos:", sorted({f["foco_principal"] for f in fotos}))
