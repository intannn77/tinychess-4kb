import json,os,urllib.request as u
Z='abcdefgh';M={'P':100,'N':320,'B':330,'R':500,'Q':900,'K':90000};P='5443344543222234422112244220012442200124422112244322223454433445';K=[(1,2),(2,1),(2,-1),(1,-2),(-1,-2),(-2,-1),(-2,1),(-1,2)];D=[(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]
S=lambda q:Z.index(q[0])+8*(int(q[1])-1)
Q=lambda s:Z[s%8]+str(s//8+1)
C=lambda c:c.isupper()
def prs(f):
 p=f.split();b={};r=8
 for w in p[0].split('/'):
  i=0
  for c in w:
   if c.isdigit():i+=int(c)
   else:b[S(Z[i]+str(r))]=c;i+=1
  r-=1
 return b,p[3]if len(p)>3 else'-',p[2]if len(p)>2 else'-'
def ev(b,s):
 t=0
 for q,c in b.items():
  if c.upper()in M:t+=(M[c.upper()]+ord(P[q])-53)*(1 if C(c)else-1)
 return t if s else-t
def ap(b,m,e):
 n=dict(b);f,t,p=m;n[t]=n[f];p and n.__setitem__(t,p);del n[f]
 if e!='-'and Q(t)==e and n[t]in'Pp':n.pop(t-8 if n[t]=='P'else t+8,0)
 if abs(f%8-t%8)==2 and n[t]in'Kk':x=t%8;y=t//8;rs=(x+1 if x>4 else x-2)+8*y;rd=(x-1 if x>4 else x+1)+8*y;rs in n and(n.__setitem__(rd,n[rs]),n.pop(rs))
 return n
cv=lambda b,m:(M[b[m[1]].upper()]if m[1]in b else 0)+(800 if m[2]else 0)
def ck(b,s):
 k=next((q for q,c in b.items()if C(c)==s and c.upper()=='K'),None)
 if not k:return 0
 x,y=k%8,k//8
 for q,c in b.items():
  if C(c)==s:continue
  i,j=q%8,q//8;u=c.upper()
  if u=='P':
   for h in(-1,1):
    if i+h==x and j+(1 if C(c)else-1)==y:return 1
  elif u=='N':
   for h,v in K:
    if i+h==x and j+v==y:return 1
  elif u in'BRQ':
   for h,v in(D[4:]if u=='B'else D if u=='Q'else D[:4]):
    for l in range(1,8):
     a,o=i+l*h,j+l*v
     if not(0<=a<8 and 0<=o<8):break
     if a==x and o==y:return 1
     if a+8*o in b:break
 return 0
def gm(b,s,e,cs):
 L=[];d=1 if s else-1;r=1 if s else 6;g=6 if s else 1;w=0 if s else 7
 for q,c in b.items():
  i,j=q%8,q//8;u=c.upper()
  if C(c)!=s:continue
  if u=='P':
   n=q+8*d
   if 0<=n<64 and n not in b:
    if j==g:
     for m in('QRBN'if C(c)else'qrbn'):L.append((q,n,m))
    else:L.append((q,n,None))
    if j==r and q+16*d not in b:L.append((q,q+16*d,None))
   for h in(-1,1):
    if 0<=i+h<8:
     t=i+h+8*(j+d)
     if 0<=t<64:
      z=b.get(t)
      if(z and C(z)!=s)or e==Q(t):L.append((q,t,None))
  elif u=='N':
   for h,v in K:
    a,o=i+h,j+v
    if 0<=a<8 and 0<=o<8:
     t=a+8*o
     if t not in b or C(b[t])!=s:L.append((q,t,None))
  elif u in'BRQ':
   for h,v in(D[4:]if u=='B'else D if u=='Q'else D[:4]):
    for l in range(1,8):
     a,o=i+l*h,j+l*v
     if not(0<=a<8 and 0<=o<8):break
     t=a+8*o;z=b.get(t)
     if z and C(z)==s:break
     L.append((q,t,None))
     if z:break
  elif u=='K':
   for h,v in D:
    a,o=i+h,j+v
    if 0<=a<8 and 0<=o<8:
     t=a+8*o
     if t not in b or C(b[t])!=s:L.append((q,t,None))
   if cs!='-'and q==4+8*w:
    ('K'if s else'k')in cs and all(x+8*w not in b for x in[5,6])and L.append((q,6+8*w,None))
    ('Q'if s else'q')in cs and all(x+8*w not in b for x in[1,2,3])and L.append((q,2+8*w,None))
 return L
lm=lambda b,s,e,cs:[m for m in gm(b,s,e,cs)if not ck(ap(b,m,e),s)]
def sr(b,d,a,B,s,e,cs):
 if d<1:return ev(b,s),None
 L=lm(b,s,e,cs)
 if not L:return(-50000 if ck(b,s)else 0),None
 L.sort(key=lambda x:-cv(b,x));bm=None
 for m in L:
  v=-sr(ap(b,m,e),d-1,-B,-a,1-s,'-','-')[0]
  if v>a:a,bm=v,m
  if a>=B:break
 return a,bm
def main():
 E=os.getenv("MAKEFUN_ENV_URL")or"";H={"Content-Type":"application/json"};g=0
 while 1:
  try:x=u.urlopen(u.Request(E+"/game",b"{}",H),timeout=9)
  except:break
  A=json.loads(x.read())
  if A.get("status")=="done":break
  g=A.get("game",g);s=1 if A["colour"]=="white"else 0;f=A["fen"]
  while A["status"]=="your_move":
   b,e,cs=prs(f)
   if not lm(b,s,e,cs):break
   _,m=sr(b,4,-99999,99999,s,e,cs)
   if not m:break
   try:x=u.urlopen(u.Request(E+"/move",json.dumps({"game":g,"move":Q(m[0])+Q(m[1])+(m[2].lower()if m[2]else'')}).encode(),H),timeout=9)
   except:break
   A=json.loads(x.read());f=A.get("fen",f)
   if A["status"]=="over":break
   if A["status"]!="your_move":break
if __name__=="__main__":main()
