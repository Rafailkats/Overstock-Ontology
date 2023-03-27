from owlready2 import *
import csv

onto=get_ontology("D:\Project\Overstock.owl").load()
with open('Overstock-Dataset.csv') as csv_file:
    csv_reader = csv.reader(csv_file)
    with onto:
        for row in csv_reader:
            if len(row)==0:
                continue
            if row[0]=="ID":
                continue
            temp=row[12].split('/')
            temp=temp[len(temp)-1]
            new_individual=onto[temp](row[0],hasTitle=row[1],hasPrice=float(row[2].replace(" EUR","")),hasBrand=row[3]
                                      ,hasRating=float(row[4]),hasReviews=int(row[5]),hasMaretial=row[6],hasColor=row[7],hasMadeIn=row[9],
                                      hasWarrantyDays=int(row[10]),hasImage=row[11]) 
            if "No" in row[8]:
                new_individual.hasAssemblyNeeded=False
            else:
                new_individual.hasAssemblyNeeded=True
           
onto.save("Overstock.owl",format="rdfxml")