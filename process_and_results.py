def load_dataframe(filename, cache_dir=".", **kwargs):
    pickle_filename = f"{cache_dir}/{filename.split('/')[-1]}.pkl"
    if os.path.exists(pickle_filename):
        print(f"Loading from cache: {pickle_filename}")
        return pd.read_pickle(pickle_filename)
    else:
        df = pd.read_csv(filename, **kwargs)
        df.to_pickle(pickle_filename)
        return df

combined_df = combined_df[combined_df["YEAR"] >= 2018]
combined_df = combined_df[~combined_df['AGE'].isin([0, 998, 999])]
combined_df = combined_df[~combined_df['TRAV_SP'].isin([998, 999])]
combined_df.loc[combined_df['TRAV_SP'] == 997, 'TRAV_SP'] = 151
combined_df = combined_df[~combined_df["VSPD_LIM"].isin([98, 99, 0])]
import matplotlib.pyplot as plt
import numpy as np
combined_df = combined_df[combined_df["PER_TYP"] == 1]
combined_df = combined_df[~combined_df['ALC_RES'].isin([995, 996, 997, 998, 999])]

#PERMUTATION TEST TIME
#Is the average speed over speed limit of a drunk driver different than the average speed limit over speed limit of a regular driver
#with a 5% significance level? We hypothesize that drunk drivers will be higher on average
combined_df["DRUNK"] = combined_df["ALC_RES"] >= 80
combined_df["SPEED_OVER_LIMIT"] = combined_df["TRAV_SP"] - combined_df["VSPD_LIM"]
drunk_df = combined_df[combined_df["DRUNK"] == True]
not_drunk_df = combined_df[combined_df["DRUNK"] == False]
avg_sp_ov_lim_drunk = drunk_df["SPEED_OVER_LIMIT"].mean()
avg_sp_ov_lim = not_drunk_df["SPEED_OVER_LIMIT"].mean()
obs_stat = avg_sp_ov_lim_drunk-avg_sp_ov_lim

vals = combined_df["DRUNK"].values
sp = combined_df["SPEED_OVER_LIMIT"].values
def simulate_test_stat(sp, vals):
  categories_shuffled = vals.copy()
  np.random.shuffle(categories_shuffled)
  idx_drunk = np.where(categories_shuffled == True)
  avg_drunk_sp = np.average(sp[idx_drunk])
  idx_not_drunk = np.where(categories_shuffled == False)
  avg_not_drunk_sp= np.average(sp[idx_not_drunk])
  sim_test_stat = avg_drunk_sp-avg_not_drunk_sp
  return sim_test_stat
#Shuffling the categories (Drunk and Not Drunk) to conduct the permutation test.

test_stats = []
for i in range(10000):
  test_stats.append(simulate_test_stat(sp, vals))

from google.colab import files
plt.figure(figsize=(15, 15))
plt.hist(test_stats, color='steelblue', edgecolor='black', alpha=0.7)
plt.axvline(obs_stat, color='royalblue', linewidth=2, linestyle='--', label='Observed Difference Of Drunk Driving - Not Drunk Driving')
plt.title('Simulated Test Statistics of Drunk vs Non-Drunk Speed Over Speed Limit', fontsize=20, fontweight='bold', color='black')
plt.xlabel('Test Statistics', fontsize=20, fontweight='bold', color='black')
plt.ylabel('Frequency', fontsize=20, fontweight='bold', color='black')

plt.xticks(fontsize=30)
plt.yticks(fontsize=30)
plt.legend(fontsize=20)
plt.savefig('drunkVnotdrunk.png', dpi=300)
files.download('drunkVnotdrunk.png')
plt.show()

#Now let's do the bootstrapping conf interval
#I'm going to estimate the mean driving speed of males in accidens with a 95% conf interval
#then im going to see if the mean driving speed of females in accidents falls within this conf interval
male_df = combined_df[combined_df["SEX"] == 1]
female_df = combined_df[combined_df["SEX"] == 2]
avg_female_sp = female_df["SPEED_OVER_LIMIT"].mean()
def one_bootstrap_mean(sample_df):
  bootstrap_sample = sample_df.sample(n=len(sample_df), replace=True)
  bootstrapped_mean = bootstrap_sample["SPEED_OVER_LIMIT"].mean()
  return bootstrapped_mean
means = []
for i in range(1000):
  means.append(one_bootstrap_mean(male_df))
  print(str(i/10000 * 100) + "% done")
left_interval_endpoint = np.percentile(means, 2.5)
right_interval_endpoint = np.percentile(means, 97.5)
interval = np.array([left_interval_endpoint, right_interval_endpoint])
plt.figure(figsize=(15, 15))
plt.hist(means, color='deepskyblue', edgecolor='black', alpha=0.7)
plt.axvline(avg_female_sp, color='royalblue', linewidth=2, label='Avg Speed of Females in Accidents')
plt.plot(interval, [0, 0], linewidth=20, color='navy', alpha=0.9)
plt.title('95% Bootstrapped Confidence Interval of \nAverage Speed Over Speed Limit of Males in Accidents', fontsize=20, fontweight='bold', color='black')
plt.xlabel('Driving Speed During Accident (MPH)', fontsize=16, fontweight='bold', color='black')
plt.ylabel('Frequency', fontsize=16, fontweight='bold', color='black')
plt.legend(fontsize=12)
plt.savefig('malevfemale.png', dpi=300)
plt.xticks(fontsize=30)
plt.yticks(fontsize=30)
files.download('malevfemale.png')

