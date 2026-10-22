import os,csv,io,uuid,datetime
from decimal import Decimal
from fastapi import FastAPI,Depends,HTTPException,UploadFile,File,Header
from fastapi.responses import HTMLResponse,StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel,Field
from sqlalchemy import create_engine,Column,String,Integer,Numeric,DateTime,ForeignKey,Text,select,func
from sqlalchemy.orm import declarative_base,sessionmaker,Session

DB=os.getenv('DATABASE_URL','sqlite:///./ap2i.db')
engine=create_engine(DB,connect_args={'check_same_thread':False} if DB.startswith('sqlite') else {})
SessionLocal=sessionmaker(bind=engine)
Base=declarative_base()
class Country(Base):
 __tablename__='countries'
 code=Column(String(3),primary_key=True);name=Column(String(120),nullable=False)
class Project(Base):
 __tablename__='projects'
 id=Column(String(36),primary_key=True);country_code=Column(String(3),ForeignKey('countries.code'),nullable=False,index=True)
 name=Column(String(350),nullable=False);sector=Column(String(100),nullable=False,index=True);agency=Column(String(200));status=Column(String(80),default='Non renseigné');start_year=Column(Integer);end_year=Column(Integer)
 initial_cost=Column(Numeric(20,2));revised_cost=Column(Numeric(20,2));currency=Column(String(3),default='XAF');physical_progress=Column(Numeric(5,2));operational_status=Column(String(100));source_url=Column(Text);source_date=Column(String(20));notes=Column(Text)
class Financing(Base):
 __tablename__='financings'
 id=Column(String(36),primary_key=True);project_id=Column(String(36),ForeignKey('projects.id'),nullable=False,index=True);funder=Column(String(200),nullable=False);instrument=Column(String(100));committed=Column(Numeric(20,2));currency=Column(String(3));source_url=Column(Text)
class Disbursement(Base):
 __tablename__='disbursements'
 id=Column(String(36),primary_key=True);financing_id=Column(String(36),ForeignKey('financings.id'),nullable=False,index=True);year=Column(Integer,nullable=False);amount=Column(Numeric(20,2),nullable=False);source_url=Column(Text)
class Amendment(Base):
 __tablename__='amendments'
 id=Column(String(36),primary_key=True);project_id=Column(String(36),ForeignKey('projects.id'),nullable=False);date=Column(String(20));amount=Column(Numeric(20,2));currency=Column(String(3));reason=Column(Text);source_url=Column(Text)
class Action(Base):
 __tablename__='actions'
 id=Column(String(36),primary_key=True);project_id=Column(String(36),ForeignKey('projects.id'),nullable=False);problem=Column(Text);recommendation=Column(Text);owner=Column(String(200));due_date=Column(String(20));status=Column(String(30),default='À faire')
Base.metadata.create_all(engine)
with SessionLocal() as s:
 if not s.get(Country,'CMR'):
  s.add(Country(code='CMR',name='Cameroun'))
  # All 54 country codes can be inserted via admin/API; no synthetic project records.
  s.commit()
app=FastAPI(title='AP²I – Africa Public Project Intelligence',version='0.1.0')
app.mount('/static',StaticFiles(directory=os.path.join(os.path.dirname(__file__),'static')),name='static')
def session():
 with SessionLocal() as s:yield s
def admin(x_admin_key:str|None=Header(None)):
 secret=os.getenv('AP2I_ADMIN_KEY')
 if not secret or x_admin_key!=secret:raise HTTPException(403,'Clé administrateur requise')
class ProjectIn(BaseModel):
 country_code:str='CMR';name:str;sector:str;agency:str|None=None;status:str='Non renseigné';start_year:int|None=None;end_year:int|None=None;initial_cost:Decimal|None=None;revised_cost:Decimal|None=None;currency:str='XAF';physical_progress:Decimal|None=Field(None,ge=0,le=100);operational_status:str|None=None;source_url:str|None=None;source_date:str|None=None;notes:str|None=None
class FinanceIn(BaseModel):
 funder:str;instrument:str|None=None;committed:Decimal|None=None;currency:str='XAF';source_url:str|None=None
class DisbursementIn(BaseModel):
 year:int=Field(ge=2000,le=2100);amount:Decimal=Field(ge=0);source_url:str|None=None
class ActionIn(BaseModel):
 problem:str;recommendation:str;owner:str|None=None;due_date:str|None=None;status:str='À faire'
def serial(x):
 return {c.name:(float(getattr(x,c.name)) if isinstance(getattr(x,c.name),Decimal) else getattr(x,c.name)) for c in x.__table__.columns}
@app.get('/',response_class=HTMLResponse)
def home():return open(os.path.join(os.path.dirname(__file__),'static','index.html'),encoding='utf8').read()
@app.get('/api/countries')
def countries(s:Session=Depends(session)):return [serial(x) for x in s.scalars(select(Country).order_by(Country.name))]
@app.post('/api/countries',dependencies=[Depends(admin)])
def add_country(payload:dict,s:Session=Depends(session)):
 x=Country(code=payload['code'].upper(),name=payload['name']);s.add(x);s.commit();return serial(x)
@app.get('/api/projects')
def projects(country:str='CMR',sector:str|None=None,year:int|None=None,limit:int=100,offset:int=0,s:Session=Depends(session)):
 q=select(Project).where(Project.country_code==country.upper())
 if sector:q=q.where(Project.sector==sector)
 if year:q=q.where((Project.start_year<=year)|(Project.start_year.is_(None))).where((Project.end_year>=year)|(Project.end_year.is_(None)))
 return [serial(x) for x in s.scalars(q.order_by(Project.name).offset(offset).limit(min(limit,500)))]
@app.post('/api/projects',dependencies=[Depends(admin)])
def create_project(p:ProjectIn,s:Session=Depends(session)):
 if not s.get(Country,p.country_code):raise HTTPException(400,'Pays non enregistré')
 x=Project(id=str(uuid.uuid4()),**p.model_dump());s.add(x);s.commit();return serial(x)
@app.get('/api/projects/{pid}')
def detail(pid:str,s:Session=Depends(session)):
 p=s.get(Project,pid)
 if not p:raise HTTPException(404)
 return {'project':serial(p),'financings':[serial(x) for x in s.scalars(select(Financing).where(Financing.project_id==pid))],'amendments':[serial(x) for x in s.scalars(select(Amendment).where(Amendment.project_id==pid))],'actions':[serial(x) for x in s.scalars(select(Action).where(Action.project_id==pid))]}
@app.post('/api/projects/{pid}/financings',dependencies=[Depends(admin)])
def add_financing(pid:str,f:FinanceIn,s:Session=Depends(session)):
 if not s.get(Project,pid):raise HTTPException(404)
 x=Financing(id=str(uuid.uuid4()),project_id=pid,**f.model_dump());s.add(x);s.commit();return serial(x)
@app.post('/api/financings/{fid}/disbursements',dependencies=[Depends(admin)])
def add_disbursement(fid:str,d:DisbursementIn,s:Session=Depends(session)):
 f=s.get(Financing,fid)
 if not f:raise HTTPException(404)
 if f.currency is None:raise HTTPException(400,'Devise du financement manquante')
 x=Disbursement(id=str(uuid.uuid4()),financing_id=fid,**d.model_dump());s.add(x);s.commit();return serial(x)
@app.post('/api/projects/{pid}/actions',dependencies=[Depends(admin)])
def add_action(pid:str,a:ActionIn,s:Session=Depends(session)):
 if not s.get(Project,pid):raise HTTPException(404)
 x=Action(id=str(uuid.uuid4()),project_id=pid,**a.model_dump());s.add(x);s.commit();return serial(x)
@app.get('/api/dashboard')
def dashboard(country:str='CMR',s:Session=Depends(session)):
 ps=list(s.scalars(select(Project).where(Project.country_code==country.upper())))
 sectors={}
 for p in ps:sectors[p.sector]=sectors.get(p.sector,0)+1
 return {'country':country.upper(),'project_count':len(ps),'sectors':sectors,'status':{v:sum(p.status==v for p in ps) for v in set(p.status for p in ps)},'data_policy':'Les montants de devises différentes ne sont jamais additionnés.'}
@app.get('/api/annual')
def annual(country:str='CMR',s:Session=Depends(session)):
 ps=list(s.scalars(select(Project).where(Project.country_code==country.upper())))
 result=[]
 for y in range(2011,2027):
  result.append({'year':y,'new_projects':sum(p.start_year==y for p in ps),'active_projects':sum(p.start_year is not None and p.start_year<=y and (p.end_year is None or p.end_year>=y) for p in ps)})
 return result
@app.get('/api/projects/{pid}/diagnostic')
def diagnostic(pid:str,s:Session=Depends(session)):
 p=s.get(Project,pid)
 if not p:raise HTTPException(404)
 alerts=[]
 if p.physical_progress is None:alerts.append({'level':'information','finding':'Avancement physique non renseigné','action':'Obtenir le dernier rapport d’exécution.'})
 if p.end_year and p.end_year<datetime.date.today().year and p.status.lower() not in ('achevé','termine','terminé','opérationnel'):
  alerts.append({'level':'attention','finding':'Date de fin prévue dépassée et statut non clôturé','action':'Vérifier le calendrier révisé et les jalons contractuels.'})
 if p.initial_cost is not None and p.revised_cost is not None and p.initial_cost>0 and p.revised_cost>p.initial_cost*Decimal('1.2'):
  alerts.append({'level':'attention','finding':'Coût révisé supérieur de plus de 20 % au coût initial','action':'Examiner les raisons documentées de la révision; ce n’est pas une preuve de mauvaise gestion.'})
 if p.status.lower() in ('achevé','termine','terminé') and not p.operational_status:
  alerts.append({'level':'information','finding':'Statut opérationnel inconnu','action':'Vérifier la mise en service et le fonctionnement effectif.'})
 return {'project_id':pid,'method':'Règles explicites, sans diagnostic IA ni causalité inférée','alerts':alerts}
@app.get('/api/export.csv')
def export(country:str='CMR',s:Session=Depends(session)):
 rows=list(s.scalars(select(Project).where(Project.country_code==country.upper())))
 buf=io.StringIO();fields=[c.name for c in Project.__table__.columns];w=csv.DictWriter(buf,fieldnames=fields);w.writeheader();[w.writerow(serial(x)) for x in rows]
 return StreamingResponse(iter([buf.getvalue()]),media_type='text/csv',headers={'Content-Disposition':'attachment; filename="ap2i_projects.csv"'})
@app.post('/api/import.csv',dependencies=[Depends(admin)])
async def import_csv(file:UploadFile=File(...),s:Session=Depends(session)):
 raw=await file.read()
 if len(raw)>3_000_000:raise HTTPException(413,'Fichier trop volumineux')
 try:records=list(csv.DictReader(io.StringIO(raw.decode('utf-8-sig'))))
 except Exception:raise HTTPException(400,'CSV invalide')
 errors=[];created=0
 for i,r in enumerate(records,2):
  try:
   clean={k:(v if v!='' else None) for k,v in r.items() if k in ProjectIn.model_fields}
   p=ProjectIn(**clean)
   if not s.get(Country,p.country_code):raise ValueError('Pays non enregistré')
   if not p.source_url:raise ValueError('URL source obligatoire pour import')
   s.add(Project(id=str(uuid.uuid4()),**p.model_dump()));s.flush();created+=1
  except Exception as e:errors.append({'line':i,'error':str(e)[:250]})
 if errors:s.rollback();return {'imported':0,'errors':errors,'message':'Import annulé intégralement: corriger les lignes.'}
 s.commit();return {'imported':created,'errors':[]}
