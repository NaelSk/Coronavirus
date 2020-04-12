import requests
import pandas as pd


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
    print(df4)
    return df4


def data_collecter():
    url = 'https://korona.kans.io/'
    html = requests.get(url).content
    df_list = pd.read_html(html)
    df = df_list[-1]
    processed_data=split_date1(df)
    return (df.to_csv('my data.csv'))


def main():
    data=data_collecter()
    print(data)
    return data

if __name__ == "__main__":
    main()
