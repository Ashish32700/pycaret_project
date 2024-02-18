import pandas as pd
import matplotlib.pyplot as plt
from pycaret.clustering import *
import sys



def create_report(algo,data,scores,s,e,verb):
  e=e+1
  report=pd.DataFrame({},index=scores)
  setup(data,verbose=verb)
  for i in range(s,e):
    create_model(algo,num_clusters=i)
    model=pull()
    model=model.transpose().loc[scores,:]
    model.columns=["Clusters="+str(i)]
    report=pd.concat([report,model],axis=1)
  # print(report)

  setup(data,normalize=True,normalize_method="zscore",verbose=verb)
  for i in range(s,e):
    create_model(algo,num_clusters=i)
    model=pull()
    model=model.transpose().loc[scores,:]
    model.columns=["Clusters="+str(i)+"(normalized)"]
    report=pd.concat([report,model],axis=1)
  # print(report)

  setup(data,transformation=True,transformation_method="yeo-johnson",verbose=verb)
  for i in range(s,e):
    create_model(algo,num_clusters=i)
    model=pull()
    model=model.transpose().loc[scores,:]
    model.columns=["Clusters="+str(i)+"(transformed)"]
    report=pd.concat([report,model],axis=1)
  # print(report)

  setup(data,pca=True,pca_method="linear",verbose=verb)
  for i in range(s,e):
    create_model(algo,num_clusters=i)
    model=pull()
    model=model.transpose().loc[scores,:]
    model.columns=["Clusters="+str(i)+"(pca)"]
    report=pd.concat([report,model],axis=1)

  setup(data,normalize=True,normalize_method="zscore",transformation=True,transformation_method="yeo-johnson",verbose=verb)
  for i in range(s,e):
    create_model(algo,num_clusters=i)
    model=pull()
    model=model.transpose().loc[scores,:]
    model.columns=["Clusters="+str(i)+"(norm+trans)"]
    report=pd.concat([report,model],axis=1)


  setup(data,normalize=True,normalize_method="zscore",transformation=True,transformation_method="yeo-johnson",pca=True,pca_method="linear",verbose=verb)
  for i in range(s,e):
    tuned_model=create_model(algo,num_clusters=i)
    model=pull()
    model=model.transpose().loc[scores,:]
    model.columns=["Clusters="+str(i)+"(norm+trans+pca)"]
    report=pd.concat([report,model],axis=1)
    
  report=report.transpose()
  report.to_csv(str(algo)+r"_report_")

scores=["Silhouette","Calinski-Harabasz","Davies-Bouldin"]
data=pd.read_csv('Your Data_base')
methods_to_use=["kmeans","hclust","ap","meanshift","dbscan","sc"]
starting_num_clusters=2  #min numberof clusters
ending_num_clusters=4  #max number of clusters
verb=False   #verbose=False
for i in methods_to_use:
  create_report(str(i),data,scores,starting_num_clusters,ending_num_clusters,verb)