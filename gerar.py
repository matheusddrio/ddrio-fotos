import json,os,io,sys,hashlib
from PIL import Image, ImageOps
FOTOS=os.path.expanduser("~/mnt/DDRio Knowlage Base/03 - Comercial/03.10 - Fichas Mestre de Produto/Fotos")
OUT=os.path.expanduser("~/w1_build/fotos")
cat=json.load(open(os.path.join(FOTOS,"catalogo_mestre_hero.json"),encoding='utf-8'))
it={i['id']:i for i in cat['itens']}
import glob
views={}
for f in sorted(glob.glob(os.path.join(FOTOS,"views","VIEW_*.json"))):
    name=os.path.basename(f)[5:-5]
    if name=="Uso_Interno": continue
    v=json.load(open(f,encoding='utf-8'))
    ids=v.get('itens') or v.get('ids') or []
    if ids and isinstance(ids[0],dict): ids=[x.get('id') for x in ids]
    ids=[i for i in ids if it.get(i,{}).get('apto_publicacao_externa')
         and os.path.exists(os.path.join(FOTOS,"HERO",it[i]['nome_fisico']))]
    views[name]={"titulo":v.get("titulo"),"proposito":v.get("proposito"),
                 "homologada_por":v.get("homologada_por"),"versao_view":v.get("versao"),"itens":ids}
uni=sorted({i for v in views.values() for i in v["itens"]})
print("gerando",len(uni),"derivadas", flush=True)
man={}
for n,i in enumerate(uni,1):
    src=os.path.join(FOTOS,"HERO",it[i]['nome_fisico'])
    dst=os.path.join(OUT,f"{i}.jpg")
    im=Image.open(src); im=ImageOps.exif_transpose(im).convert("RGB")
    w,h=im.size; s=min(1.0,1280/max(w,h))
    im=im.resize((max(1,round(w*s)),max(1,round(h*s))), Image.LANCZOS)
    im.save(dst,"JPEG",quality=82,optimize=True,progressive=True)  # sem EXIF: metadados removidos
    b=open(dst,'rb').read()
    man[i]={"arquivo":f"{i}.jpg","bytes":len(b),
            "sha256":hashlib.sha256(b).hexdigest(),
            "resolucao_px":f"{im.size[0]}x{im.size[1]}",
            "nome_comercial":it[i].get("nome_comercial"),
            "valor_estrategico":it[i].get("valor_estrategico"),
            "promessa_visual":it[i].get("promessa_visual")}
    if n%10==0: print(" ",n,"/",len(uni),flush=True)
json.dump({"ativos":man,"galerias":views},open(os.path.expanduser("~/w1_build/_dados.json"),"w",encoding='utf-8'),ensure_ascii=False,indent=1)
print("PRONTO", sum(m["bytes"] for m in man.values())//1024, "KB total", flush=True)
