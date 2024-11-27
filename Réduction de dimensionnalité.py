#!/usr/bin/env python
# coding: utf-8

# In[7]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

df =pd.read_csv('nettoyer.csv')
print(df.describe())
print(df.isnull().sum())

plt.figure(figsize=(10, 6))
sns.histplot(data=df, x='accords_avis')
plt.title('Distribution des accords')
plt.show()


# In[8]:


vectorizer= TfidfVectorizer(max_features=1000, ngram_range=(1, 2))
X =vectorizer.fit_transform(df['review'])

df['sentiment_binaire']= df['accords_avis'].apply(lambda x: 1 if x > df['accords_avis'].median() else 0)
y =df['sentiment_binaire']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model =LogisticRegression()
model.fit(X_train, y_train)

predictions= model.predict(X_test)


pipeline = Pipeline([
    ('vectorizer', TfidfVectorizer()),
    ('classifier', LogisticRegression())
])

parameters ={
    'vectorizer__max_features': [1000, 2000],
    'vectorizer__ngram_range': [(1, 1), (1, 2)],
    'classifier__C': [0.1, 1, 10]
}

grid_search = GridSearchCV(pipeline, parameters, cv=5)
grid_search.fit(df['review'], y)

tsne = TSNE(n_components=2, random_state=42)
X_tsne = tsne.fit_transform(X.toarray())

print("Meilleurs paramètres:", grid_search.best_params_)
print("Meilleur score:", grid_search.best_score_)
print(classification_report(y_test, predictions))
plt.figure(figsize=(12, 8))
scatter = plt.scatter(X_tsne[:, 0], X_tsne[:, 1], c=y, cmap='viridis')
plt.colorbar(scatter)
plt.title('Visualisation t-SNE des reviews')
plt.show()

