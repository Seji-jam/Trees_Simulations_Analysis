import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re


# Set the working directory
working_dir = r'D:\Trees\trees272_corrected'
os.chdir(working_dir)

file_names = [f for f in os.listdir(working_dir) if f.endswith('.sim')]

files_to_remove = [
    'cotton_avg_soil_geno_VC_DeltaPine16_wl.sim',
    'cotton_avg_soil_geno_VC_DeltaPine16_ww.sim',
    'cotton_avg_soil_geno_VC_Virescentnankeen_wl.sim',
    'cotton_avg_soil_geno_VC_Virescentnankeen_ww.sim'
]

# Remove specified items
file_names = [file for file in file_names if file not in files_to_remove]


# Separate files by treatment
ww_files = [f for f in file_names if '_ww.sim' in f]
wl_files = [f for f in file_names if '_wl.sim' in f]

file_names = ww_files + wl_files

# Create a figure and axes for 12 plots in a 2x6 grid
fig, axes = plt.subplots(2, 4, figsize=(36, 10), sharex=True, sharey=True, constrained_layout=True)
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
    simulated_data['Canopy_Temp']=(simulated_data['Tshd'].astype(float) + simulated_data['Tsun'].astype(float))/2
    # Calculate the daily average of LAI
    daily_simulated_data = simulated_data.groupby('Date').agg({'Canopy_Temp': 'mean'}).reset_index()
    daily_simulated_data=daily_simulated_data.loc[daily_simulated_data['Canopy_Temp']>-10]
    # =============================================================================
    # read the measured data
    # =============================================================================
    measurement_file_name = 'Cotton_GoField_CanopyTemperature.xlsx'
    measured_data = pd.read_excel(measurement_file_name,sheet_name=f'{genotype_name}_{treatment.upper()}')
       
    measured_data['date_time'] = pd.to_datetime(measured_data['date_time'])
    measured_data['Date'] = measured_data['date_time'].dt.date

    
    measured_data_avg = measured_data.groupby([ 'Date']).agg(
        CanopyTemp_mean=('canopy_temp', 'mean')).reset_index()
    measured_data_avg['CanopyTemp_mean'].min()
    # =============================================================================
    # comparing measured versus simulated
    # =============================================================================
    ax = axes[i]
    
    sns.lineplot(x='Date', y='Canopy_Temp', data=daily_simulated_data, linewidth=2,
                 linestyle='--', color='red', label='Simulated Canopy Temperature', ax=ax)
    
    sns.lineplot(x='Date', y='CanopyTemp_mean', data=measured_data_avg, linewidth=2,
                 linestyle='-', color='k', label='Measured Canopy Temperature', ax=ax)
    
    
    
    ax.set_ylim(20, 42)
    ax.set_xlabel('')
    ax.set_ylabel('Canopy Temp', fontsize=20)
    ax.tick_params(axis='x', rotation=45, labelsize=16)
    ax.tick_params(axis='y', labelsize=16)
    ax.grid(True, linestyle='--', linewidth=0.7)
    
    if i == 0:
        ax.legend(fontsize=20, loc='upper left')
    else:
        ax.legend().remove()

# Add genotype names above each column
for idx, genotype in enumerate(set(genotype_names)):
    fig.text(0.1 + 0.26 * idx, 1.015, genotype, ha='center', va='center', fontsize=25, fontweight='bold')

# Add treatments behind each row
fig.text(-0.015, 0.76, 'Well Watered', ha='center', va='center', rotation='vertical', fontsize=25, fontweight='bold')
fig.text(-0.015, 0.32, 'Water Limited', ha='center', va='center', rotation='vertical', fontsize=25, fontweight='bold')

plt.show()


