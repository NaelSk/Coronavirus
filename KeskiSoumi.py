import requests
import pandas as pd
import matplotlib.pyplot as plt

from datetime import datetime

import seaborn as sns

def split_date1(df):
    #Split one colum according to space
    new=df.Päiväys.str.split("-",expand=True)
    df["Date"]=new[0]
    df2=df.astype({"Date":str})
     
    df3=df2.drop(columns="Päiväys")

    new=df3.Date.str.split(".",expand=True)
    df3["Day"]=new[0]
    df3["Month"]=new[1]
    df3["Year"]=new[2]
    df4=df3.drop(columns="Date")
    #print(df4)
    return df4


def data_collecter():
    url = 'https://korona.kans.io/'
    html = requests.get(url).content
    df_list = pd.read_html(html)
    df = df_list[-1]
    processed_data=split_date1(df)
    return processed_data#(processed_data.to_csv('my data.csv'))


def data_city(df,city):
    mask=df["Sair.hoitopiiri"]==city
    return df[mask]


def grouping(df):
    groups=df.groupby(["Year","Month","Day"]).size().reset_index(name ='number_of_infection')
    groups=groups.astype(int)
    
    groups['Date'] = groups.apply(lambda row: datetime.strptime(f"{int(row.Year)}-{int(row.Month)}-{int(row.Day)}", '%Y-%m-%d'), axis=1)
    
    groups=groups.drop(columns=["Year", "Month", "Day"])

    total_number=groups["number_of_infection"].sum()
    total="Totale"+str(total_number)
    
    plt.bar(groups["Date"], groups["number_of_infection"] )
    plt.xlabel('Data')
    plt.ylabel('Number of infection \n'+ total) 
    plt.xticks(rotation=70)
    plt.show() 
    return  groups

def main():
    data=data_collecter()
    #print(data.columns)
    data=data_city(data,"Keski-Suomi")
    data=grouping(data)
    print(data.dtypes)
    #print(data.columns)
    
    return data

if __name__ == "__main__":
    print(main())
