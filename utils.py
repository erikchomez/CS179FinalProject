import pandas as pd
import numpy as np


def recommend(user_id, predictions_df, movies_df, ratings_df, num_recs=10):
    # 1 based index so we subtract 1
    # sort the predictions
    sorted_user_pred = predictions_df.iloc[user_id-1].sort_values(ascending=False)
    
    og_user_data = ratings_df[ratings_df.userId == (user_id)]
    # merge with movies data frame (full data frame)
    merged_user = (og_user_data.merge(movies_df, how = 'left', left_on = 'movieId', right_on = 'movieId').
                     sort_values(['rating'], ascending=False))
                   
    # recommended movies based on predicted rating
    recs = (movies_df[~movies_df['movieId'].isin(merged_user['movieId'])])
    to_merge_with = pd.DataFrame(sorted_user_pred).reset_index()
    recs = recs.merge(to_merge_with, how='left', left_on='movieId', right_on='movieId')
    #recs = recs.rename(columns = {user_id-1: 'Predictions'}).sort_values('Predictions', ascending = False).iloc[:num_recs, :-1]
    #print(recs.head()
    recs.columns = ['movieId', 'title', 'prediction']
    recs = recs.sort_values(by=['prediction'], ascending=False)

    return merged_user, recs