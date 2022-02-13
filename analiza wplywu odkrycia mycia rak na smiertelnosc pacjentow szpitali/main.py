#analiza wplywu mycia rak na smiertelnosc w szpitalach przy uzyciu pythona oraz bibliotek

import pandas as pd
# Read datasets/yearly_deaths_by_clinic.csv into yearly
yearly = pd.read_csv('datasets/yearly_deaths_by_clinic.csv')

# Print out yearly
print(yearly)
yearly['proportion_deaths']=yearly['deaths']/yearly['births']
# Extract Clinic 1 data into clinic_1 and Clinic 2 data into clinic_2
clinic_1 = yearly[yearly['clinic']=='clinic 1']
clinic_2 = yearly[yearly['clinic']=='clinic 2']

# Print out clinic_1
print(clinic_1)
# This makes plots appear in the notebook
%matplotlib inline

# Plot yearly proportion of deaths at the two clinics
ax=clinic_1.plot(x='year',y='proportion_deaths',label='Clinic 1')
clinic_2.plot(x='year',y='proportion_deaths',ax=ax,label='Clinic 2',ylabel='Proportion deaths')
# Read datasets/monthly_deaths.csv into monthly
monthly = pd.read_csv('datasets/monthly_deaths.csv',parse_dates=['date'])

# Calculate proportion of deaths per no. births
# ... YOUR CODE FOR TASK 4 ...
monthly["proportion_deaths"]=monthly['deaths']/monthly['births']
# Print out the first rows in monthly
print(monthly.head())
# Plot monthly proportion of deaths
ax=monthly.plot(x='date',y='proportion_deaths',ylabel='Proportion deaths')
# Date when handwashing was made mandatory
handwashing_start = pd.to_datetime('1847-06-01')

# Split monthly into before and after handwashing_start
before_washing = monthly[monthly['date']<handwashing_start]
after_washing = monthly[monthly['date']>=handwashing_start]

# Plot monthly proportion of deaths before and after handwashing
ax = before_washing.plot(x='date',y='proportion_deaths',label='before washing')
after_washing.plot(x='date',y='proportion_deaths',ax=ax,label='after washing',ylabel='Proportion deaths')
# Difference in mean monthly proportion of deaths due to handwashing
before_proportion = before_washing['proportion_deaths']
after_proportion = after_washing['proportion_deaths']
mean_diff = after_proportion.mean()-before_proportion.mean()
mean_diff
# A bootstrap analysis of the reduction of deaths due to handwashing
boot_mean_diff = []
for i in range(3000):
    boot_before = before_proportion.sample(frac=1,replace=True)
    boot_after = after_proportion.sample(frac=1,replace=True)
    boot_mean_diff.append( boot_before.mean()-boot_after.mean() )

# Calculating a 95% confidence interval from boot_mean_diff
confidence_interval = pd.Series(boot_mean_diff).quantile([0.025,0.975])
confidence_interval
