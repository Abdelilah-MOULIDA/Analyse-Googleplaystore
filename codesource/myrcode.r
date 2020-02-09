#importing packages to use
library(dplyr)
library(plyr)
library(ggplot2)
library(reshape2)
options(warn=-1)
library(tidyverse)
library(magrittr)
library(readr)
library(stringr)
library(scales)

# Loading the Data
df = read.csv("/Users/abdelilahmoulida/Desktop/googleplaystore/googleplaystore.csv")

# 5 premières rows du dataframe
head(df)

# dimensions
dim(df)
print("10841 observations and 13 variables")

# Résumez les différentes variables afin que nous ayons une idée de ce avec quoi nous travaillons
summary(df)

# enlevement de la category 1.9
df = subset(df, Category != '1.9')

# traçage d'un bar graph pour Categories
ggplot(aes(x = Category), data = df)+geom_bar(fill = 'royalblue2')+coord_flip()+ggtitle("Categories")

# la médiane
med = median(subset(df$Rating, df$Rating >= 0.01))

# histogramme pour la distribution des Rating dans le jeu de données
ggplot(aes(x = Rating), data = df )+
  geom_histogram(binwidth = 0.1, fill = 'violetred2')+
  xlim(1,5)+ 
  geom_vline(xintercept = med, col = 'blue')+
  ggtitle('Rating')

summary(df$Rating)

print("Nombre d'applications avec notes complètes: ") 
count(df$Rating[df['Rating'] == 5 ])

# changement de la colonne Reviews en numbers
df$Reviews = as.numeric(df$Reviews)

# Histogramme
ggplot(aes(x = Reviews), data = df)+ 
  geom_histogram(fill = 'violetred2', bins=30)+
  scale_x_log10()+
  geom_vline(xintercept = median(df$Reviews), color = 'blue')+
  ggtitle('Reviews')

# summary
summary(df$Reviews)

#str(df$Type)
#summary(df$Type)
## There is one row with NaN value, let's check this row
#df[df$Type=='NaN',]
## As shown, price of this app is equal to 0 which means the App is Free
## change the value of Type to Free
#df[df$Type=='NaN',]$Type <- 'Free'

ggplot(df[unique(df$App),], aes(x = Type, fill = Type)) +
  geom_bar() +
  geom_text(stat='count', aes(label=..count..), vjust=-1) +
  labs(title = "Nombre d'apps par Type") +
  guides(fill = FALSE)

# il y a de types paid and free
df_type = subset(df, (Type == 'Free' | Type == 'Paid'))

temp <- df_type%>%
  group_by(Type)%>%
  dplyr::summarise(n = n())

# piechart
ggplot(aes(x = '', y = n, fill = Type), data = temp )+
  geom_bar(stat = 'identity')+
  coord_polar('y', start = 0)+
  theme_void()+
  ggtitle('Type')

# enlevement du caractère $
df$Price = as.numeric(gsub("\\$", "", df$Price))

ggplot(aes(x = Price), data = df) + 
    geom_histogram(fill = 'royalblue2', binwidth = 3)+
    scale_y_log10()+ggtitle('Price')

# barplot
ggplot(aes(x = Content.Rating), data = df)+
  geom_bar(fill = 'royalblue2')+
  coord_flip()+
  scale_y_log10()+
  ggtitle('Content Rating')

# création d'un dataset temporaire
temp <-df%>%
  group_by(Android.Ver)%>%
  dplyr::summarise(n = n())

ver_df<-subset(temp, (Android.Ver != 'NaN' & n >10))

# barplot
ggplot(aes(x = Android.Ver, y = n), data = ver_df)+
geom_bar(stat = 'identity', fill = 'royalblue2')+
coord_flip()+
ylab('count')+
xlab('Version Android')+
ggtitle('Version Android')

df_size = subset(df, Size != 'Varies with device')

# enelvement du caractère et conversion en M(/1024)afin d'avoir des valeurs numérique
condition = grepl('M', df_size$Size)
if_true = as.numeric(gsub("[a-zA-Z ]", "" , df_size$Size))
if_false = as.numeric(gsub("[a-zA-Z ]", "", df_size$Size))/1024

df_size$Size = ifelse(condition == TRUE, if_true,if_false)

# plot
ggplot(aes(x = round(Size)), data = df_size)+
  geom_histogram(fun.y = count, geom ='line', fill = 'violetred2', bins=30)+
  geom_vline(xintercept = median(subset(df_size,!is.na(df_size$Size))$Size), col = 'red')+
  geom_vline(xintercept = mean(subset(df_size,!is.na(df_size$Size))$Size), col = 'blue')+
  ggtitle('Size')+
  xlab('Size')

# Plotting les Genres des apps les plus populaires

# groupement des Genres pour trouver celui le plus fréquent 
topgenres = group_by(df, Genres)%>%
  dplyr::summarise(n = n())%>%
  arrange(desc(n))

# enlevement des Genres moins fréquent
# la variable topgenres je vais l'utiliser dans l'anlyse bivariés
topgenres = head(topgenres,15)
mask= df$Genres %in% topgenres$Genres
topgenres = df[mask,]

# barplot
ggplot(aes(x = Genres), data = topgenres)+
  geom_bar(fill = 'violetred2')+
  coord_flip()+
  ggtitle('Genres')

# Cleaning la colonne Installs
df = subset(df, df$Installs != 'Free')

# plotting a bargraph pour le nombre d'installs pour chaque Level
ggplot(aes(x = Installs), data = df )+geom_bar(fill = 'violetred2')+coord_flip()+ggtitle('Installs')

# rating - reviews
ggplot(aes(y =Reviews, x=Rating), data = df)+
  geom_jitter(alpha = 0.06, color = 'royalblue2')+
  geom_smooth(method = 'lm')+
  ggtitle('Rating - Reviews')

# Rating - Installs
ggplot(aes(x =Installs , y =Rating ), data = df)+
  geom_boxplot(fill = 'violetred2')+
  coord_flip()+
  ggtitle('Rating - Installs')

# Rating - Price
ggplot(aes(x = Rating , y = Price), data = df)+
  geom_jitter(alpha = 0.3, color = 'royalblue1')+
  ylim(0,25)+
  geom_line(stat = 'summary', fun.y = mean)+
  ggtitle('Rating - Price')

# rating vs. type
ggplot(aes(x = Type, y = Rating), data = df_type )+
  geom_boxplot(fill = 'violetred2' )+
  ggtitle('Rating vs. Type')

# summary pour les apps de Type paid
summary(subset(df, Type == 'Paid')$Rating)

# summary pour les apps de Type free
summary(subset(df, Type == 'Free')$Rating)

# j'utilise df_size dataframe que j'ai crée avant dans la section pour l'analyse univarié

# rating - size
ggplot(aes(x =Rating , y =Size ), data = df_size)+
  geom_jitter(alpha = 0.05, color ='royalblue1')+
  geom_smooth(method = 'lm')+
  geom_line(stat = 'summary', fun.y = mean  )+
  ggtitle('Rating - Size')

# correlation entre rating et size
cor.test(df_size$Rating,df_size$Size)

# average rating pour chauque category
dfcat <- subset(df, !is.na(Rating))
dfcat <- dfcat%>%
  group_by(Category)%>%
  dplyr::summarise(Rating = mean(as.numeric(Rating)))

#plot
ggplot(aes(x = Category, y = Rating), data = dfcat)+
  geom_bar(stat="identity", fill = 'violetred2')+
  coord_flip(ylim = c(3.8,4.5))

# enlèvement de toute les lignes qui n'ont pas un rating
topgenres <- subset(topgenres, !is.na(Rating))

# group la colonne topgenres 
topgenres_group <- topgenres%>%
  group_by(Genres)%>%
  dplyr::summarise(Rating = mean(as.numeric(Rating)))

# barplot du mean de rating pour les genres les plus frequent
ggplot(aes(x = Genres, y = Rating), data = topgenres_group)+
  geom_bar(stat = 'identity', position = 'dodge', fill = 'royalblue2')+
  coord_flip(ylim = c((min(topgenres_group$Rating) - 0.1),4.35))+
  ggtitle('Rating - Top Genres')

# point plot
ggplot(aes(x = Genres, y = Rating), data = topgenres)+
  geom_jitter(alpha = 0.3, color = 'royalblue2')+
  coord_flip()+
  ggtitle('Rating - Top Genres')

# création d'un boxplot sans le level unrated dans le Content Rating
ggplot(aes(y = Rating, x = Content.Rating),
       data = subset(df, Content.Rating != 'Unrated'))+
  geom_boxplot( fill = 'royalblue1')+
  ggtitle('Rating - Content Rating')

# plot des differents genres que les categories contiennent
ggplot(aes(x = Category), data = df)+
  geom_bar(aes(fill = Genres))+
  coord_flip()+
  theme(legend.position="none")+
  ggtitle('Genre - Category')

# un dataframe temporaire qui ne sera utilisée qu'une seule fois et qui a le nombre  
# des applications de chaque genre qui composent la catégorie Game
temp <- subset(df, Category == 'GAME')%>%
  group_by(Genres)%>%
  dplyr::summarise(n = n())

# plot
ggplot(aes( x = Genres, y = n), data = temp)+
  geom_bar(stat = 'identity', fill = 'tomato')+
  coord_flip()+
  geom_text(aes(label = n), hjust = -0.1)+
  ggtitle("Genre dans la Category Game")+
  ylab('count')

# un dataframe temporaire qui ne sera utilisée qu'une seule fois et qui a le nombre  
# des applications de chaque genre qui composent la catégorie Family
temp <- subset(df, Category == 'FAMILY')%>%
  group_by(Genres)%>%
  dplyr::summarise(n = n())

temp<- temp[order(temp$n, decreasing = TRUE),]
temp <- head(temp, 20)

# plot
ggplot(aes( x = Genres, y = n), data = temp)+
  geom_bar(stat = 'identity', fill = 'tomato')+
  coord_flip()+
  geom_text(aes(label = n), hjust = -0.1)+
  ggtitle("Genre dans la Category Family")+
  ylab('count')

# plot de topgenres et category
ggplot(aes (x = Genres), data = topgenres)+
  geom_bar(aes(fill = Category))+
  coord_flip()+
  ggtitle('Top genres et Category')

# plot de category par type 
ggplot(aes(x= Category), data = df)+
  geom_bar(aes(fill = Type))+
  coord_flip()+
  ggtitle('Category - Type')

# plot du nbr d'Installs par Category
ggplot(aes(x = Installs), data = df)+
  geom_bar(aes(fill = Category))+
  coord_flip()+
  theme(legend.position="none")+
  ggtitle('Installs par Category')

# Installs - Reviews
# temporaire dataset où on groupe le nbr d'Installs
temp <- df%>%
  group_by(Installs)%>%
  dplyr::summarise(mean = mean(Reviews), median = median(Reviews), max = max(Reviews),
            n = n())

ggplot(aes(x=Installs, y = Reviews), data = df)+
  geom_jitter(alpha = 0.05, color = 'violetred2')+
  coord_flip()+
  ggtitle('Install - Reviews')

#install vs. mean reviews
ggplot(aes(x = Installs, y = mean), data = temp)+
  geom_bar(stat = 'identity', fill = 'royalblue2')+
  coord_flip()+
  geom_text(aes(label = n), hjust = -0.1)+
  ggtitle('Installs - mean no. de Reviews')+
  ylab('mean reviews')

ggplot(aes(x = Category), data = df)+
  geom_bar(aes(fill = Content.Rating))+
  coord_flip()+
  scale_y_log10()+
  ggtitle('category - content rating')

# Android.ver avec plus de 1000 applications
ver_df2 = subset(ver_df, n >1000)

# plot
ggplot(aes(x= Installs, y = Reviews), data = subset(df, df$Android.Ver %in% ver_df2$Android.Ver))+
  geom_jitter(aes(color = Android.Ver), alpha = 0.5)+
  coord_flip()+
  ggtitle('Installs, Reviews et Android.Ver')

####### IL FAUT UN CLEAN POUR QUE ÇA MARCHE

# sous-ensemble pour Type
paidapp <- subset(df, Type == "Paid")

paidappgroup <- paidapp%>%
  group_by(Category)%>%
  dplyr::summarise(mean_Price = mean(Price), n = n(), median_Price = median(Price))

# Category - mean_price
ggplot(aes(x =Category, y =mean_Price ), data = paidappgroup)+
  geom_bar(stat = 'identity', position = 'dodge', fill = 'royalblue1')+
  coord_flip()+
  geom_text(aes(label = n), hjust=-0.1)+
  ggtitle('Category - mean price')

# Relation entre la median de Price et category
ggplot(aes(x =Category, y = median_Price ), data = paidappgroup)+
  geom_bar(stat = 'identity', position = 'dodge', fill = 'tomato')+
  coord_flip()+
  geom_text(aes(label = n), hjust=-0.1)+
  ggtitle('Median price - Category')

# relation entre price et category lors de la comptabilisation du type
ggplot(aes(y = Price, x = Category), data = paidapp)+
  geom_point(alpha = 0.2, color = 'tomato')+
  coord_flip()+
  scale_y_log10()+
  ggtitle('Price - Category')

# Regardons l'app la plus cher dans la category Finance
temp <- head(subset(df, Category == 'FINANCE' & Type == 'Paid'))%>%
  select(App, Category, Price, Genres)

outliers <- temp[order(temp$Price, decreasing = TRUE),]%>%
  head(5)

outliers

# Regardons l'app la plus cher dans la category LifeStyle
temp <- subset(df, Category == 'LIFESTYLE' & Type == 'Paid')%>%
  select(App, Category, Price, Genres)

temp[order(temp$Price, decreasing = TRUE),]%>%
  head(5)

# check the app in the events category
subset(df, Category == 'EVENTS' & Type == 'Paid')%>%
  select(App,Category,Price, Genres)

ggplot(df, aes(x=Rating, y=Category)) +
  geom_segment(aes(yend=Category), xend=0, colour="grey50") +
  geom_point(size=1, aes(colour=Type)) +
  scale_colour_brewer(palette="Set1", limits=c("Free", "Paid"), guide=FALSE) +
  theme_bw() +
  theme(panel.grid.major.y = element_blank()) +
  facet_grid(Type ~ ., scales="free_y", space="free_y") +
  ggtitle("Category qui a la Rating la plus élevée entre les applications Free et Paid")

ggplot(df, aes(x= Category, y= Rating, fill = Type)) +
  geom_bar(position='dodge',stat='identity') +
  coord_flip() +
  ggtitle("Nombre de App Rating basées sur Category et Type")

ggplot(df, aes(x= Category, y= Reviews, fill = Type)) +
  geom_bar(position='dodge',stat='identity') +
  coord_flip() +
  ggtitle("Nombre de App Reviews basées sur Category et Type")
