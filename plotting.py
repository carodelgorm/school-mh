import pandas as pd
import textwrap
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
import matplotlib.transforms as transforms
from matplotlib.ticker import FuncFormatter

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

from util.env import out_data_path, out_path

def format_axes():
    
    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    
    ax.yaxis.grid(True, alpha=0.5, zorder=1, color='#d4d2d2')
    
    return ax

def set_properties():
    """sets mpl properties"""
    mpl.rcParams['legend.handlelength'] = 1
    mpl.rcParams['legend.fontsize'] = 10
    mpl.rcParams['xtick.labelsize'] = 11
    mpl.rcParams['ytick.labelsize'] = 11
    mpl.rcParams['figure.titlesize'] = 18
    mpl.rcParams['axes.titlesize'] = 12
    mpl.rcParams['axes.titlepad'] = 20
    mpl.rcParams['font.family'] = 'Arial'
    
    if 0:
        if 'Arial' in [f.name for f in font_manager.fontManager.ttflist]:
            mpl.rcParams['font.family'] = 'Arial'
        else:
            mpl.rcParams['font.family'] = 'DejaVu Sans'
            print("Arial not found, using default.")


def billions_formatter(x, pos):
    """Format numbers as billions with a dollar sign."""
    return f'${x * 1e-9:.1f}B'

def millions_formatter(x, pos):
    """format numbers as millions with a dollar sign"""
    return f'${x * 1e-6:.0f}'


def plot_ed_amounts(df: pd.DataFrame, col: str, save: bool = True):
    set_properties()
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df['FY'], df[col], marker='o', linestyle='-', color='#2c48dc')

    format_axes()
    title_str = 'Appropriations for school-based mental-health initiatives, U.S. Department of Education'
    fig.suptitle(
        'Figure 1', 
        fontsize=11, ha='left', x=0.01, y=1.08, fontweight='bold', color='#20222e'
        )
    fig.text(
        0.01, 1, title_str, ha='left', fontsize=13, fontweight='bold', color='#20222e'
        )

    ax.set_xlabel('Fiscal Year', fontsize=11, labelpad=7, color='#aeb0b7')
    ax.set_ylabel('Funding (in millions)', fontsize=11, labelpad=10, color='#aeb0b7')
    plt.xticks(df['FY'])
    ax.set_ylim(0, 700000000)
    ax.tick_params(axis='y', which='both', length=0)

    ax.yaxis.set_major_formatter(FuncFormatter(millions_formatter))

    source_text = """Source: FY 2013-2023 Congressional Action, U.S. Department of Education
"""
    note_text = """Note: Funding shown is conservative and non-comprehensive. Included:
funds for safe and drug-free schools and communities, elementary and secondary school
counseling, full-service community schools, and 20 percent of ESEA IV-A student
support and academic enrichment (SSAE) grants (the required minimum that districts
must use of these funds toward student mental and behavioral health, school climate, or
school safety). Not included: Department of Education ESSA Title II funds (which may go
toward educator training related to student mental health), special education, funds
for neglected and delinquent students, or funds for initiatives through other federal
agencies (e.g., SAMHSA, CMS, CDC, or DOJ).
"""
    wrapper = textwrap.TextWrapper(width=146) 
    wrapper2 = textwrap.TextWrapper(width=145)
    source_string = wrapper2.fill(text=source_text) 
    note_string = wrapper.fill(text=note_text)

    plt.figtext(0.05, -0.16, note_string, fontsize=10, color='#20222e')
    plt.figtext(0.05, -0.2, source_string, fontsize=10, color='#aeb0b7')
    plt.tight_layout()

    fig.patch.set_facecolor('#e8ecfc')
    ax.set_facecolor('#e8ecfc')

    if save==True:
        plt.savefig(
            out_path(f'fig1.png'),
            dpi=300, 
            bbox_inches='tight')
    else:
        plt.show() 
    
    return 

def plot_ed_pct_change(df: pd.DataFrame, col: str, save: bool = True):
    set_properties()

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df['FY'], df[col], marker='o', linestyle='-', color='#2c48dc')
    
    format_axes()
    title_str = 'Percent change (relative to 2013) in appropriations for school-based mental-health initiatives \nas a proportion of U.S. Department of Education spending'
    fig.suptitle(
        'Appendix Figure 1', 
        fontsize=11, ha='left', x=0.01, y=1.12, fontweight='bold', color='#20222e'
        )
    fig.text(
        0.01, 1, title_str, ha='left', fontsize=13, fontweight='bold', color='#20222e'
             )

    ax.set_xlabel('Fiscal Year', fontsize=11, labelpad=7, color='#aeb0b7')
    ax.set_ylabel('Percent change in proportion of spending (%)', fontsize=11, labelpad=10, color='#aeb0b7')
    plt.xticks(df['FY'])
    ax.set_ylim(0, None)
    ax.tick_params(axis='y', which='both', length=0)

    #ax.yaxis.set_major_formatter(FuncFormatter(billions_formatter))

    source_text = """Source: FY 2013-2023 Congressional Action, U.S. Department of Education
"""
    note_text = """Note: Percent change is for the proportion of annual appropriations for
school-based mental-health initiatives out of a sum of appropriations for: Education for
the Disadvantaged, Impact Aid, School Improvement Programs, Indian Education, Innovation
and Improvement, Safe Schools and Citizenship Education, and English Language Acquisition.
School-based mental-health initiatives include: funds for safe and drug-free schools and
communities, elementary and secondary school counseling, full-service community schools,
and 20 percent of appropriations for ESEA IV-A student support and academic enrichment
(SSAE) grants (the required minimum that districts must use of these funds toward student
mental and behavioral health, school climate, or school safety). Percent change is
relative to the 2013 proportion appropriated for school-based mental-health.
"""
    wrapper = textwrap.TextWrapper(width=147) 
    wrapper2 = textwrap.TextWrapper(width=145)
    source_string = wrapper2.fill(text=source_text) 
    note_string = wrapper.fill(text=note_text)

    plt.figtext(0.05, -0.15, note_string, fontsize=10, color='#20222e')
    plt.figtext(0.05, -0.185, source_string, fontsize=10, color='#aeb0b7')
    plt.tight_layout()

    fig.patch.set_facecolor('#e8ecfc')
    ax.set_facecolor('#e8ecfc')

    if save==True:
        plt.savefig(
            out_path(f'fig2.png'),
            dpi=300, 
            bbox_inches='tight')
    else:
        plt.show() 



if __name__ == '__main__':
    df = pd.read_csv(out_data_path('ed_sbmh_funding_for_plotting.csv'))

    plot_ed_amounts(df=df, col='Sum SBMH Amt')
    plot_ed_pct_change(df=df, col='Pct Chg 2013')