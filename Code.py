import streamlit as st
import graphviz as graphviz
import pandas as pd
from prettytable import PrettyTable
from collections import defaultdict
from csv import writer
import csv

columns=["T1","T2","T3","T4","T5"]
#F_path = "E:\\College\\Documents\\DBMS\\Innovative\\"
F_path = ""
with open(F_path+"styles.css") as f:
    st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)

m=[]
c2 = "<div class='heading1'>Transaction and Concurrency Management</div>"
st.markdown(c2, unsafe_allow_html=True)
cl1,cl2 = st.columns(2)
with cl1:
    num_trans=st.number_input("Select the number of transactions: ",2,10)
with cl2:
    num_var=st.number_input("Select the number of Variables: ",2,10)
myTable1 = PrettyTable(columns)
nodes = {}
length=[]
Final=[]

class SerializabilitySequence():
    def __init__(self):
        self.nodes=defaultdict(list)

    def addNode(self,a,b):
        if a not in list(self.nodes.keys()):
            self.nodes[a] = [b]
        else:
            self.nodes[a].append(b)
        # print(self.nodes)

    def rcall(self,b,tvisited,csequence):
        tvisited[b]=True
        for q in self.nodes[b]:
            if tvisited[q]==False:
                self.rcall(q,tvisited,csequence)
        csequence.append(b+1)

    def sort(self):
        m = max(self.nodes.keys())
        for k in self.nodes.keys():
            m = max(m,max(self.nodes[k]))
        tvisited = [False]*(m+1)
        csequence = []
        M = list(self.nodes.keys()).copy()
        for p in M:
            if tvisited[p]==False:
                self.rcall(p,tvisited,csequence)
        csequence.reverse()
        return csequence
        # st.text("Serializability sequence is: "+str(csequence))

class Cycle():

    def __init__(self):
        self.Graph=defaultdict(list)

    def addedge(self,a,b):
        # st.write(a,b)
        if a not in list(self.Graph.keys()):
            self.Graph[a] = [b]
        else:
            self.Graph[a].append(b)

    def checkCycle(self,node,visited,dfsvisit):
        # st.text("top visited = "+str(visited))
        # st.text("top dfsvisited = "+str(dfsvisit))
        # st.text("node = "+str(node))
        visited[node]=True
        dfsvisit[node]=True
        for j in self.Graph[node]:
            # st.text("visited = "+str(visited))
            # st.text("dfsvisited = "+str(dfsvisit))
            # st.text("j="+str(j))
            # st.text("j=",j)
            # st.text("visited=",visited[j])
            # st.text("dfsvisit=",dfsvisit[j])
            if visited[j]==False:
                # st.text("j="+str(j-1))
                if self.checkCycle(j,visited,dfsvisit)==True:
                    return True
            elif dfsvisit[j]==True:
                return True
        dfsvisit[node]=False
        # st.text("dfsvisited = "+str(dfsvisit))
        return False

    def isCyclic(self):
        m = max(self.Graph.keys())
        for k in self.Graph.keys():
            m = max(m,max(self.Graph[k]))
        visited=[False]*(m+1)
        dfsvisit=[False]*(m+1)
        # st.text("visited = "+str(visited))
        M = list(self.Graph.keys()).copy()
        for k in M:
            # st.text("k="+str(k))
            # st.text("visitedk = "+str(visited[k]))
            if visited[k]==False:
                if self.checkCycle(k,visited,dfsvisit)==True:
                    return True
        return False

lst=[]
varlst=[]
num_trans=int(num_trans)
num_var=int(num_var)
u=97
for w in range(1,num_trans+1):
    lst.append(w)
for v in range(1,num_var+1):
    varlst.append(chr(u))
    u+=1

temp=st.form(key="Conflict Serialization")

with open(F_path+"Transactions.csv") as Tfile:      
    R_Obj = csv.reader(Tfile)
    f = open(F_path+"text.txt",mode="w")
    i=0
    for r in R_Obj:
        if(i==0):
            i=1;continue
        f.write("".join(r).strip("-")+"\n")
f.close()        
with temp:

    t=st.selectbox("Select Transaction",lst)
    var=st.selectbox("Select variable: ",varlst)
    op=st.selectbox("Select operation",["Read","Write"])
    s=st.form_submit_button("Submit!")
    if op=="Read":
        sel="R"+str(t)+"("+var+")"
    else:
        sel="W"+str(t)+"("+var+")"


with open(F_path+"Transactions.csv","r") as Tfile:      
    x=["-"]*max(t,len(Tfile.readline().split(",")))
# st.text(x)
# st.text(t)
# st.text(sel)
x[t-1]=sel
# st.text(x)
if s:
    fo=open(F_path+"text.txt","a")
    fo.write(sel)
    fo.close()
    st.markdown("<br><div class='note'>You entered : "+str(sel)+"</div><br>", unsafe_allow_html=True)
    with open(F_path+'transactions.csv', 'a') as f_object:
        writer_object = writer(f_object)
        writer_object.writerow(x)
    f_object.close()

#implementing conflict serializability

def check(A,B):
    if(A=="" or B==""):
        return False
    if(A[0]=="W"):
        li=["R","W"]
    else:
        li=["W"]
    if(A[3]==B[3] and B[0] in li and A[1]!=B[1]):
        return True
    else:
        return False
graph = graphviz.Digraph(strict=True)
f1 = open(F_path+'text.txt', "r").read().split("\n")[:-1]
# f2 = open(F_path+'text.txt', "r")
# li = f2.split("\n")
f1 = list(filter(None, f1))
print(f1)
Trs = set()
G = Cycle()
T = SerializabilitySequence()
cl3,cl4 = st.columns(2)
with cl3:
    S=st.button("FINAL SUBMIT")
with cl4:
    Cl=st.button("RESET DATA")
if S:
    data = pd.read_csv(F_path+"Transactions.csv") 
    st.dataframe(data,width=700,height=800)
    count=0
    st.markdown("<br><div class='note'>Graph for Conflicting operations : </div><br>", unsafe_allow_html=True)
    c1,c3,c5=st.columns(3)
    co=0
    for x in f1:        
        count+=1
        if(count==len(f1)):
            break           
        for y in f1[count:]:
            Trs.add("T"+str(x[1]))
            if(check(x,y)):
                co=1
                graph.edge("T"+str(x[1]),"T"+str(y[1]))
                m=int(x[1])-1
                n=int(y[1])-1
                G.addedge(m,n)
                T.addNode(m,n)
                with c3:
                    st.markdown("<p class='grt'>"+str("T"+str(x[1])+" → T"+str(y[1]))+"</p>", unsafe_allow_html=True)
                    st.graphviz_chart(graph)
        if(co==0):
            st.markdown("<p class='warn'>There are no two records which are conflicting..</p>", unsafe_allow_html=True)
        # f2.seek(0,0)
    # for k in nodes.keys():
    #     st.text(str(k)+" : "+str(nodes[k]))
    # st.text(G.Graph)
    # st.text(T.nodes)
    
    st.markdown("<hr><div class='Ans'>Cycle detection in Graph : </div><br><br>", unsafe_allow_html=True)
    if(len(list(G.Graph.keys()))>0 and G.isCyclic()):
        st.markdown("<div class='Ans'>There is a Cycle so It is not Conflict serializable..</div><hr>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='Ans'>There is not a Cycle so It is Conflict serializable..</div>", unsafe_allow_html=True)
        st.markdown("<div class='Ans1'>So, It is possible to create equivalent Serial Schedule</div><hr>", unsafe_allow_html=True)
        if len(list(T.nodes.keys())):
            Seq = T.sort()
        else:
            Seq = list(Trs)
        st.markdown("<div class='Final'>Serial Schedule :"+" → ".join([str(n) for n in Seq])+" </div>", unsafe_allow_html=True)

if Cl:
    f = open(F_path+"Transactions.csv", "w+")
    f.write(",".join(["T"+str(k+1) for k in range(num_trans)])+"\n")
    f.close()
    f = open(F_path+"text.txt", "w+")
    f.close()
    st.markdown("<hr><div class='Ans'>Data Resetted Successfully</div><br><br>", unsafe_allow_html=True)