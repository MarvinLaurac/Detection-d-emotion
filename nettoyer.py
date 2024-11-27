#!/usr/bin/env python
# coding: utf-8

# In[38]:


import pandas as pd
import re
df =pd.read_csv('reviews_all_pages.csv')
df = df.drop_duplicates(subset='review')

def nettoyer_texte_complet(texte):
    texte= str(texte).lower()
    texte= re.sub(r'[^\w\s]', ' ', texte)
    texte= re.sub(r'\d+', '', texte)
    texte= re.sub(r'\s+', ' ', texte)
    texte= texte.strip()
    
    mots= texte.split()
    mots_filtres = [mot for mot in mots if len(mot) > 1]
    texte= ' '.join(mots_filtres)    
    return texte

def convertir_date(date_str):
    date_str = date_str.replace('Posté le ', '')
    date_part = date_str.split(' à ')[0]
    date_part = date_part.replace('.', '')
    
    try:
        jour, mois, annee= date_part.split(' ')
        mois_fr= {
            'janv': '01', 'févr': '02', 'mars': '03', 'avr': '04',
            'mai': '05', 'juin': '06', 'juil': '07', 'août': '08',
            'sept': '09', 'oct': '10', 'nov': '11', 'déc': '12'
        }
        
        mois_num = mois_fr[mois.lower()]
        return f"{jour.zfill(2)}/{mois_num}/{annee}"
    except Exception as e:
        return date_str

df['review']= df['review'].apply(nettoyer_texte_complet)
df['dates'] =df['dates'].apply(convertir_date)

#df.to_csv('nettoyer.csv', index=False)
#df.head()

