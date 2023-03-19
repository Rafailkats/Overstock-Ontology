from tkinter import *
from customtkinter import *
from tkinter import ttk
import rdflib
from rdflib.namespace import RDF,SKOS
from owlready2 import *
import tkinter.messagebox
import random
import webview
from tkcalendar import Calendar
global onto
global g
global listmadein
onto=get_ontology("D:/Project/Overstock.owl").load()
g = rdflib.Graph()
g.parse('D:/Project/Overstock.owl')
current="HomeItem"
previous="HomeItem"
query5="SELECT ?madein WHERE { ?id :hasMadeIn ?madein .}"
listmadein=[""]
resultss=g.query(query5)
for i in resultss:
    if str(i["madein"]) not in listmadein and str(i["madein"]) != 'No Info' :
            listmadein.append(str(i["madein"]))
#Αυτή η συνάρτηση εκτελείται όταν πατηθούν τα κουμπία delete για του υπαλλλήλους
#πελάτες κα συναλλαγές και διαγράφη το αντίστοιχο στιγμιότυπο. Καταστρέφει το στιγμιότυπο
#και αποθηκευέι τις αλλαγές με την .save() της αλλαγές στην οντολογία
def deletebutton(i,window1):
    name=str(i).replace("http://test.org/onto.owl#","")
    arxika=name[0]+name[1]
    destroy_entity(onto[name])
    onto.save("Overstock.owl",format="rdfxml")
    tkinter.messagebox.showinfo("Delete","The entity deleted along with every record of it!!")
    window1.destroy()


#συνάρτηση αποθήκευσης υπαλλήλου και πελάτη
def saving(string,name,surname,phone,email,address):
   querya="SELECT ?id WHERE { ?id a :"+string+" . ?id :address \""+address+"\"^^xsd:string . ?id :firstName \""+name+"\"^^xsd:string ."
   queryb=" ?id :lastName \""+surname+"\"^^xsd:string . ?id :phone \""+phone+"\"^^xsd:string .  ?id :email \""+email+"\"^^xsd:string .}"
   query=querya+queryb
   results=g.query(query)
   for i in results:
        tkinter.messagebox.showinfo(string,  "There is already such "+ string)
        return
   with onto:
      if string=="" or name=="" or surname=="" or phone=="" or email=="" or address=="":
          tkinter.messagebox.showinfo(string,  "Error, you have to fill all the fields!!")
          return
      elif string=="Employee":
          found=False
          while found==False:
              found=True
              id_name="EM"+str(random.randint(0,100000))
              query="""SELECT ?id WHERE { ?id a :Employee .  }"""
              results=g.query(query)
              for i in results:
                  if str(i["id"]).replace("http://test.org/onto.owl#EM","")==id_name:
                      found=False
                      break
          new_indi=onto["Employee"](id_name,firstName=name,lastName=surname,phone=phone,email=email,address=address)
      else:
          found=False
          while found==False:
              found=True
              id_name="CU"+str(random.randint(0,100000))
              query="""SELECT ?id WHERE { ?id a :Customer .  }"""
              results=g.query(query)
              for i in results:
                  if str(i["id"]).replace("http://test.org/onto.owl#CL","")==id_name:
                      found=False
                      break
          new_indi=onto["Customer"](id_name,firstName=name,lastName=surname,phone=phone,email=email,address=address)
      tkinter.messagebox.showinfo(string,  "Succesfful Entry!!")
      onto.save("Overstock.owl",format="rdfxml")
#συνάρτηση για αποθήκευση συναλλαγής
def savingTr(string,e1,e2,combo1,combo2):
    with onto:
      if e1=="" or e2=="" or combo1=="" or combo2=="":
          tkinter.messagebox.showinfo(string,  "Error, you have to fill all the fields!!")
          return
      id_name="TR"+str(random.randint(0,100000))
      cid=[]
      eid=[]
      for i in combo1:
          if i==":":
              break
          else:
              eid.append(i)
      for i in combo2:
          if i==":":
              break
          else:
              cid.append(i)
      ilist=[]
      temp=""
      for i in e2:
          if i==",":
              ilist.append(temp.replace(" ",""))
              temp=""
          else:
              temp=temp+i
      ilist.append(temp.replace(" ",""))
      items=[]
      price=0.0
      for i in ilist:
          items.append(onto[i])
          price=price+onto[i].hasPrice
      new_indi=onto["Transaction"](id_name,date=e1,hasEmploy=onto["".join(eid)],hasClient=onto["".join(cid)],inItem=items,totalPrice=round(float(price),3))
      tkinter.messagebox.showinfo(string,  "Succesfful Entry!!")
      onto.save("Overstock.owl",format="rdfxml")

#εκτελείται για εισαγωγή νέου στιγμιότυπου συναλλαγής,πελάτης,υπαλληλος.
def insertNew(string):
   g = rdflib.Graph()
   g.parse('D:/Project/Overstock.owl')
   window2=CTk()
   window2.title("New "+string)
   window2.geometry('550x400')
   window2.resizable(width=False, height=False)
   if string=="Customer" or string=="Employee":
      CTkLabel(window2, text="First Name: ",font=('calibri', 35)).grid(row=0)
      CTkLabel(window2, text="Last Name: ",font=('calibri', 35)).grid(row=1)
      CTkLabel(window2, text="Phone: ",font=('calibri', 35)).grid(row=2)
      CTkLabel(window2, text="Email: ",font=('calibri', 35)).grid(row=3)
      CTkLabel(window2, text="Address: ",font=('calibri', 35)).grid(row=4)
      e1 = Entry(window2,font=('calibri', 15))
      e2 = Entry(window2,font=('calibri', 15))
      e3 = Entry(window2,font=('calibri', 15))
      e4 = Entry(window2,font=('calibri', 15))
      e5 = Entry(window2,font=('calibri', 15))
      CTkButton(window2,text="SAVE",font=('calibri', 17),command=lambda:[saving(string,e1.get(),e2.get(),e3.get(),e4.get(),e5.get()),window2.destroy()]).grid(row=5,column=1)
      e1.grid(row=0, column=1)
      e2.grid(row=1, column=1)
      e3.grid(row=2, column=1)
      e4.grid(row=3, column=1)
      e5.grid(row=4, column=1)
   else:
      e1=Calendar(window2, selectmode = 'day',year = 2023, month = 1,day = 1)
      e1.grid(row=0, column=1,pady=6)
      clist=[]
      elist=[]
      query="""SELECT ?id WHERE { ?id a :Employee .  }"""
      results=g.query(query)
      for i in results:
          code=str(i["id"]).replace("http://test.org/onto.owl#","")
          elist.append(""+code+": "+onto[code].firstName+" "+onto[code].lastName)
      query="""SELECT ?id WHERE { ?id a :Customer .  }"""
      results=g.query(query)
      for i in results:
          code=str(i["id"]).replace("http://test.org/onto.owl#","")
          clist.append(""+code+": "+onto[code].firstName+" "+onto[code].lastName)
      Combo10=CTkComboBox(window2, values = elist,width=250)
      Combo10.grid(row=1,column=1)
      Combo10.set("")
      Combo11=CTkComboBox(window2, values = clist,width=250)
      Combo11.grid(row=2,column=1)
      Combo11.set("")
      CTkLabel(window2, text="Employee: ",font=('calibri', 18)).grid(row=1,column=0,pady=5)
      CTkLabel(window2, text="Customer: ",font=('calibri', 18)).grid(row=2,column=0,pady=5)
      CTkLabel(window2, text="Items: ",font=('calibri', 18)).grid(row=3,column=0)
      CTkLabel(window2, text="Please insert the codes of the items\neg: 2322424,234332423: ",font=('calibri', 12),text_color='red').grid(row=4,column=0)
      e2 =Text(window2,width=25,height=3)
      e2.grid(row=3, column=1,pady=6)
      CTkButton(window2,text="SAVE",command=lambda:[savingTr(string,e1.get_date(),e2.get("1.0",'end-1c'),Combo10.get(),Combo11.get()),window2.destroy()]).grid(row=5,column=1)
   window2.mainloop()


#εκτελείται όταν πατηθούν τα κουμπιά Transactions/Employments/Customers. Παρουσιάζει
#τις συνναλαγές,πελάτες,υπαλλήλους με τα στοιχεία τους.
def empcust(string,choice):
    onto=get_ontology("D:/Project/Overstock.owl").load()
    g = rdflib.Graph()
    g.parse('D:/Project/Overstock.owl')
    window1=CTk(fg_color='darkgrey')
    window1.title(string+"s")
    window1.geometry('550x450')
    window1.resizable(width=False, height=False)
    main_frame=Frame(window1)
    main_frame.pack(fill=BOTH,expand=1)
    my_canvas=Canvas(main_frame,bg='#232323')
    my_canvas.pack(side=LEFT,fill=BOTH,expand=1)
    my_scrollbar=Scrollbar(main_frame,orient=VERTICAL,command=my_canvas.yview)
    my_scrollbar.pack(side=RIGHT,fill=Y)
    my_canvas.configure(yscrollcommand=my_scrollbar.set)
    my_canvas.bind('<Configure>',lambda e:my_canvas.configure(scrollregion=my_canvas.bbox("all")))
    second_frame=Frame(my_canvas,bg='#232323')
    my_canvas.create_window((0,0),window=second_frame,anchor="nw")
    Button(second_frame,text="Press to insert New "+string,width=56,font=('Clibri', 11),fg='white',bg='#3374FF',command=lambda:[window1.destroy(),insertNew(string)]).grid(row=0,column=0,pady=10,padx=15)
    if string=="Transaction":
         query="""SELECT ?id ?date ?totalPrice ?date ?employ ?client
                  WHERE { ?id a :Transaction . ?id :date ?date . ?id :totalPrice ?totalPrice .
                        OPTIONAL{?id :hasEmployee ?employ . }
                        OPTIONAL{?id :hasCustomer ?client . }
                    }"""
         if "EM" in choice:
             query=query.replace("OPTIONAL{?id :hasEmployee ?employ . }","?id :hasEmployee :"+choice+" .")
         elif "CL" in choice:
             query=query.replace("OPTIONAL{?id :hasEmployee ?employ . }","?id :hasCustomer :"+choice+" .")
             query=query.replace("OPTIONAL{?id :hasCustomer ?client . }","OPTIONAL{?id :hasEmployee ?employ . }")
         results=g.query(query)
         rowline=1
         for i in results:
            iditem=str(i["id"]).replace("http://test.org/onto.owl#","")
            itemlist=onto[iditem].inItem
            customer=str(i["client"]).replace("http://test.org/onto.owl#","").replace("None","No Info")
            if "EM" in choice:
                employment=choice
            else:
                employment=str(i["employ"]).replace("http://test.org/onto.owl#","").replace("None","No Info")
            if "CL" in choice:
                customer=choice
            else:
                customer=str(i["client"]).replace("http://test.org/onto.owl#","").replace("None","No Info")
            if employment!="No Info": employment=onto[employment].firstName + " " + onto[employment].lastName
            if customer!="No Info": customer=onto[customer].firstName + " " + onto[customer].lastName
            text_label="ID: "+ iditem +"\nDate: "+i["date"]+"\nTotal Price: " +i["totalPrice"] +" EUR"
            text_label=text_label+"\nEM: "+ employment
            text_label=text_label+"\nCL: "+ customer+"\nItems: "
            for y in itemlist:
                text_label=text_label+str(y).replace("Overstock.","")+","
            temp_frame=Frame(second_frame,bg='#232323')
            temp_frame.grid(row=rowline,column=0,pady=10,padx=15)
            Label(temp_frame,text=text_label,font=('calibri', 12),borderwidth=1, relief="solid").pack()
            CTkButton(temp_frame,text="Delete",command=lambda txt=i['id']:deletebutton(txt,window1)).pack()
            rowline=rowline+1
    else:
        classT=string
        query="""SELECT ?id ?fname ?lname ?phone ?email ?address
                 WHERE { ?id a :"""+classT+""" . ?id :firstName ?fname . ?id :lastName ?lname .
                     ?id :phone ?phone . ?id :address ?address . ?id :email ?email . }"""
        results=g.query(query)
        rowline=1
        for i in results:
          iditem=str(i["id"]).replace("http://test.org/onto.owl#","")
          text_label="ID: "+iditem+"\nName: "+i["fname"]+" "+i["lname"]+"\nPhone: "+i["phone"]+"\nEmail: "+i["email"]+"\nAddress: "+i["address"]
          temp_frame=Frame(second_frame,bg='#232323')
          temp_frame.grid(row=rowline,column=0,pady=10,padx=15)
          Button(temp_frame,text=text_label,font=('calibri', 12),borderwidth=1, relief="solid",command=lambda txt=iditem:empcust("Transaction",txt)).pack()
          CTkButton(temp_frame,text="Delete",command=lambda txt=i['id']:deletebutton(txt,window1)).pack()
          rowline=rowline+1
    window1.mainloop()
#εκτελείται όταν πατηθεί ένα αντικείμενο της αναζήτησης. Ανοίγει νέο παράθυρο με την εικόνα
#του αντικειμένου.
def expandImage(i):
   webview.create_window('Image of Home Item', onto[i].hasImage)
   webview.start()  
#συνάρτηση που εκτελείται όταν πατηθέι το κουμπί search. Ανάλογα με τα κριτήρια αναζήτησης δημιουργεί
#κατάλληλο query και οπτικοοιεί τα αποτελέσματα της αναζήτησης.
def searchFunction(m,h,c,r,made,a):
    if r.get()=="":rating=0
    elif r.get()=="5 stars": rating=5
    elif r.get()=="4 up": rating=4
    elif r.get()=="3 up": rating=3
    elif r.get()=="2 up": rating=2
    elif r.get()=="1 up": rating=1
    if m.get()=="": mini=0
    else: mini=float(m.get())
    if h.get()=="": highest=sys.float_info.max
    else: highest=float(h.get())
    if a.get()=='Yes': asse=True
    else: asse=False
    windowS=CTk()
    windowS.title("SEARCH RESULTS in "+current+"!!")
    windowS.geometry('750x550')
    #windowS.resizable(width=False, height=False)
    main_frameS=CTkFrame(windowS)
    main_frameS.pack(fill=BOTH,expand=1)
    my_canvasS=Canvas(main_frameS)
    my_canvasS.pack(side=LEFT,fill=BOTH,expand=1)
    my_scrollbarS=CTkScrollbar(main_frameS,orientation=VERTICAL,command=my_canvasS.yview)
    my_scrollbarS.pack(side=RIGHT,fill=Y)
    my_canvasS.configure(yscrollcommand=my_scrollbarS.set)
    my_canvasS.bind('<Configure>',lambda e:my_canvasS.configure(scrollregion=my_canvasS.bbox("all")))
    second_frameS=CTkFrame(my_canvasS)
    my_canvasS.create_window((0,0),window=second_frameS,anchor="nw")
    temp_list=list(onto[current].descendants())
    desc=[]
    for i in temp_list:
        desc.append(str(i).replace("Overstock.",""))  
    descendants=""
    turn=0
    for i in desc:
        if turn==0:
            descendants="?class = :"+i+" "
            turn=turn+1
        else:
            descendants=descendants+"|| ?class = :"+i+""
    query3="SELECT ?id ?price ?color ?rating WHERE { ?id a ?class . ?id :hasPrice ?price . ?id :hasMadeIn ?madein . ?id :hasColor ?color . ?id :hasRating ?rating ."
    query4="FILTER(regex(?color,\"" +c.get()+ "\",\"i\") && regex(?madein,\"" +made.get()+ "\",\"i\") && ?price <="+str(highest)+" && ?price >="+str(mini)+" && ?rating >= "+str(rating)+" && ("+descendants+")) }"
    query=query3+query4
    results=g.query(query)    
    rowline=0
    for i in results:
        iditem=str(i["id"]).replace("http://test.org/onto.owl#","")
        if (asse != "") and (onto[iditem].hasAssemblyNeeded != asse):
            continue
        texta=""+onto[iditem].hasTitle+"\nID: "+iditem+"\nPrice: "+str(i["price"])+" EUR""\nBrand: "+onto[iditem].hasBrand+"\nRating: "+str(i["rating"])+"""  Reviews: """+str(onto[iditem].hasReviews)
        textb="\nMade In: " + onto[iditem].hasMadeIn +"\nColor: " + (onto[iditem].hasColor).replace("\n","") +"\nWarranty Days: "+ str(onto[iditem].hasWarrantyDays) +"\nAssembly Needed: " + str(onto[iditem].hasAssemblyNeeded)
        textc=texta+textb
        CTkButton(second_frameS,fg_color='lightgray',text_color='black',text=textc,command=lambda txt=iditem:expandImage(txt)).pack(pady=5,expand=True, fill='x',padx=10)
        rowline=rowline+1     
    windowS.mainloop()
   
#συνάρτηση που εκτελείται όταν πατηθεί το κουμπί previous και next. Ανάλογα τροποποιεί τις μεταβλητές
#current, previous και ανανεώνει τις επιλογές για υποκλάσεις
def previousNext(m,label,bt):
    global current
    global previous
    query1="SELECT ?class WHERE { :"+current+" rdfs:subClassOf ?class .}"# επιστρέφει ποιες υποκλάσης είναι η κλάση current
    choice=m.get()
    if bt=="Previous":
      results=g.query(query1)
      for i in results:
          is_subclass=str(i["class"]).replace("http://test.org/onto.owl#","")
      if current=="HomeItem" or is_subclass=="HomeItem":
         current="HomeItem"
         previous="HomeItem"
      else:
         current=previous
         results=g.query(query1)
         for i in results:
             previous=str(i["class"]).replace("http://test.org/onto.owl#","")
    elif choice=="" or choice=="subclasses":
        return None
    else:
        previous=current
        current=choice
    query2="SELECT ?class WHERE { ?class rdfs:subClassOf :"+current+" .}"
    results=g.query(query2)
    vlist=[]
    for i in results:
        vlist.append(str(i["class"]).replace("http://test.org/onto.owl#",""))
    label.configure(text="Current Class: "+current)
    m.configure(values=vlist)
    m.set('')
#H παρακάτω εκτελείται όταν πατηθεί το κουμπί Home Items από το κεντρικό μενού.      
def homeItems(x):
    subclasses=list(onto["HomeItem"].subclasses()) #επιστρέφει τις υποκλάσεις της HomeItem
    vlist=[]
    for i in subclasses:
        vlist.append(str(i).replace("Overstock.",""))
    window3=CTk()
    window3.title("Home Items of Overstock Ontology!!")#δημιουργία layout 
    window3.geometry('550x450')
    window3.resizable(width=False, height=False)
    label1=CTkLabel(window3,text="Current Class: "+current,font=("Arial", 30))
    label1.pack(pady=10)
    frame=CTkFrame(window3)
    buttonpr=CTkButton(frame,text="<-- Previous",font=("Arial", 15),command=lambda: previousNext(Combo,label1,"Previous")).grid(row=0,column=0)
    Combo = CTkComboBox(frame, values = vlist,font=("Arial", 15))
    Combo.set("subclasses:")
    Combo.grid(row=0,column=1,padx=10)
    buttonNet=CTkButton(frame,text="Next -->",font=("Arial", 15),command=lambda: previousNext(Combo,label1,"Next")).grid(row=0,column=2)
    frame.pack(pady=10)
    label2=CTkLabel(window3,text="========= Search Options =========",font=("Arial", 30)).pack(pady=60)# επιλογές search
    #το layout για τις επιλογές για αναζήτηση color,price(min,high),rating
    frame15=CTkFrame(window3)
    frame15.pack(padx=70)
    CTkLabel(frame15,text="Price: ",font=("Arial", 12)).grid(row=0,column=0)
    frame16=CTkFrame(frame15)
    entryM=Entry(frame16,width=10)
    entryM.grid(row=0,column=0)
    CTkLabel(frame16,text="Min",font=("Arial", 12),padx=10).grid(row=0,column=1)
    frame16.grid(row=0,column=1)
    entryH=Entry(frame15,width=10)
    entryH.grid(row=0,column=3)
    CTkLabel(frame15,text="High",font=("Arial", 12),padx=10).grid(row=0,column=4)
    CTkLabel(frame15,text="Color:",font=("Arial", 12),padx=10).grid(row=1,column=0)
    CTkLabel(frame15,text="Rating:",font=("Arial", 12),padx=10).grid(row=2,column=0)
    CTkLabel(frame15,text="Made In:",font=("Arial", 12),padx=10).grid(row=3,column=0)
    CTkLabel(frame15,text="Assembly Needed:",font=("Arial", 12),padx=10).grid(row=4,column=0)
    clist=["Black","White","Red","Blue","Grey","Yellow","Orange","Brown","Tan","Beige","Silver","Cream","Green","Gold","Pink","Purple",""]
    rlist=["5 stars","4 up","3 up","2 up","1 up",""]
    Combo1 = CTkComboBox(frame15, values = clist)
    Combo1.set("")
    Combo1.grid(row=1,column=1)
    Combo2 = CTkComboBox(frame15, values = rlist)
    Combo2.set("")
    Combo2.grid(row=2,column=1)
    Combo3 = CTkComboBox(frame15, values = x)
    Combo3.set("")
    Combo3.grid(row=3,column=1)
    Combo4 = CTkComboBox(frame15, values = ["","Yes","No"])
    Combo4.set("")
    Combo4.grid(row=4,column=1)
    searchButton=CTkButton(window3,text="Search",command=lambda:[searchFunction(entryM,entryH,Combo1,Combo2,Combo3,Combo4)])
    searchButton.pack()
    window3.mainloop()
#η συνάρτηση που εμφανίζει τα αποτελέσματα το query ερωτήματος
def querysearch(query):
    g.parse('D:/Project/Overstock.owl')
    try:
        results=g.query(query)
    except:
        tkinter.messagebox.showinfo("Error!",  "Something wrong with the query. Try again!!")
        return
    window6=CTk()
    window6.resizable(width = 100, height = 100)
    window6.title("Query Results!!")
    treev = ttk.Treeview(window6, selectmode ='browse')
    treev.pack(side ='top',expand=True, fill='both')
    verscrlbar = ttk.Scrollbar(window6,orient ="vertical",command = treev.yview)
    treev.configure(xscrollcommand = verscrlbar.set)
    columns=[]
    columns_number=[]
    temp=1
    for i in results.vars:
        columns.append(str(i)) 
        columns_number.append(str(temp))
        temp=temp+1 
    treev["columns"]=columns_number
    treev['show'] = 'headings'
    for i in columns_number:
        if i=="1":
            treev.column("1", width = 120, anchor ='c')
        else:
            treev.column(i, width = 120, anchor ='se')
    temp=1
    for i in columns:
        treev.heading(str(temp), text =i)
        temp=temp+1
    for i in results:
        values=[]
        for y in columns:
            values.append(str(i[y]).replace("http://test.org/onto.owl#",""))
        treev.insert("", 'end', text ="L1",values =values)   
    window6.mainloop()
#η παρακάτω εντολή εκτελείται όταν πατηθέι το κουμπί queries στο κεντρικό μενού. Γραφική διεπαφή που
#επιτρεπι στον χρήστη να εκτελεί query ερωτήματα
def querymenu():
    window5=CTk()
    window5.title("Queries Menu!!")
    window5.geometry('550x350')
    window5.resizable(width=False, height=False)
    labelQuery=CTkLabel(window5,text="Query = ",font=("Arial", 17)).grid(row=1,column=0)
    e4 = Text(window5,width=50,height=18)
    e4.grid(row=1,column=1,columnspan=3,pady=10)
    CTkButton(window5,text="Search",text_color="white",command=lambda: [querysearch(e4.get("1.0",'end-1c')),window5.destroy()]).grid(row=3,column=2)
    window5.mainloop()
#Παρακάτω ακολουθει ο κώδικας για το layout του κεντρικού μενού. Αποτελέιται από έναν τίλτο και τέσσερα
#κουμπιά HomeItems/Transactions/Customers/Employments
window = CTk()
window.title("Welcome to Overstock Ontology!!")
window.geometry('550x450')
window.resizable(width=False, height=False)
label=CTkLabel(window,text="============= Overstock Ontology =============",font=("Arial", 25))
button1=CTkButton(window,text="Home Items",font=('Ariel', 23),text_color="white",command=lambda: homeItems(listmadein))
button2=CTkButton(window,text="Transactions",font=('Ariel', 23),text_color="white",command=lambda: empcust("Transaction","None"))
button3=CTkButton(window,text="Employees",font=('Ariel', 23),text_color="white",command=lambda: empcust("Employee","None"))
button4=CTkButton(window,text="Customers",font=('Ariel', 23),text_color="white",command=lambda: empcust("Customer","None"))
button5=CTkButton(window,text="Queries",font=('Ariel', 23),text_color="white",command=lambda: querymenu())
label.pack(pady=18),button1.pack(pady=18),button2.pack(pady=18),button3.pack(pady=18),button4.pack(pady=18),button5.pack(pady=18)
window.mainloop()
