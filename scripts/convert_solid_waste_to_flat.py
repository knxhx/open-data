import pandas as pd
from datetime import datetime
from dateutil import parser

def get_recyling(xl, sheet_nm):
    recycling_df = xl.parse(sheet_nm, skiprows=4,nrows=8)
    recycling_df = recycling_df.rename(columns={ recycling_df.columns[0]: 'material' })
    recycling_df = recycling_df.drop(columns=['DROP OFF CENTER TOTALS'])
    recycling_long = pd.melt(recycling_df, id_vars = ['material'], \
        value_vars=recycling_df.columns.values.tolist()[1:10], \
        var_name='location', value_name = 'commodity_wt')
    recycling_long['date'] = parser.parse(f'1 {sheet_nm}')

    def label_location(row):
        if row['location'] in recycling_df.columns.values.tolist()[1:5]:
            return 'drop off center'
        elif row['location'] in recycling_df.columns.values.tolist()[7:8]:
            return 'curbside'
        else:
            return 'other'

    recycling_long['location_type'] = recycling_long.apply( \
        lambda row: label_location(row),axis = 1)
    return recycling_long

def get_landfill(xl, sheet_nm):
    landfill_df = xl.parse(sheet_nm, skiprows=17,nrows=6,usecols=[0,1,2])
    landfill_df = landfill_df.rename(columns={ landfill_df.columns[1]: \
    landfill_df.iloc[0,1], landfill_df.columns[2]: \
    str(landfill_df.iloc[0,2])})
    landfill_df = landfill_df.drop(index=0)
    landfill_df = landfill_df.rename(columns={ landfill_df.columns[0]: 'source' })
    landfill_long = pd.melt(landfill_df, id_vars = ['source'], \
        value_vars=landfill_df.columns.values.tolist()[1:3], \
        var_name='class', value_name = 'landfill_wt')
    landfill_long['date'] = parser.parse(f'1 {sheet_nm}')
    return landfill_long

if __name__ == "__main__":
    xl = pd.ExcelFile('./data/solid_waste_reports.xlsx')
    recycling_ls = [get_recyling(xl, sheet) for sheet in xl.sheet_names[:-2]]
    recycling_df = pd.concat(recycling_ls)
    recycling_df.to_csv('data/recycling_flat.csv')
    landfill_ls = [get_landfill(xl, sheet) for sheet in xl.sheet_names[:-2]]
    landfill_df = pd.concat(landfill_ls)
    landfill_df.to_csv('data/landfill_flat.csv')