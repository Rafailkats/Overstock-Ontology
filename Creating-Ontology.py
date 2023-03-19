from owlready2 import *
import csv
import types
onto = get_ontology("http://test.org/onto.owl#")
lines=0
pro=[]
checked=[]
classes=['Overstock','Person','Customer','Employee','Transaction']
fathers=['Thing','Overstock','Person','Person','Overstock']
with open('Overstock-Dataset.csv') as csv_file:
   csv_reader = csv.reader(csv_file)
   for row in csv_reader:
       lines+=1
       if lines==1:
           pro=row[1:13]
       else:
           break   
   for row in csv_reader:
       if lines==1:
           lines=0
           continue
       else:
           if row[12] in checked:
               continue
           else:
               checked.append(row[12])
for x in checked:
    temp=x.split('/')
    for previous,current in zip(temp, temp[1:]):
        if current in classes:
            continue
        else:
            classes.append(current)
            fathers.append(previous)
temp=[]
for x in pro:
    temp.append("has" + x.replace(" ",""))
pro=temp
with onto:
     for (child, father) in zip(classes, fathers):
         if child=="Overstock":
               NewClass=types.new_class(child,(Thing,))
         else:
               NewClass=types.new_class(child,(onto[father],))
     for proper in pro:
         NewProperty= types.new_class(proper, (DataProperty,FunctionalProperty))
         if "Price" in proper or "Rating" in proper:
            onto[proper].domain=[onto["HomeItem"]]
            onto[proper].range=[float]
         elif "Warranty" in proper or "Reviews" in proper:
            onto[proper].range=[int]
            onto[proper].domain=[onto["HomeItem"]]
         elif "Assembly" in proper:
             onto[proper].domain=[onto["HomeItem"]]
             onto[proper].range=[bool]
         else:
             onto[proper].domain=[onto["HomeItem"]]
             onto[proper].range=[str]
     #Person class
     person_pro=['firstName','lastName','phone','email','address']
     for propert in person_pro:
             NewProperty= types.new_class(propert, (DataProperty,FunctionalProperty))
             onto[propert].domain=[onto["Person"]]
             onto[propert].range=[str]
     #transaction class
     NewProperty= types.new_class('totalPrice', (DataProperty,FunctionalProperty))
     onto['totalPrice'].range=[float]
     onto['totalPrice'].domain=[onto["Transaction"]]
     NewProperty= types.new_class('date', (DataProperty,FunctionalProperty))
     onto['date'].range=[str]
     onto['date'].domain=[onto["Transaction"]]
     NewProperty= types.new_class('hasEmployee', (ObjectProperty,FunctionalProperty))
     onto['hasEmployee'].domain=[onto["Transaction"]]
     onto['hasEmployee'].range=[onto["Person"]]
     NewProperty= types.new_class('hasCustomer', (ObjectProperty,FunctionalProperty))
     onto['hasCustomer'].domain=[onto["Transaction"]]
     onto['hasCustomer'].range=[onto["Person"]]
     NewProperty= types.new_class('inItem', (ObjectProperty,))
     onto['inItem'].domain=[onto["Transaction"]]
     onto['inItem'].range=[onto["HomeItem"]]
  
onto.save("Overstock.owl",format="rdfxml")








