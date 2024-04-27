import pandas as pd
import numpy as np
from bs4 import BeautifulSoup

# Change the path here
my_path = r"C:/Users/epana/PycharmProjects/NLP_project/"

# Initialize an empty dictionary of dataframes
my_dfs = {}

# Read in the files
for x in ['ac_discussion1', # Introduction, hobbies
          'ac_discussion2', # Describe real world linear regression problem
          'ac_discussion3', # Describe first 5 weeks, like/dislike about R
          'ac_discussion4', # Describe clustering algorithms and how they solve problems
          'ac_discussion5', # What is your dream data science job? Course recs
          'ac_audienceblog1', # Analytics Computing Project Fair blog 1
          'ac_audienceblog2', # Analytics Computing Project Fair blog 2
          'dw_discussion1', # Discuss how data wrangling was used in Prediction by Numbers video
          'dw_discussion2', # Discuss ethical issues dangers on generative AI in NOVA video
          'dw_discussion3', # Select API, project, and how you would use it
          'dw_discussion4']: # Data wrangling project writeup / advice for future students
    my_dfs[x] = pd.read_json(my_path + "/%s.json" % x)

# Drop some unnecessary columns
for i in my_dfs:
    # drop attachment column if it has an attachment
    if 'attachment' in my_dfs[i].columns:
        my_dfs[i] = my_dfs[i].drop(columns=['attachment','attachments'],axis=1)

    # drop irrelevant columns
    my_dfs[i] = my_dfs[i].drop(columns = ['parent_id','rating_count','rating_sum','user','read_state',
                      'forced_read_state','recent_replies','has_more_replies','editor_id'],
                       axis = 1)

    # Rename the columns
    my_dfs[i].columns = ['post_id','user_id','created_time','updated_time','student','message']

    # Create a create date column
    my_dfs[i]['created_date'] = my_dfs[i]['created_time'].dt.date

    my_dfs[i] = my_dfs[i][['post_id', 'user_id', 'student','created_date', 'created_time', 'updated_time','message']]

    for j in range(len(my_dfs[i])):
        soup = BeautifulSoup(my_dfs[i]['message'][j], 'html.parser')
        soup = soup.text.replace("\r\n", "").replace('Â ','').replace('â€™',"'")
        my_dfs[i].loc[j,'message'] = soup


# Separate the dataframes from the dictionary so easier to call
# Each row in a dataframe is a discussion post, which also has the post id, user_id, user_name (student name),
# created_at time, updated_at time.
ac_discussion1 = my_dfs['ac_discussion1']
ac_discussion2 = my_dfs['ac_discussion2']
ac_discussion3 = my_dfs['ac_discussion3']
ac_discussion4 = my_dfs['ac_discussion4']
ac_discussion5 = my_dfs['ac_discussion5']
ac_audienceblog1 = my_dfs['ac_audienceblog1']
ac_audienceblog2 = my_dfs['ac_audienceblog2']
dw_discussion1 = my_dfs['dw_discussion1']
dw_discussion2 = my_dfs['dw_discussion2']
dw_discussion3 = my_dfs['dw_discussion3']
dw_discussion4 = my_dfs['dw_discussion4']

# Concatenate dataframes and denote source
combined_discussions = pd.concat([ac_discussion1,ac_discussion2,ac_discussion3,ac_discussion4,ac_discussion5,
                    ac_audienceblog1,ac_audienceblog2,dw_discussion1,dw_discussion2,dw_discussion3,dw_discussion4],
                   keys=my_dfs.keys())

# Reset index to make keys as a column
combined_discussions .reset_index(inplace=True)

# Rename the newly created column
combined_discussions  = combined_discussions .rename(columns={'level_0': 'discussion'})

# Create a course column
combined_discussions['course'] = np.where(combined_discussions['discussion'].str.startswith('ac'), 'Analytics Computing',
                            np.where(combined_discussions['discussion'].str.startswith('dw'), 'Data Wrangling', 'Other'))

# Reorder columns
combined_discussions = combined_discussions[['course','discussion','post_id', 'user_id', 'student','created_date',
                                             'created_time','updated_time','message']]

combined_discussions.to_csv('combined_discussion.csv', encoding='utf-8-sig')
ac_discussion1.to_csv('ac_discussion1.csv',encoding='utf-8-sig')
ac_discussion2.to_csv('ac_discussion2.csv',encoding='utf-8-sig')
ac_discussion3.to_csv('ac_discussion3.csv',encoding='utf-8-sig')
ac_discussion4.to_csv('ac_discussion4.csv',encoding='utf-8-sig')
ac_discussion5.to_csv('ac_discussion5.csv',encoding='utf-8-sig')
ac_audienceblog1.to_csv('ac_audienceblog1.csv',encoding='utf-8-sig')
ac_audienceblog2.to_csv('ac_audienceblog2.csv',encoding='utf-8-sig')
dw_discussion1.to_csv('dw_discussion1.csv',encoding='utf-8-sig')
dw_discussion2.to_csv('dw_discussion2.csv',encoding='utf-8-sig')
dw_discussion3.to_csv('dw_discussion3.csv',encoding='utf-8-sig')
dw_discussion4.to_csv('dw_discussion4.csv',encoding='utf-8-sig')





