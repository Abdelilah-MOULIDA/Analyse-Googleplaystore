#!/usr/bin/env python
# coding: utf-8

# 

# # Analyse du jeux de données de Google PlayStore avec Python

# > ## Importation des packages nécessaires : 

# In[241]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ignorer l'affichage des warnings
import warnings
warnings.filterwarnings( 'ignore' )

# linear regression
#import the libraries
get_ipython().run_line_magic('matplotlib', 'inline')
from sklearn.model_selection import train_test_split
from sklearn import linear_model

# Importing all necessary libraries
import scipy.stats as stats
get_ipython().run_line_magic('matplotlib', 'inline')


# > ## Lecture des données :

# In[242]:


# importation du dataset, affichage de ses 1ères lignes
df = pd.read_csv( "/Users/abdelilahmoulida/Desktop/googleplaystore/googleplaystore.csv" )
df.head()


# > ## Traitement des données : 
# ### <b style="font-size:14pt;">Gestion des valeurs NULL :</b>

# <i><u><b style="font-size:14pt;">Remarque :</b></u> <b style="font-size:12pt;">nombreuses valeurs NULL dans Rating, et quelques-unes dans Type, Current Ver et Avdroid Ver.</b></i>

# In[243]:


# affichage du nombre de valeur NULL par colonne
print( df.isnull().sum() )

# suppression des colonnes avec des valeurs NULL
df.dropna( inplace = True ) 

df.shape


# In[244]:


# suppression des doublons
df.drop_duplicates(inplace=True)


# In[245]:


# dimension du data set : 8886 lignes et 13 colonnes
df.shape


# ### <b style="font-size:14pt;">Gestion des types de données :</b>

# In[246]:


# affichage des types de données de chaque colonnes du dataset
df.info()
df.dtypes


# <i><b style="font-size:14pt;">Les <u>types de données</u></b> <b style="font-size:12pt;">doivent être modifiés dans un format approprié pouvant être utilisé pour l'analyse.<br>
# </b></i><b><i style="font-size:14pt;"><u>Reviews</u></i></b> <b style="font-size:12pt;"><i>doit être de type numérique.</i></b><b><i style="font-size:14pt;"> <u>Size</u>, <u>Installs</u>, <u>Price</u> et <u>Android Vers</u></i></b> <b style="font-size:12pt;"><i>doivent également être de type numérique. Leurs valuers doivent être modifiées dans un format approprié afin que nous puissions les utiliser pour l’analyse et les graphiques.</i></b>

# <b><i style="font-size:14pt;"><u>Reviews</u> :</i></b>

# In[247]:


# conversion du type de "Reviews" de 'object' vers 'int64'
df.Reviews = df.Reviews.astype('int64')


# In[248]:


df.dtypes


# <b><i style="font-size:14pt;"><u>Size</u> :</i></b>

# \pagebreak

# In[249]:


# nouvelle valeur de la varaible Size
newSize = []

for row in df.Size:
    # enlevement du caractere M
    newrow = row[:-1]
    try:
        newSize.append(float(newrow))
    except:
        newSize.append(0)

# la nouvelle colonne Size
df.Size = newSize

df.Size.head()


# <b><i style="font-size:14pt;"><u>Installs</u> :</i></b>

# In[250]:


# nouvelle valeur de la variable Size
newInstalls = []

for row in df.Installs:
    # enlevement du signe $
    row = row[:-1]
    
    # enlevement de la ,
    newRow = row.replace(",", "")
    newInstalls.append(float(newRow))
    
# la nouvelle colonne Installs
df.Installs = newInstalls

df.Installs.head()


# <b><i style="font-size:14pt;"><u>Price</u> :</i></b>

# \pagebreak

# In[251]:


newPrice = []

for row in df.Price:
    if row!= "0":
        # si l'application est payante on l'attribue la valeur 1
        newrow = float(row[1:])
    else:
        # 0 pour les applications non payante
        newrow = 0 
        
    newPrice.append(newrow)
        
df.Price = newPrice

df.Price.head()


# <b><i style="font-size:14pt;"><u>Android Ver</u> :</i></b>

# In[252]:


newVer = []

for row in df['Android Ver']:
    try:
        newrow = float(row[:2])
    except:
        # quand la valeur de la colonnes est - Varies with device
        newrow = 0  
    
    newVer.append(newrow)
    
df['Android Ver'] =  newVer

df['Android Ver'].value_counts()


# > ## Statstiques descriptives :
# ### <b style="font-size:16pt;">Analyses univariés : </b>

# <b><i style="font-size:14pt;">Variable <u>Catégorie</u> :</i></b>

# In[253]:


# affichage de toutes les catégories et de leurs comptes
df.Category.value_counts()


# In[254]:


df.Category.value_counts().plot(kind='barh',figsize= (12,8))


# In[255]:


# pie chart pour afficher la distribution des applications dans différentes catégories
fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(aspect="equal"))
number_of_apps = df["Category"].value_counts()
labels = number_of_apps.index
sizes = number_of_apps.values
ax.pie(sizes,labeldistance=2,autopct='%1.1f%%')
ax.legend(labels=labels,loc="right",bbox_to_anchor=(0.9, 0, 0.5, 1))
ax.axis("equal")
plt.show()


# > <b><i style="font-size:14pt;">Le nombre maximal d'applications appartient à la catégorie Famille et Game.</i></b>

# <b><i style="font-size:14pt;">Variable <u>Rating</u> :</i></b>

# In[256]:


df.Rating.describe()


# <b><i style="font-size:12pt;">Diagramme de distribution de Rating : </i></b>

# In[257]:


plt.figure(figsize=(15,5))
sns.countplot(x='Rating',data=df)


# In[258]:


sns.distplot(df.Rating)


# > <b><i style="font-size:14pt;">Remarque : la plupart des applications ont clairement un Rating supérieure à 4.0 et beaucoup semblent avoir un Rating : 5.0.</i></b>

# In[259]:


print("Nombre d'applications avec notes complètes: ",df.Rating[df['Rating'] == 5 ].count())


# > <b><i style="font-size:14pt;">Il y a 271 applications dans qui ont eu un Rating de 5.0. Est-ce que tout cela le mérite réellement ? Ou est-ce que ces évaluations sont spammées ? Analysons plus loin dans la statistique multivariés </i></b>

# <b><i style="font-size:14pt;">Variable <u>Reviews</u> :</i></b>

# <b><i style="font-size:12pt;">Diagramme de distribution de Reviews : </i></b>

# In[260]:


plt.figure(figsize=(10,5))
sns.distplot(df.Reviews)


# <b><i style="font-size:12pt;">Examinons ces applications qui ont un bon nombre de 'Reviews' : </i></b>

# In[261]:


# affichage des application qui ont plus de 40 000 000 Reviews
df[df.Reviews>40000000]


# > <b><i style="font-size:14pt;">Remarque : Les applications les plus célèbres telles que WhatsApp, Facebook et Clash of Clans sont les applications les plus Reviewed, comme indiqué ci-dessus. </i></b>

# In[262]:


df['Reviews']=df['Reviews'].astype(int)


# In[263]:


top5reviews=df.nlargest(15,'Reviews')
top5reviews = top5reviews.sort_values(by='Reviews', ascending=False).drop_duplicates('App')
top5reviews.plot(x='App',y='Reviews', kind='bar')
plt.xlabel('Applications')
plt.ylabel('Reviews')
plt.title('Top 5 Applications les plus Reviewed')


# <b><i style="font-size:14pt;">Variable <u>Type</u> :</i></b>

# In[264]:


# pourcentage des application 'Paid' et celle 'Free'
plt.pie(df.Type.value_counts(), labels=['Free', 'Paid'], autopct='%1.1f%%')


# > <b><i style="font-size:14pt;">Remarque : 93.1% des applications sont gratuites dans le Play Store et seulement 6.9% qui sont payantes</i></b>

# <b><i style="font-size:14pt;">Variable <u>Price</u> :</i></b>

# In[265]:


# regardeons de plus près les applications avec un Price de plus de 100$
expensive_apps = df[df["Price"]>100]
expensive_apps["Installs"].groupby(expensive_apps["App"]).sum()


# In[266]:


df[df.Price == df.Price.max()]


# > <b><i style="font-size:14pt;">L'application la plus chère est : I'm Rich - Trump Edition coûte 400$</i></b>

# <b><i style="font-size:14pt;">Variable <u>Content Rating</u> :</i></b>

# In[267]:


df.columns = df.columns.str.replace( 'Content Rating', 'ContentRating' )
g = pd.DataFrame( df.groupby( 'ContentRating' )[ 'ContentRating' ].count() )
cont = list( df.ContentRating.unique() )
cont


# In[268]:


g


# In[269]:


plt.tight_layout()
plt.figure(figsize=(5,5))
plt.pie(g, labels=cont, startangle = -90, autopct = '%.2f%%')


# <b><i style="font-size:14pt;">Variable <u>Android Ver</u> :</i></b>

# In[270]:


df['Android Ver'].value_counts()


# In[271]:


sns.countplot(df['Android Ver'])


# > <b><i style="font-size:14pt;">Remarque: la plupart des applications prennent en charge Android 4.0 et les versions ultérieures.</i></b>

# \pagebreak

# ### <b style="font-size:16pt;">Analyses bivariées : </b>

# <b><i style="font-size:14pt;"><u>Installs</u> par <u>Catégorie</u> :</i></b>

# In[272]:


# une vue sur le nbr d'Installs par Catégorie
# par exemple : regardant le nombre d'installations dans les 5 premières catégories
no_of_apps_category = df["Category"].value_counts()
no_of_apps_category[0:5]
number_of_installs = df["Installs"].groupby(df["Category"]).sum()
print(f"Nombre d'installements dans Family: {number_of_installs.loc['FAMILY']}")
print(f"Nombre d'installements dans Game: {number_of_installs.loc['GAME']}")
print(f"Nombre d'installements dans Tools: {number_of_installs.loc['TOOLS']}")
print(f"Nombre d'installements dans Productivity: {number_of_installs.loc['PRODUCTIVITY']}")
print(f"Nombre d'installements dans Finance: {number_of_installs.loc['FINANCE']}")
      
# traçage d'un graphique à barres simple pour représenter le nombre d'installations dans chaque catégorie.
plt.figure(figsize=(10,8))
sns.barplot(x="Category", y="Installs", data=df, label="Total Installs", color="b")
plt.xticks(rotation=90)
plt.show()


# > <b><i style="font-size:14pt;">Resultats : Les 3 principales catégories en termes de nombre d'installations sont : Communication, lecteurs vidéo et divertissement.</i></b>

# \pagebreak

# <b><i style="font-size:14pt;"><u>Price</u> par <u>Catégorie</u> :</i></b>

# In[273]:


# Regardons pourquoi la famille, même si elle a beaucoup d'applications, n'a pas le plus grand nombre 
# d'installations
# Le prix pourrait être l'un des facteurs
paid_apps = df[df["Price"] != 0.0]

paid_family_apps = paid_apps[paid_apps["Category"]=="FAMILY"]
paid_family_apps.count()

paid_communications_apps = paid_apps[paid_apps["Category"]=="COMMUNICATION"]
paid_communications_apps.count()

# Visualisons ceci sous la forme d'un simple diagramme à barres
plt.figure(figsize=(10,8))
sns.barplot(x="Category", y="Price", data=paid_apps, label="Total des Apps payées dans chaque catégorie")
plt.xticks(rotation=90)
plt.show()


# <b><i style="font-size:14pt;"><u>Rating</u> par <u>Catégorie</u> :</i></b>

# In[274]:


# Ratings of the apps over various categories
# Classement des applications sur différentes catégories
avg_rating = df["Rating"].mean()
print(avg_rating)

plt.figure(figsize=(10,8))
sns.boxplot('Category','Rating',data=df)
plt.title("Distribution des Ratings par Catégorie")
plt.ylabel("Rating")
plt.xlabel("Category")
plt.xticks(rotation=90)
plt.show();


# In[275]:


plt.figure(figsize=(15,15))
sns.barplot(x='Rating', y='Category', data=df)


# <b><i style="font-size:14pt;"><u>Rating</u> par <u>Type</u> :</i></b>

# In[276]:


plt.figure(figsize=(5,5))
plt.tight_layout()
sns.boxplot(x='Type', y='Rating', data=df)


# <b><i style="font-size:14pt;"><u>Installs</u> par <u>Price</u> :</i></b>

# In[277]:


# Paid Vs free et le nombre d'Installs
installs_greater_1000 = df[df["Installs"]>1000]
installs_greater_1000 = installs_greater_1000.sort_values(['Price'])


# In[278]:


plt.figure(figsize=(20,20))
sns.catplot(x="Installs", y="Price",data=installs_greater_1000);
plt.xticks(rotation=90)
plt.show()


# <b><i style="font-size:14pt;"><u>Category</u> par <u>Size</u> :</i></b>

# In[279]:


plt.figure(figsize=(5,15))
sns.barplot(x='Size', y='Category', data=df)


# > <b><i style="font-size:14pt;">Analyses de la variable <u>Installs</u> : dans cette partie on va se consacrer de la variable Installs avec les autres variables</i></b>
# 

# <b><i style="font-size:14pt;">Groupement des nombres d'Installs en 4 groupes : A, B, C, Highest.</i></b>

# In[280]:


n=df.Installs
num=[]

for i in n:
    if i <=100:
        num.append('A')
    elif 101<i<100000:
        num.append('B')
    elif 100001<i<100000000:
        num.append('C')
    else:
        num.append('Highest')

        
df['Group'] = num


# In[281]:


installs=pd.DataFrame(df.groupby('Group')['Group'].agg({'Count':len}).sort_values('Group', ascending=True))


# In[282]:


sns.countplot(x='Group', data=df, palette='husl', order=df['Group'].value_counts().index)
plt.title("Regroupement des applications Installées")


# In[283]:


plt.figure(figsize=(5,5))
sns.barplot(x='Group', y='Rating', data=df, hue='Type', palette='husl')
plt.legend(loc=4)
plt.title('Nombre d\'applications installées et leurs Rating par rapport au type d\'application')


# > <b><i style="font-size:14pt;">Les applications installées en moins grand nombre ont le Rating la plus élevée. Cependant, la majorité des Apps sont gratuites. Nous pouvons conclure que ces applications pourraient être nouvelles et essayées et examinées par un nombre moindre d'utilisateurs.</i></b>

# In[284]:


plt.figure(figsize=(5,5))
sns.barplot(x='Group', y='Reviews', data=df, hue='Type', palette='husl')
plt.legend(loc=0)
plt.title('Groupe d\'applications installées en ce qui concerne les Reviews et le Type')


# > <b><i style="font-size:14pt;">Les utilisateurs sont plus intéressés par les applications gratuites et donc ces applications ont un plus grand nombre de Reviews</i></b>

# In[285]:


plt.figure(figsize=(5,5))
ax=sns.barplot(x='Installs', y='Category', data=df)
plt.xticks(rotation=90)

