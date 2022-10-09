import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

cred = credentials.Certificate("foxtrot-analytics-95472-firebase-adminsdk-6e9fo-d86906cb59.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://foxtrot-analytics-95472-default-rtdb.firebaseio.com/'
})
ref = db.reference('metrics')
json_data = ref.get()

# remove '10' key and keep entries that are timestamp : metrics
del json_data['10']

df_transpose = pd.DataFrame.from_dict(json_data)
print(df_transpose)
df = df_transpose.T
df = df.reset_index()
print(df)
print(df.columns)

# Remove prefixes from variables
df = df.replace('Level_', '', regex=True)

"""
Metric 1: Level Completions
"""
### Plot 1: Count of Completions: Bar
### Level Completions Counts
df['finished_count'] = 0
df.loc[df['finished'] == 'True','finished_count'] = 1
df['total_finished_count'] = 1
finish_by_level = df.groupby(['level'])[('finished_count', 'total_finished_count')].sum().reset_index()
print(finish_by_level)
plt.bar(finish_by_level['level'], finish_by_level['finished_count'], width = 0.3, color = "#6596C7")
plt.xlabel('Level')
plt.ylabel('Count')
plt.title('Successful Level Completions')
# leave room for counts
plt.ylim(0, max(finish_by_level['finished_count']) + 1)
for x,y in zip(finish_by_level['level'],finish_by_level['finished_count']):

    label = "{:.0f}".format(y)

    plt.annotate(label, # this is the text
                 (x,y), # these are the coordinates to position the label
                 textcoords="offset points", # how to position the text
                 xytext=(0,10), # distance from text to points (x,y)
                 ha='center') # horizontal alignment can be left, right or center


plt.legend(loc='best')
plt.savefig('firebase_plots/level_completion_count_bar.png')
plt.show()

### Level Completion Percentages (Success/Overall)
### Plot 2: Percentage of Users that Completed Level
finish_by_level['percentage'] = (finish_by_level['finished_count'] / finish_by_level['total_finished_count']) * 100
print(finish_by_level)
plt.bar(finish_by_level['level'], finish_by_level['percentage'], width = 0.3, color = "#6596C7")
plt.xlabel('Level')
plt.ylabel('Percentage')
plt.title('Percentage of Successful Level Completions')
# leave room for counts
plt.ylim(0, max(finish_by_level['percentage']) + 6)
for x,y in zip(finish_by_level['level'],finish_by_level['percentage']):

    label = "{:.2f}%".format(y)

    plt.annotate(label, # this is the text
                 (x,y), # these are the coordinates to position the label
                 textcoords="offset points", # how to position the text
                 xytext=(0,10), # distance from text to points (x,y)
                 ha='center') # horizontal alignment can be left, right or center


plt.legend(loc='best')
plt.savefig('firebase_plots/level_completion_percentage_bar.png')
plt.show()

### Plot 3: Compare Count of Successful Completions vs. Overall Plays
### Stacked area chart by count
colors = ['#B8E4FF', '#6596C7']
plt.stackplot(finish_by_level['level'], finish_by_level['finished_count'], finish_by_level['total_finished_count'], labels=['Completed Level', 'Total Completions'], colors=colors)
plt.legend(loc='upper left')
plt.show()

### Plot 4: Overall Percentage of Completions
### Pie Chart
df['count_val'] = 1
did_finish_df_counts = df.groupby(['finished']).sum().reset_index()
colors = ['#ED9C9C', '#97DEB1']
fig = plt.figure(figsize =(10, 7))
plt.pie(did_finish_df_counts['count_val'], labels=did_finish_df_counts['finished'], autopct='%1.1f%%', colors=colors)
plt.title('Total Game Plays: Wins vs. Losses')
plt.savefig('firebase_plots/level_completion_pie.png')
plt.show()


#time taken per level
#time taken vs enemies killed/encountered
#time taken vs highscore
#enemies killed vs highscore
#health at end vs highscofe