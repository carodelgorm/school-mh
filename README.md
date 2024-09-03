# School-Based Mental-Health Initiatives

This repo includes the original source data and data used to plot the figures in 
"School-Based Mental-Health Initiatives: Challenges and Considerations for Policymakers"

Python version: 3.8.19
<br>
Check that all packages in setup.py and plotting.py are installed 

For plotting:
- run setup.py to generate csv file of merged "ed_sbmh_funding.csv" and "ed_overall_budgets.csv" (saved as 'ed_sbmh_funding_for_plotting.csv')
- run plotting.py to generate fig1.png and fig2.png
- run maps.py to generate appendix maps: map_mh_absences.png, map, map_mh_literacy.png, prek12sel.png

CSV Files:
- in 'src' 11-24action.xlxs are raw files from US Department of Education representing FY budgets, used to create 'ed_overall_budgets.csv' and 'ed_sbmh_funding.csv' for Figure 1 and Appendix Figure 1 (saved as fig2.png)
- in 'src' state_level_policies.csv is used to create map figures in appendix