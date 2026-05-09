# =============================================================
# THE HIDDEN CRISIS: Data Cleaning Script
# Tory Seaton | FA 550 Capstone
# =============================================================
# This script cleans and processes four SAMHSA datasets:
#   1. NSDUH 2021-2024 (primary substance use survey)
#   2. TEDS-D 2021, 2022, 2023 (treatment episode data)
#
# Output: Pre-aggregated values used in the dashboard
# =============================================================

import pyreadstat
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

# =============================================================
# PART 1: CLEAN NSDUH DATASET
# =============================================================

print("=" * 50)
print("PART 1: CLEANING NSDUH 2021-2024")
print("=" * 50)

# Key columns needed for dashboard
nsduh_cols = [
    'year', 'AGE3', 'irsex', 'NEWRACE2',      # Demographics
    'iralcrc', 'irmjrc', 'ircocrc',            # Substance use (alcohol, marijuana, cocaine)
    'irherrc', 'irfentanyyr',                  # Substance use (heroin, fentanyl)
    'cigmon', 'tobmon', 'irnicvaprec',         # Nicotine/tobacco use
    'amdelt', 'amdeyr',                        # Depression (lifetime, past year)
    'irsutoutrhab', 'irsutinrhab',             # Treatment received
    'mhtrtpy',                                 # Mental health treatment
    'sutuncost', 'sutunwher',                  # Unmet treatment need - barriers
    'sutunnohlp', 'sutunstart',
    'IRPINC3', 'PDEN10'                        # Income, geography
]

print("Loading NSDUH 2021-2024...")
df_nsduh, meta = pyreadstat.read_dta(
    'NSDUH_2021_2024.dta',
    usecols=nsduh_cols
)
print(f"Loaded: {len(df_nsduh):,} rows, {len(df_nsduh.columns)} columns")

# -------------------------------------------------------
# STEP 1: Decode all numeric codes to human-readable labels
# -------------------------------------------------------
print("\nStep 1: Decoding numeric value labels...")

# Age group labels (11 groups)
clean_age = {
    1: '12-13', 2: '14-15', 3: '16-17', 4: '18-20',
    5: '21-23', 6: '24-25', 7: '26-29', 8: '30-34',
    9: '35-49', 10: '50-64', 11: '65+'
}

# Race/ethnicity labels
clean_race = {
    1: 'White', 2: 'Black', 3: 'Native American',
    4: 'Pacific Islander', 5: 'Asian',
    6: 'Multiracial', 7: 'Hispanic'
}

# Sex labels
clean_sex = {1: 'Male', 2: 'Female'}

# Substance use recency labels
clean_use = {
    1: 'Past 30 days', 2: 'Past 12 months',
    3: 'Over 12 months ago', 9: 'Never used'
}

# Geography labels
clean_pden = {1: 'Large Metro', 2: 'Small Metro', 3: 'Rural'}

# Yes/No labels
clean_yesno = {1: 'Yes', 2: 'No'}

# Apply all decodings
df_nsduh['age_group'] = df_nsduh['AGE3'].map(clean_age)
df_nsduh['race'] = df_nsduh['NEWRACE2'].map(clean_race)
df_nsduh['sex'] = df_nsduh['irsex'].map(clean_sex)
df_nsduh['alcohol_use'] = df_nsduh['iralcrc'].map(clean_use)
df_nsduh['marijuana_use'] = df_nsduh['irmjrc'].map(clean_use)
df_nsduh['cocaine_use'] = df_nsduh['ircocrc'].map(clean_use)
df_nsduh['heroin_use'] = df_nsduh['irherrc'].map(clean_use)
df_nsduh['depression_lifetime'] = df_nsduh['amdelt'].map(clean_yesno)
df_nsduh['depression_past_year'] = df_nsduh['amdeyr'].map(clean_yesno)
df_nsduh['location'] = df_nsduh['PDEN10'].map(clean_pden)

print("  Labels decoded successfully")

# -------------------------------------------------------
# STEP 2: Handle special/missing codes
# -------------------------------------------------------
print("Step 2: Handling special codes (-9, 97, 98, 99)...")

# -9  = Data not collected that year
# 97  = Refused to answer
# 98  = Blank
# 99  = Legitimate skip (question did not apply)
# These are NOT real responses and must be excluded from calculations

special_codes = [-9, 97, 98, 99]

# Fentanyl: replace -9 with NaN (not collected in 2021 and 2024)
df_nsduh['irfentanyyr'] = df_nsduh['irfentanyyr'].replace(-9, None)

# Nicotine vaping: not collected in 2021
df_nsduh['irnicvaprec'] = df_nsduh['irnicvaprec'].replace(-9, None)

print("  Special codes handled")

# -------------------------------------------------------
# STEP 3: Create binary use flags (1 = used, 0 = did not use)
# -------------------------------------------------------
print("Step 3: Creating binary use flags...")

df_nsduh['uses_alcohol']       = (df_nsduh['iralcrc'] == 1).astype(int)
df_nsduh['uses_marijuana']     = (df_nsduh['irmjrc'] == 1).astype(int)
df_nsduh['uses_cocaine']       = (df_nsduh['ircocrc'] == 1).astype(int)
df_nsduh['uses_heroin']        = (df_nsduh['irherrc'] == 1).astype(int)
df_nsduh['uses_fentanyl']      = (df_nsduh['irfentanyyr'] == 1).astype(int)
df_nsduh['uses_cigarettes']    = (df_nsduh['cigmon'] == 1).astype(int)
df_nsduh['uses_vaping']        = (df_nsduh['irnicvaprec'] == 1).astype(int)
df_nsduh['has_depression']     = (df_nsduh['amdeyr'] == 1).astype(int)
df_nsduh['got_mh_treatment']   = (df_nsduh['mhtrtpy'] == 1).astype(int)
df_nsduh['got_outpat_rehab']   = (df_nsduh['irsutoutrhab'] == 1).astype(int)

print("  Binary flags created")

# -------------------------------------------------------
# STEP 4: Year filtering
# -------------------------------------------------------
print("Step 4: Filtering by year for treatment chapters...")

# All years: use for substance use chapters (1-2)
df_nsduh_all = df_nsduh.copy()

# 2022-2023 only: use for treatment and mental health chapters (3-4)
# Mental health treatment data is ONLY available in 2022 and 2023
df_nsduh_treat = df_nsduh[df_nsduh['year'].isin(['2022', '2023'])].copy()

print(f"  All years: {len(df_nsduh_all):,} rows")
print(f"  2022-2023 only: {len(df_nsduh_treat):,} rows")

# -------------------------------------------------------
# STEP 5: Save cleaned files
# -------------------------------------------------------
print("Step 5: Saving cleaned files...")
df_nsduh_all.to_csv('nsduh_clean_all.csv', index=False)
df_nsduh_treat.to_csv('nsduh_clean_treatment.csv', index=False)
print("  Saved: nsduh_clean_all.csv")
print("  Saved: nsduh_clean_treatment.csv")


# =============================================================
# PART 2: CLEAN AND COMBINE TEDS-D 2021, 2022, 2023
# =============================================================

print("\n" + "=" * 50)
print("PART 2: CLEANING TEDS-D 2021-2023")
print("=" * 50)

# Only load the columns needed to avoid memory crashes
# Loading all 76 columns across 3 years exceeds memory limits
teds_cols = [
    'DISYR',                           # Discharge year
    'AGE', 'RACE', 'GENDER',           # Demographics
    'SUB1', 'SUB2', 'SUB3',            # Primary, secondary, tertiary substance
    'SERVICES', 'SERVICES_D',          # Treatment type at admission and discharge
    'REASON',                          # Reason for discharge (completed, dropped out, etc.)
    'LOS',                             # Length of stay (days)
    'METHUSE',                         # Medication assisted treatment used
    'EMPLOY', 'EMPLOY_D',              # Employment at admission and discharge
    'ARRESTS', 'ARRESTS_D',            # Arrests at admission and discharge
    'PSYPROB',                         # Co-occurring mental health issue
    'NOPRIOR',                         # No prior treatment episodes
    'STFIPS',                          # State
    'DAYWAIT',                         # Days waiting for treatment
    'HLTHINS'                          # Health insurance status
]

print("Loading TEDS-D 2021...")
df21, _ = pyreadstat.read_dta(
    'tedsd_puf_2021_Stata.dta',
    encoding='latin1',
    usecols=teds_cols
)
print(f"  2021: {len(df21):,} rows")

print("Loading TEDS-D 2022...")
df22, _ = pyreadstat.read_dta(
    'tedsd_puf_2022.dta',
    encoding='latin1',
    usecols=teds_cols
)
print(f"  2022: {len(df22):,} rows")

print("Loading TEDS-D 2023...")
df23, _ = pyreadstat.read_dta(
    'tedsd_puf_2023.dta',
    encoding='latin1',
    usecols=teds_cols
)
print(f"  2023: {len(df23):,} rows")

# -------------------------------------------------------
# STEP 1: Combine all three years
# -------------------------------------------------------
print("\nStep 1: Combining all three years...")
df_teds = pd.concat([df21, df22, df23], ignore_index=True)
del df21, df22, df23  # Free memory
print(f"  Combined: {len(df_teds):,} rows")

# -------------------------------------------------------
# STEP 2: Remove invalid rows
# -------------------------------------------------------
print("Step 2: Removing invalid rows...")
df_teds = df_teds[df_teds['REASON'].notna() & (df_teds['REASON'] > 0)]
df_teds = df_teds[df_teds['SUB1'].notna() & (df_teds['SUB1'] > 0)]
print(f"  Clean rows: {len(df_teds):,}")

# -------------------------------------------------------
# STEP 3: Decode labels
# -------------------------------------------------------
print("Step 3: Decoding TEDS value labels...")

clean_reason = {
    1: 'Treatment completed', 2: 'Dropped out',
    3: 'Terminated by facility', 4: 'Transferred',
    5: 'Incarcerated', 6: 'Death', 7: 'Other'
}

clean_services = {
    1: 'Detox - Hospital', 2: 'Detox - Residential',
    3: 'Inpatient Hospital', 4: 'Short-term Residential',
    5: 'Long-term Residential', 6: 'Intensive Outpatient',
    7: 'Outpatient', 8: 'Ambulatory Detox'
}

clean_sub = {
    2: 'Alcohol', 3: 'Cocaine', 4: 'Marijuana', 5: 'Heroin',
    7: 'Other Opiates', 10: 'Methamphetamine',
    19: 'Nicotine/Tobacco'
}

clean_employ = {
    1: 'Full time', 2: 'Part time',
    3: 'Unemployed', 4: 'Not in labor force'
}

clean_race_teds = {
    1: 'Native American', 2: 'Asian/Pacific Islander',
    3: 'Black', 4: 'White', 5: 'Hispanic',
    6: 'Other', 7: 'Two or more races'
}

df_teds['discharge_reason']     = df_teds['REASON'].map(clean_reason)
df_teds['treatment_type']       = df_teds['SERVICES'].map(clean_services)
df_teds['primary_substance']    = df_teds['SUB1'].map(clean_sub)
df_teds['employment_admit']     = df_teds['EMPLOY'].map(clean_employ)
df_teds['employment_discharge'] = df_teds['EMPLOY_D'].map(clean_employ)
df_teds['race']                 = df_teds['RACE'].map(clean_race_teds)

print("  Labels decoded successfully")

# -------------------------------------------------------
# STEP 4: Create binary outcome flags
# -------------------------------------------------------
print("Step 4: Creating binary outcome flags...")

df_teds['completed']            = (df_teds['REASON'] == 1).astype(int)
df_teds['dropped_out']          = (df_teds['REASON'] == 2).astype(int)
df_teds['used_MAT']             = (df_teds['METHUSE'].isin([1, 2])).astype(int)
df_teds['employed_at_admit']    = (df_teds['EMPLOY'].isin([1, 2])).astype(int)
df_teds['employed_at_discharge']= (df_teds['EMPLOY_D'].isin([1, 2])).astype(int)
df_teds['arrested_at_admit']    = (df_teds['ARRESTS'] > 0).astype(int)
df_teds['arrested_at_discharge']= (df_teds['ARRESTS_D'] > 0).astype(int)

print("  Binary flags created")

# -------------------------------------------------------
# STEP 5: Save combined TEDS file
# -------------------------------------------------------
print("Step 5: Saving cleaned TEDS file...")
df_teds.to_csv('teds_clean_2021_2023.csv', index=False)
print("  Saved: teds_clean_2021_2023.csv")

print("\n" + "=" * 50)
print("ALL CLEANING COMPLETE")
print(f"  NSDUH (all years):     {len(df_nsduh_all):,} rows")
print(f"  NSDUH (2022-2023):     {len(df_nsduh_treat):,} rows")
print(f"  TEDS (2021-2023):      {len(df_teds):,} rows")
print("=" * 50)
