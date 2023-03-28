# Overstock-Ontology

In the context of a thesis, an ontology of semantic knowledge was created for household objects, called Overstock. The first step in the implementation is the creation of a complete and sufficient dataset. The data for the items was retrieved from the online store Overstock.com, using the method of scrapping. We managed to collect 20,012 household items and every item has 11 characteristic-columns: id, title, price, rating, reviews, brand, colors, image,warranty in days, made in country, if assemply needed and material. 

![s](https://user-images.githubusercontent.com/128267473/228316134-2ebc1595-fcf1-4b19-b32a-4506dad78589.png)
Pict-1: E-shop of home items Overstock.com

Overstcok-Scrapping.py: contains the python source file for the scrapping method

Overstock-Dataset.csv: the dataset of the household items (20.012 items)

![δδδδ](https://user-images.githubusercontent.com/128267473/228316873-11ff2618-18da-4fe5-a309-2bb94df9fef6.png)

Pict-2: Example of 3 items in Overstock-Dataset.csv

=== Creation of the Overstock Ontology =======

Second step in the implementation is to create and populate the ontology using the Overstock-Dataset.csv. The file Creating-Ontology.py is the python source code that implements the creation and the file Overstock-Population.py implements the polulation part. For more complex functions, the ontology has been enriched with classes whose instances represent customers, employees and transactions. The population part only applies to home object instances. The creation of instances for classes Transaction, Customer, Employee,  is implemented in the retrieval and modification mechanism in the next step.

![image2](https://user-images.githubusercontent.com/128267473/228058762-ac581908-425d-4c3b-ad05-7b5e4db8c90d.png)

Pict-3: Visualization of Overstock ontology using Protégé software

![image1](https://user-images.githubusercontent.com/128267473/228059638-5a145707-851c-48c9-aa24-cd186258819b.png)
Pict-4: Visualization of Overstock ontology's main classes with properties
