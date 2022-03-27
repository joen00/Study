import os
from scipy.sparse.linalg import svds
import pandas as pd
import numpy as np
import psycopg2
from scipy.sparse.linalg.dsolve.linsolve import use_solver


conn_string = "host = 'localhost' dbname = 'test_db'  user = 'postgres' password = 'cse3207'"
conn = psycopg2.connect(conn_string)
cur = conn.cursor()

# 현재 폴더 경로; 작업 폴더 기준


def read_room_score():
    cur.execute(
        "SELECT evaluator_pk_id ,classroombasic_pk_id, score FROM classroom_classroomscore")
    df_rating = cur.fetchall()
    #df_rating = pd.read_csv('./class.csv', encoding='cp949')
    # print(df_rating)
    return df_rating


def read_user_goal(uid):
    # return "중국어"
    cur.execute("SELECT user_goal FROM agora_oneuser where id="+str(uid))
    user_goal = cur.fetchall()
    print(user_goal)
    user_goal = user_goal[0]
    tup1 = user_goal
    user_goal = ''.join(tup1)
    return user_goal


def read_room_info():
    cur.execute("SELECT basic.id, basic.title, info.main_goal ,basic.score FROM classroom_classroombasic as basic INNER JOIN classroom_classroominfo as info ON basic.id = info.classroombasic_pk_id")
    df_class = cur.fetchall()
    df_class = pd.read_csv('./class.csv')

    return df_class


def read_user_keyword(uid):
    cur.execute("select word from agora_userkeyword as au inner JOIN agora_keyword as ak on (au.keyword_pk_id=ak.id) where au.user_pk_id="+str(uid))  # 받아오기
    user_keyword = cur.fetchall()
    # print(user_keyword)
    if len(user_keyword) >= 1:
        user_keyword = pd.DataFrame(user_keyword)
        user_keyword.columns = ['keyword']
        user_keyword = user_keyword.values.tolist()
    else:
        user_keyword = ""

    return user_keyword


def recommend_class(df_svd_preds,  class_df, ratings_df, user_id, num_recommendations, user_goal):
    user_row_number = user_id-1
    sorted_user_predictions = df_svd_preds.iloc[user_row_number].sort_values(
        ascending=False)
    user_data = ratings_df[ratings_df.userId == user_id]
    user_history = user_data.merge(class_df, on='classId')
    sorting_name = user_history.columns[2]
    user_history = user_history.sort_values([sorting_name], ascending=False)
    recommendations = class_df[~class_df['classId'].isin(
        user_history['classId'])]
    recommendations = pd.merge(recommendations, pd.DataFrame(
        sorted_user_predictions).reset_index(), on='classId')
    user_row_number = user_row_number+1
    recommendations = recommendations.rename(
        columns={user_row_number: 'Predictions'}).sort_values('Predictions', ascending=False)
    recommendations.loc[recommendations["goal"]
                        == user_goal, 'Predictions'] = 5
    recommendations = recommendations.sort_values(
        'Predictions', ascending=False)
    recommendations = recommendations.iloc[:num_recommendations, :]
    return recommendations


def Id_recommendlist(uid):

    #df_rating = read_room_score()
    df_rating = pd.read_csv('./rating.csv', encoding='cp949')
    df_rating = pd.DataFrame(df_rating)
    df_rating.columns = ['userId', 'classId', 'rating']

    df_class = read_room_info()
    df_class = pd.DataFrame(df_class)
    df_class.columns = ['classId', 'title', 'goal', 'rating']
    class_count = df_class.shape[0]

    user_goal = read_user_goal(uid)
    group = df_rating.groupby(['userId'])
    rating_count = group.size().reset_index(name='counts')
    condition = (rating_count.userId == uid)
    rating_counts = rating_count[condition]
    rating_counts = rating_counts.shape[0]
    rating_count = rating_count.shape[0]
    print(df_rating)
    user_class_rating = df_rating.pivot(
        index='userId', columns='classId', values='rating').fillna(0)
    matrix = user_class_rating.values
    user_rating_mean = np.mean(matrix, axis=1)
    user_rating_std = np.std(matrix, axis=1)
    matrix_normalization = matrix - user_rating_mean.reshape(-1, 1)
    matrix_normalization = matrix_normalization / \
        user_rating_std.reshape(-1, 1)
    pd.DataFrame(matrix_normalization, columns=user_class_rating.columns)

    # 콜드스타트 아닐경우
    if class_count >= 15 and rating_count >= 50 and rating_counts >= 1:
        print("not cold")
        U, s, Vt = svds(matrix_normalization, k=14)
        s = np.diag(s)
        predict_rating = np.dot(np.dot(U, s), Vt)
        predict_rating = predict_rating * user_rating_std.reshape(-1, 1)
        predict_rating = predict_rating + user_rating_mean.reshape(-1, 1)
        pred = pd.DataFrame(
            predict_rating, index=user_class_rating.index, columns=user_class_rating.columns)
        recommendN = 5
        recommend_list = recommend_class(
            pred, df_class, df_rating, uid, recommendN, user_goal)
        return recommend_list['classId'].tolist()

    # 콜드스타트 경우 평점이 높은 스터디 추천 + 사용자의 목표,선호하는 keyword에 해당하는 스터디가 있으면 해당 스터디를 우선추천
    elif class_count >= 15:
        print("cold")
        # print(user_goal)
        # print(user_keyword)
        df_sorted_by_values = df_class.sort_values(['rating'], ascending=False)
        user_keyword = read_user_keyword(uid)
        df_sorted_by_values.loc[df_sorted_by_values["goal"]
                                == user_goal, 'rating'] = 5
        n = 0
        for k in user_keyword:
            n = n+1
            tup1 = k
            word = ''.join(tup1)
            df_sorted_by_values.loc[df_sorted_by_values["goal"]
                                    == word, 'rating'] = 5
        #df_sorted_by_values.loc[df_sorted_by_values["goal"]== user_keyword, 'rating'] = 5
        df_sorted_by_values = df_sorted_by_values.sort_values(
            'rating', ascending=False)
        df_sorted_by_values = df_sorted_by_values.iloc[:5, :]
        recommend_list = df_sorted_by_values
        return recommend_list['classId'].tolist()
        # return recommend_list[['classId']]
    else:
        return None
       # 추천시스템 작동X


print(Id_recommendlist(1))
