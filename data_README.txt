=======================================================
DATA FILES — THE HIDDEN CRISIS
Tory Seaton | FA 550 Capstone
=======================================================

NOTE ON FILE SIZES:
The raw data files are too large to include in this submission package.
All four datasets are publicly available for free download from SAMHSA
at: https://www.samhsa.gov/data/data-we-collect

Download links for each file are listed below.

=======================================================
DATASET 1: NSDUH 2021-2024 (Primary Dataset)
=======================================================
Full Name: National Survey on Drug Use and Health 2021-2024
Source: Substance Abuse and Mental Health Services Administration (SAMHSA)
Download: https://www.samhsa.gov/data/data-we-collect/nsduh-national-survey-drug-use-and-health/datafiles
File Format: Stata (.dta)
File Name: NSDUH-2021_2024-DS0001-bndl-data-stata_v1.zip
Rows: 232,441 individual survey respondents
Columns: 2,638 variables
Years Covered: 2021, 2022, 2023, 2024
Used For: Chapters 1-4 (substance use rates, age, gender, race, mental health)
Notes:
  - Mental health treatment variables only available in 2022-2023
  - Fentanyl data not collected in 2024
  - Nicotine vaping data not collected in 2021
  - All variables stored as numeric codes requiring decoding

=======================================================
DATASET 2: TEDS-D 2021 (Treatment & Recovery)
=======================================================
Full Name: Treatment Episode Data Set - Discharges 2021
Source: Substance Abuse and Mental Health Services Administration (SAMHSA)
Download: https://www.samhsa.gov/data/data-we-collect/teds-treatment-episode-data-set/datafiles
File Format: Stata (.dta)
File Name: TEDS-D-2021-DS0001-bndl-data-stata_v1.zip
Rows: 1,351,748 treatment episodes
Columns: 76 variables
Years Covered: 2021
Used For: Chapters 5-7 (treatment completion, methods, life after treatment)
Notes:
  - Each row represents one treatment episode, not one individual
  - Only covers publicly funded treatment facilities
  - Private pay facilities are not included

=======================================================
DATASET 3: TEDS-D 2022 (Treatment & Recovery)
=======================================================
Full Name: Treatment Episode Data Set - Discharges 2022
Source: Substance Abuse and Mental Health Services Administration (SAMHSA)
Download: https://www.samhsa.gov/data/data-we-collect/teds-treatment-episode-data-set/datafiles
File Format: Stata (.dta)
File Name: TEDS-D-2022-DS0001-bndl-data-stata_v1.zip
Rows: 1,394,138 treatment episodes
Columns: 76 variables
Years Covered: 2022
Used For: Chapters 5-7 (treatment completion, methods, life after treatment)
Notes: Same structure as TEDS-D 2021

=======================================================
DATASET 4: TEDS-D 2023 (Treatment & Recovery)
=======================================================
Full Name: Treatment Episode Data Set - Discharges 2023
Source: Substance Abuse and Mental Health Services Administration (SAMHSA)
Download: https://www.samhsa.gov/data/data-we-collect/teds-treatment-episode-data-set/datafiles
File Format: Stata (.dta)
File Name: teds-d-2023-ds0001-bndl-data-stata_v1.zip
Rows: 1,474,025 treatment episodes
Columns: 76 variables
Years Covered: 2023
Used For: Chapters 5-7 (treatment completion, methods, life after treatment)
Notes:
  - Same structure as TEDS-D 2021 and 2022
  - An earlier download of the 2023 file was in SAS CPORT format (.stc)
    which is incompatible with Python. The Stata version was used instead.

=======================================================
COMBINED TOTALS:
- NSDUH: 232,441 survey respondents
- TEDS-D combined (2021+2022+2023): 4,219,911 treatment episodes
- Total records across all datasets: 4,452,352
=======================================================
