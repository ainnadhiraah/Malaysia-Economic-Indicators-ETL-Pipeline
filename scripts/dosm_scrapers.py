import pandas as pd
from scripts.base_fetch_API import BaseFetchAPI

class PPI_Scraper(BaseFetchAPI):
    def clean(self, df):
        df = df[df['series'].str.lower() == 'abs']
        df = df.rename(columns={
            'date': 'Date',
            'index': 'Malaysia: PPI: Local Production (NSA, 2010=100)'
        })
        df['Malaysia: PPI: Local Production (NSA, 2010=100)'] = pd.to_numeric(
            df['Malaysia: PPI: Local Production (NSA, 2010=100)'], errors='coerce'
        )
        return df[['Date', 'Malaysia: PPI: Local Production (NSA, 2010=100)']]


class WholesaleRetail_Scraper(BaseFetchAPI):
    def clean(self, df):
        df = df[df['series'].str.lower() == 'abs']
        df = df.rename(columns={
            'date': 'Date',
            'volume_sa': 'Malaysia: Volume Index of Wholesale & Retail Trade (NSA, 2010=100)'
        })
        df['Malaysia: Volume Index of Wholesale & Retail Trade (NSA, 2010=100)'] = pd.to_numeric(
            df['Malaysia: Volume Index of Wholesale & Retail Trade (NSA, 2010=100)'], errors='coerce'
        )
        return df[['Date', 'Malaysia: Volume Index of Wholesale & Retail Trade (NSA, 2010=100)']]


class GDP_Scraper(BaseFetchAPI):
    def clean(self, df):
        df = df[df['series'].str.lower() == 'abs']
        df = df[df['type'].isin(['e5', 'e6'])]
        df_pivot = df.pivot(index='date', columns='type', values='value').reset_index()
        df_pivot = df_pivot.rename(columns={
            'date': 'Date',
            'e5': 'Malaysia: GDP: Exports of Goods and Services (SA, Mil.2015.Ringgit)',
            'e6': 'Malaysia: GDP: Imports of Goods and Services (SA, Mil.2015.Ringgit)'
        })
        df_pivot['Malaysia: GDP: Net Exports of Goods and Services (SA, Mil.2015.Ringgit)'] = (
            df_pivot['Malaysia: GDP: Exports of Goods and Services (SA, Mil.2015.Ringgit)']
            - df_pivot['Malaysia: GDP: Imports of Goods and Services (SA, Mil.2015.Ringgit)']
        )
        for col in df_pivot.columns[1:]:
            df_pivot[col] = pd.to_numeric(df_pivot[col], errors='coerce')
        return df_pivot


class Productivity_Scraper(BaseFetchAPI):
    def clean(self, df):
        df = df[df['series'].str.lower() == 'abs']
        df = df[df['sector'].isin(['p1', 'p2', 'p3', 'p4', 'p5'])]
        df_pivot = df.pivot(index='date', columns='sector', values='employment').reset_index()
        df_pivot = df_pivot.rename(columns={
            'date': 'Date',
            'p1': 'Malaysia: Employment: Agriculture, Forestry and Fishing (NSA, Thous)',
            'p2': 'Malaysia: Employment: Mining and Quarrying (NSA, Thous)',
            'p3': 'Malaysia: Employment: Manufacturing (NSA, Thous)',
            'p4': 'Malaysia: Employment: Construction (NSA, Thous)',
            'p5': 'Malaysia: Employment: Services (NSA, Thous)'
        })
        for col in df_pivot.columns[1:]:
            df_pivot[col] = pd.to_numeric(df_pivot[col], errors='coerce')
        return df_pivot
