
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re


# Set the working directory
working_dir = r'D:\Trees\trees272_corrected'
os.chdir(working_dir)

file_names = [f for f in os.listdir(working_dir) if f.endswith('.sim')]

# Separate files by treatment
ww_files = [f for f in file_names if '_ww.sim' in f]
wl_files = [f for f in file_names if '_wl.sim' in f]

file_names = ww_files + wl_files

# Create a figure and axes for 12 plots in a 2x6 grid
fig, axes = plt.subplots(2, 6, figsize=(36, 10), sharex=True, sharey=True, constrained_layout=True)
axes = axes.flatten()


genotype_names = []
treatments = []

# Iterate over the files and plot each on its respective subplot
for i, file_name in enumerate(file_names):
    
    # =============================================================================
    # read the simulation output from Trees272
    # =============================================================================

    match = re.search(r'_VC_(.*?)_(.*?)\.sim', file_name)
    genotype_name = match.group(1)
    treatment = match.group(2)
    
    genotype_names.append(genotype_name)
    treatments.append(treatment)
    
    # Load the simulated data
    simulated_data = pd.read_csv(file_name, sep='\t', header=None)
    
    # Set the first row as the column headers
    simulated_data.columns = simulated_data.iloc[0]
    simulated_data = simulated_data[1:]
    
    # Convert the data types for the relevant columns
    simulated_data['ti'] = simulated_data['ti'].astype(str)
    simulated_data['LAI'] = simulated_data['LAI'].astype(float)
    
    # Extract the DOY from the 'ti' column
    simulated_data['DOY'] = simulated_data['ti'].apply(lambda x: int(x.split(':')[1]))
    simulated_data['Year'] = 2023
    simulated_data['Date'] = pd.to_datetime(simulated_data['Year'] * 1000 + simulated_data['DOY'], format='%Y%j')
    
    # Calculate the daily average of LAI
    daily_simulated_data = simulated_data.groupby('Date').agg({'LAI': 'mean'}).reset_index()
    
    # =============================================================================
    # read the measured data
    # =============================================================================
    file_path_csv = 'LAI_measured_data.csv'
    measured_data = pd.read_csv(file_path_csv)
    replacements = {
        'UGA230': 'UGA230',
        'Pronto': 'Pronto',
        'Tipo Chaco': 'TipoChaco',
        'Virescent nankeen': 'Virescentnankeen',
        'Coker 310': 'Coker310',
        'DeltaPine 16': 'DeltaPine16'
    }
    measured_data['Entry'] = measured_data['Entry'].replace(replacements)
    measured_data['Treatment'] = measured_data['Treatment'].str.lower()
    
    measured_data['Date and Time'] = pd.to_datetime(measured_data['Date and Time'])
    measured_data['Date'] = measured_data['Date and Time'].dt.date
    measured_data = measured_data.loc[measured_data['Position'] != 'Top']
    
    measured_data_avg_lai = measured_data.groupby(['Entry', 'Treatment', 'Date']).agg(
        LAI_mean=('Leaf Area Index [LAI]', 'mean'),
        LAI_std=('Leaf Area Index [LAI]', 'std')
    ).reset_index()
    
    # Filter the data for the specific genotype and treatment
    measured_genotype_data = measured_data_avg_lai.loc[
        (measured_data_avg_lai['Entry'] == genotype_name) & 
        (measured_data_avg_lai['Treatment'] == treatment)
    ]
    
    
    # =============================================================================
    # comparing measured versus simulated
    # =============================================================================
    ax = axes[i]
    
    sns.lineplot(x='Date', y='LAI', data=daily_simulated_data, linewidth=2,
                 linestyle='-', color='k', label='Simulated LAI', ax=ax)
    
    eb1 = ax.errorbar(
        x=measured_genotype_data['Date'], 
        y=measured_genotype_data['LAI_mean'], 
        yerr=measured_genotype_data['LAI_std'], 
        fmt='D', 
        markersize=10,
        markerfacecolor='white', 
        markeredgecolor='red', 
        ecolor='red',
        label='Measured LAI', 
        capsize=5,
        capthick=2,
        elinewidth=2,
    )
    eb1[-1][0].set_linestyle('--')
    
    ax.set_ylim(0.5, 6.8)
    ax.set_xlabel('')
    ax.set_ylabel('LAI (Leaf Area Index)', fontsize=20)
    ax.tick_params(axis='x', rotation=45, labelsize=16)
    ax.tick_params(axis='y', labelsize=16)
    ax.grid(True, linestyle='--', linewidth=0.7)
    
    if i == 0:
        ax.legend(fontsize=20, loc='upper left')
    else:
        ax.legend().remove()

# Add genotype names above each column
for idx, genotype in enumerate(set(genotype_names)):
    fig.text(0.1 + 0.16 * idx, 1.015, genotype, ha='center', va='center', fontsize=25, fontweight='bold')

# Add treatments behind each row
fig.text(-0.015, 0.76, 'Well Watered', ha='center', va='center', rotation='vertical', fontsize=25, fontweight='bold')
fig.text(-0.015, 0.32, 'Water Limited', ha='center', va='center', rotation='vertical', fontsize=25, fontweight='bold')

plt.show()


















# # =============================================================================
# # =============================================================================
# # =============================================================================
# # =============================================================================
# # # # # original for individual plots
# # =============================================================================
# # =============================================================================
# # =============================================================================
# # =============================================================================

# import pandas as pd
# import matplotlib.pyplot as plt
# import os
# import re
# import seaborn as sns

# working_dir=r'D:\Trees\trees272_corrected'
# os.chdir(working_dir)
# # os.chdir(r'D:\Trees\trees272_corrected\validation_runs-20240601T161853Z-001\validation_runs\output')

# # =============================================================================
# # read the simulation output from Trees272
# # =============================================================================

# file_names =  [f for f in os.listdir(working_dir) if f.endswith('.sim')]
# # file_path = 'cotton_output_wet_high_clay_newParams.sim'

# for file_name in file_names:
#     # Extract the genotype name and treatment using regular expressions
#     match = re.search(r'_VC_(.*?)_(.*?)\.sim', file_name)
#     genotype_name = match.group(1)
#     treatment = match.group(2)
    
    
#     simulated_data = pd.read_csv(file_name, sep='\t', header=None)
    
#     # Set the first row as the column headers
#     simulated_data.columns = simulated_data.iloc[0]
#     simulated_data = simulated_data[1:]
    
#     # Convert the simulated_data types for the relevant columns
#     simulated_data['ti'] = simulated_data['ti'].astype(str)
#     simulated_data['LAI'] = simulated_data['LAI'].astype(float)
    
#     # Extract the DOY from the 'ti' column
#     simulated_data['DOY'] = simulated_data['ti'].apply(lambda x: int(x.split(':')[1]))
#     simulated_data['Year']=2023
#     simulated_data['Date'] = pd.to_datetime(simulated_data['Year'] * 1000 + simulated_data['DOY'], format='%Y%j')
    
    
#     # Calculate the daily average of LAI
#     daily_simulated_data = simulated_data.groupby('Date').agg({'LAI': 'mean'}).reset_index()
    
    
    
#     # =============================================================================
#     # read the measured data
#     # =============================================================================
    
#     file_path_csv = 'LAI_measured_data.csv'
#     measured_data = pd.read_csv(file_path_csv)
#     replacements = {'UGA230': 'UGA230',
#         'Pronto': 'Pronto',
#         'Tipo Chaco': 'TipoChaco',
#         'Virescent nankeen': 'Virescentnankeen',
#         'Coker 310': 'Coker310',
#         'DeltaPine 16': 'DeltaPine16'}
#     measured_data['Entry'] = measured_data['Entry'].replace(replacements)
#     measured_data['Treatment'] = measured_data['Treatment'].str.lower()
#     # Convert the 'Date and Time' to a datetime object and extract the date
#     measured_data['Date and Time'] = pd.to_datetime(measured_data['Date and Time'])
#     measured_data['Date'] = measured_data['Date and Time'].dt.date
#     measured_data=measured_data.loc[~(measured_data['Position']=='Top')]
#     # Calculate the daily average LAI for each Entry, Treatment, and Date
#     # measured_data_avg_lai = measured_data.groupby(['Entry', 'Treatment', 'Date']).agg({'Leaf Area Index [LAI]': 'mean'}).reset_index()
#     measured_data_avg_lai = measured_data.groupby(['Entry', 'Treatment', 'Date']).agg(
#         LAI_mean=('Leaf Area Index [LAI]', 'mean'),
#         LAI_std=('Leaf Area Index [LAI]', 'std')
#     ).reset_index()
    
#     # =============================================================================
#     # comparing measured versus simulated
#     # =============================================================================
    
    
#     measured_genotype_data=measured_data_avg_lai.loc[(measured_data_avg_lai['Entry']==genotype_name)&
#                                           (measured_data_avg_lai['Treatment']==treatment)]
    
    
    
#     plt.rc_context({'axes.edgecolor':'black', 'xtick.color':'black', 'ytick.color':'black'})
    
#     plt.figure(figsize=(12, 8))
    
#     # Simulated LAI line plot
#     sns.lineplot(x='Date', y='LAI', data=daily_simulated_data,linewidth=2,
#                  linestyle='-', color='k', label='Simulated LAI')
    
#     # Measured LAI scatter plot with error bars
#     eb1=plt.errorbar(
#         x=measured_genotype_data['Date'], 
#         y=measured_genotype_data['LAI_mean'], 
#         yerr=measured_genotype_data['LAI_std'], 
#         fmt='D', 
#         markersize=10,
#         markerfacecolor='white', 
#         markeredgecolor='red', 
#         ecolor='red',
#         label='Measured LAI', 
#         capsize=5,
#         capthick=2,
#         elinewidth=2,
#     )
#     eb1[-1][0].set_linestyle('--')
    
#     plt.text(0.5, 0.98, genotype_name+"_"+treatment.upper(), ha='center', va='top', transform=plt.gca().transAxes, fontsize=20, fontweight='bold')
    
#     plt.ylim(0.5,6.8)
#     plt.xlabel('')
#     plt.ylabel('LAI (Leaf Area Index)', fontsize=20)
#     plt.xticks(rotation=45, fontsize=20)
#     plt.yticks(fontsize=16)
#     plt.grid(True, linestyle='--', linewidth=0.7)
#     plt.legend(fontsize=16, loc='upper left')
#     plt.tight_layout()
#     plt.show()








# Genotypes=list(set(measured_data_avg_lai['Entry']))
# for Gn in Genotypes:
#     Gn_data=measured_data_avg_lai.loc[measured_data_avg_lai['Entry']==Gn]
#     # Plot the daily average LAI for each Entry and Treatment
#     plt.figure(figsize=(14, 8))
#     sns.lineplot(x='Date', y='Leaf Area Index [LAI]', hue='Treatment', data=Gn_data, markers=True, dashes=False)
#     plt.xlabel('Date')
#     plt.ylabel('LAI (Leaf Area Index)')
#     plt.title('Daily Average LAI for Each Plant Type and Treatment')
#     plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
#     plt.xticks(rotation=45)
#     plt.tight_layout()
#     plt.grid(True)
#     plt.show()




















