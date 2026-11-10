import pandas as pd, json, glob
d=glob.glob('z1/*/')[0]
RAW='/tmp/claude-0/-home-claude/f2ce5bc5-82e3-548f-b12c-c0022589acee/scratchpad/'
g=pd.read_csv(d+'Base-de-Dados.csv',decimal=',')
s=pd.read_csv(d+'IDH-SEXO.csv',decimal=',')
c=pd.read_csv(d+'IDH-COR.csv',decimal=',')
V=['IDHM','IDHM_L','IDHM_E','IDHM_R','ESPVIDA','T_FREQ5A6','T_FUND11A13','T_FUND15A17','T_MED18A20','T_FUND18M','RDPC','GINI']
def rows(df,grpcol,agg):
    x=df[df.AGREGACAO==agg]; out=[]
    for _,r in x.iterrows():
        o={'a':int(r.ANO),'g':(r[grpcol] if grpcol else 'TODOS'),'n':(r.NOME if agg!='BRASIL' else 'Brasil')}
        for v in V: o[v]=round(float(r[v]),4)
        out.append(o)
    return out
data={}
for k,df,gc in [('geral',g,None),('sexo',s,'SEXO'),('cor',c,'COR')]:
    data[k]={'brasil':rows(df,gc,'BRASIL'),'uf':rows(df,gc,'UF'),'rm':[r for r in rows(df,gc,'RM_RIDE') if r['a']==2021]}
REG={"Norte":["Rondônia","Acre","Amazonas","Roraima","Pará","Amapá","Tocantins"],
"Nordeste":["Maranhão","Piauí","Ceará","Rio Grande do Norte","Paraíba","Pernambuco","Alagoas","Sergipe","Bahia"],
"Sudeste":["Minas Gerais","Espírito Santo","Rio de Janeiro","São Paulo"],"Sul":["Paraná","Santa Catarina","Rio Grande do Sul"],
"Centro-Oeste":["Mato Grosso do Sul","Mato Grosso","Goiás","Distrito Federal"]}
data['reg']={u:r for r,us in REG.items() for u in us}
missing=set(x['n'] for x in data['sexo']['uf'])-set(data['reg']); print('sem região',missing)
t=pd.read_csv(d+'TabelaIndio.csv',sep=';',skiprows=5,names=['uf','n'],encoding='utf-8-sig',nrows=27)
t['n']=t.n.astype(int); print(t.n.sum(), len(t))
data['ind']={'uf':[{'n':r.uf,'v':int(r.n)} for r in t.itertuples()],'brasil':1694836}
# stats checks (pandas, ddof=1)
u=g[(g.AGREGACAO=='UF')&(g.ANO==2021)]
r=u.RDPC; q1,q3=r.quantile(.25),r.quantile(.75); i=q3-q1
print('RDPC',r.mean(),r.median(),q1,q3,i,u[(r<q1-1.5*i)|(r>q3+1.5*i)][['NOME','RDPC']].values.tolist())
open(RAW+'build/data.json','w').write(json.dumps(data,ensure_ascii=False,separators=(',',':')))
print(len(json.dumps(data))//1024,'KB')
