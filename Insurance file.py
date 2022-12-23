# -*- coding: utf-8 -*-
"""Insuracnce file.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/18QtHMcSO56BeKtjSlYqstxGVoPJtOa8v
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import seaborn as sns
from tqdm import tqdm

!pip install -q dtreeviz

from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import Lasso, ElasticNet

from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import KFold

from plotnine.data import mpg

import itertools
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re

# wizualizacja drzew decyzyjnych
from sklearn import tree
from dtreeviz.trees import dtreeviz

#1 Wczytanie danych

dataset_name = "insurance.csv"
path_to_data = dataset_name
df = pd.read_csv(path_to_data)
df.head(5)

#2
df.dtypes

#2
df_missing_values = df.isnull().sum()
df_missing_values

df.head(5)

df.region.unique()

df["sex"] = pd.factorize(df['sex'])[0]
df["region"] = pd.factorize(df['region'])[0]
df["smoker"] = pd.factorize(df['smoker'])[0]

df.head(5)

#2 Wykresy oraz korelacja 

# wykresy

for feature_name in df.columns:
  if feature_name != "Charges":
    df[feature_name]

plt.clf()
fig, ax = plt.subplots(3, 3)

for counter, feature_name in enumerate(df.columns):
  i = counter // 3
  j = counter % 3

  if feature_name != "charges":
    ax[i, j].scatter(df[feature_name], df["charges"])
    
    ax[i, j].set_xlabel(feature_name, fontsize=15)
    ax[i, j].set_ylabel("charges", fontsize=15)
    ax[i, j].set_title(f"{feature_name} vs charges", fontsize=14)

fig.set_size_inches((30, 30))
plt.show()

# macierz korelacji
plt.figure(figsize=(10, 10))
corr_chart = sns.heatmap(df.corr(), cmap="RdYlGn", annot=True)

#3 podzielenie cech na zależne i niezależne feature_names oraz zależne target_name

target_name = 'charges'
feature_names = df[[col for col in df.columns if col not in ['charges']]]

df_target = df['charges']
df_features = feature_names

# utworzenie niezbędnych macierzy
X = df_features.to_numpy()
Y = df_target.to_numpy()

print(X.shape,Y.shape)

# podział na dane treningowe i testowe korzystają z metody train_test_split dla splitu 0.2 , 80% treningowe i 20% testowe
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state=50)
print(X_test.shape, X_train.shape)

# 4 Eskploracja danych i wizualizacja

def extract_x_y_from_df(x_cols=None, y_col=None, df=None):

  x_values = df[x_cols].to_numpy()
  y_values = df[y_col].to_numpy()

  # zmiana wymiarów macierzy (przypadek pojedynczej cechy)
  if x_values.ndim == 1:
    x_values = x_values.reshape(-1, 1)
  
  return x_values, y_values

x_cols = 'age'
y_col = 'charges'
x_values, y_values = extract_x_y_from_df(x_cols, y_col, df)

print(x_values.shape)
print(y_values.shape)

fig, ax = plt.subplots()
ax.scatter(x_values, y_values, zorder=3)
ax.set_xlabel(x_cols[0])
ax.set_ylabel(y_col)
ax.set_title("Samples visualization for insurance dataset")
ax.grid(zorder=0)
plt.show()

sns.lmplot(data = df, x='age', y='charges', hue='smoker',fit_reg=False)

# 4.2 Normalizacja danych

#for feature_name in df:
  #if feature_name != "charges":
    #df[feature_name] = (df[feature_name] - df[feature_name].mean()) / df[feature_name].std()

# 4.3 Podział zbioru na dane treningowe i testowe

from sklearn.model_selection import train_test_split

df_train, df_test = train_test_split(df, test_size=0.3)
print(f"{len(df_train)} {len(df_test)}")

x_values_train, y_values_train = extract_x_y_from_df(x_cols, y_col, df_train)
x_values_test, y_values_test = extract_x_y_from_df(x_cols, y_col, df_test)

print(f"{x_values_train.shape} {x_values_test.shape}")

fig, ax = plt.subplots()
ax.scatter(x_values_train, y_values_train, label="train", zorder=3, alpha=0.5)
ax.scatter(x_values_test, y_values_test, label="test", zorder=3, alpha=0.5)
ax.set_xlabel(x_cols[0])
ax.set_ylabel(y_col)
ax.set_title("Samples visualization for insurance dataset")
ax.legend()
ax.grid(zorder=0)

#6 Prosta regresja liniowa

reg = LinearRegression()
reg.fit(x_values_train, y_values_train)

# wyznaczenie przewidywanych wartości dla wizualizacji linii regresji
x_min = np.min(x_values_train)
x_max = np.max(x_values_train)
x_interval_values = np.arange(x_min, x_max, 0.01).reshape(-1, 1)
y_pred_values = reg.predict(x_interval_values)

# wizualizacji linii regresji
fig, ax = plt.subplots()
ax.scatter(x_values_train, y_values_train, label="train", zorder=3, alpha=0.5)
ax.scatter(x_values_test, y_values_test, label="test", zorder=3, alpha=0.5)
ax.plot(x_interval_values, y_pred_values, label="regression line", color="red", linestyle="--", zorder=3)
ax.set_xlabel(x_cols[0])
ax.set_ylabel(y_col)
ax.set_title("Regression for insurance dataset")
ax.legend()
ax.grid(zorder=0)

# 12.4. Podział zbioru danych na zmienne niezależne (cechy, features) oraz zależne (targets)

feature_names = ['smoker']
target_name = 'charges'
df_features = df[[col for col in df.columns if col in feature_names]] 
df_targets = df[[col for col in df.columns if col == target_name]] 
print(df_features.head(5))
print(df_targets.head(5))

# 12.5. Zamiana pandas series na macierze numpy

X = df_features.to_numpy()
Y = df_targets[target_name].to_numpy()
print(f"{X.shape} {Y.shape}")

#6 Trenowanie modelu regresyjnego (model drzewa decyzyjnego)

reg_tree = DecisionTreeRegressor(max_depth=3)
reg_tree.fit(X, Y)

#6.2 Wizualizacja modelu drzewa

fig = plt.figure(figsize=(25, 20))
_ = tree.plot_tree(reg_tree, feature_names=['smoker'], filled=True)

# drzewo decyzyjne ogólnie jak wygląda dla  max_depth=3
first_tree = DecisionTreeRegressor(max_depth=3)
first_tree.fit(X_train, Y_train)

fig = plt.figure(figsize=(20, 20))
new_plot = tree.plot_tree(first_tree, feature_names=df.columns[:-1], filled=True)

print(X_train.shape)

from tqdm import tqdm

print(X.shape)

# jakie max_depth najlepszą kroswalidacje =  drzewo o głębokości 10 wydaje się najblizsze regresji linowej
# Obliczenie RMSE - standardowego błedu regresji
# porównanie do regresji liniowej

for depth in range (1,30):
  estimated_tree = DecisionTreeRegressor(max_depth= depth)
  scores = cross_val_score(estimator= estimated_tree, X=X, y=Y, scoring='neg_root_mean_squared_error')
  print(f"depth={depth}\tRMSE={-scores.mean().round(2)}+-{scores.std().round(2)}")

my_regression = LinearRegression()
scores = cross_val_score(estimator= my_regression, X=X, y=Y, scoring='neg_root_mean_squared_error')
print(f"Linear regression \tRMSE={-scores.mean().round(2)}+-{scores.std().round(2)}")

print(feature_names)

# wartości RMSE -- najwazniejsze cechy w range 1-12 czyli najlepiej do depth=10
feature_names= df.columns[:-1]
RMSE_min = dict()
RMSE_min["mean"] = np.inf

max_range = len(feature_names) + 1


for n in range(1, max_range):
  for model in itertools.combinations(feature_names, n):

    df_features = df[[col for col in df.columns if col in model]]

    X = df_features.to_numpy()
    Y = df[target_name].to_numpy()

    for depth in range (1, 12):
      estimated_tree_model = DecisionTreeRegressor(max_depth= depth)
      scores = cross_val_score(estimator= estimated_tree_model, X=X, y=Y, scoring='neg_root_mean_squared_error')
      if abs(scores.mean()) < abs(RMSE_min['mean']): # dlatego jest pierwszy infinity, żeby przeszło, a potem to już w pętli
        RMSE_min["mean"] = -scores.mean()
        RMSE_min["std"] = scores.std()
        RMSE_min["features"] = model
        RMSE_min["max_depth"] = depth
        RMSE_min["features_importances"] = estimated_tree_model.fit(X, Y).feature_importances_
        RMSE_min["model_opt"] = estimated_tree_model
      i += 1        


fig, ax = plt.subplots()
ax.bar(RMSE_min["features"] , RMSE_min["features_importances"], zorder=3)
ax.set_ylabel("feature_importances")
ax.set_title("Most important features for insurance charge")
ax.grid(zorder=0)

print(f"depth={depth}\tRMSE={-scores.mean().round(2)}+-{scores.std().round(2)}")

# wykres Happiness Score - GDP oraz Happicess Score - Social Support

fig, ax = plt.subplots(1,3)

 
ax[0].scatter(data=df,x="age",y="charges")
ax[0].set_title("charges VS Age")
ax[0].set_xlabel("age")
ax[0].set_ylabel("charges")

 
ax[1].scatter(data=df,x="bmi",y="charges")
ax[1].set_title("charges VS bmi")
ax[1].set_xlabel("bmi")
ax[1].set_ylabel("charges")
ax[2].scatter(data=df,x="smoker",y="charges")
ax[2].set_title("charges Vs smoker")
ax[2].set_xlabel("Smoker")
ax[2].set_ylabel("charges")

fig.set_size_inches(14,8)