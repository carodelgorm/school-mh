import pandas as pd

from util.env import data_path, out_data_path

def prep_data_for_plot():
    # get program-level funding for sbmh items
    ed_sbmh = pd.read_csv(data_path('ed_sbmh_funding.csv'))

    ed_sbmh['Appropriated Amt'] = (
        ed_sbmh['Appropriated Amt'].str.replace(',', '').apply(int)
        )

    ed_sbmh = ed_sbmh[ed_sbmh['SBMH'] == 'Y'].copy()

    ed_sbmh_fy_df = ed_sbmh.groupby('FY')['Appropriated Amt'].sum().reset_index()
    ed_sbmh_fy_df = ed_sbmh_fy_df.rename(columns={'Appropriated Amt': 'Sum SBMH Amt'})

    # keep only 2013 - 2023
    ed_sbmh_fy_df = ed_sbmh_fy_df[
        (ed_sbmh_fy_df['FY'] > 2012) & 
        (ed_sbmh_fy_df['FY'] < 2024)
        ]
    
    # get overall ed budgets by FY and area ('Account')
    ed = pd.read_csv(data_path('ed_overall_budgets.csv'))
    
    ed['Total Appropriated Amount'] = (
        ed['Total Appropriated Amount'].str.replace(',', '').apply(int)
        )
    # exclude special ed in total
    ed = ed[ed['Account']!='Special Education']
    # keep only 2013 - 2023
    ed = ed[(ed['FY'] > 2012) & (ed['FY'] < 2024)]

    ed_fy = ed.groupby('FY')['Total Appropriated Amount'].sum().reset_index()
    ed_fy_df = ed_fy.rename(columns={'Total Appropriated Amount': 'Sum Tot Amt'})

    # merge the dataframes to get the prop of funding per fy and pct chg
    df = pd.merge(ed_sbmh_fy_df, ed_fy_df, on='FY', how='left')

    df['Prop'] = df['Sum SBMH Amt'] / df['Sum Tot Amt']

    prop_2013 = df.loc[df['FY'] == 2013, 'Prop'].values[0]
    df['Pct Chg 2013'] = ((df['Prop'] - prop_2013) / prop_2013 * 100)

    df.to_csv(out_data_path('ed_sbmh_funding_for_plotting.csv'), index=False)

    return 

if __name__ == '__main__':
    prep_data_for_plot()








