import pandas as pd
import numpy as np
import time

'''
    R: real rating matrix
    P: |U| * K (User latency values matrix)
    Q: |D| * K (Item latency values matrix)
    K: number of latent features
    steps: iterations alpha: learning rate
    beta: regularization parameter
'''
def matrix_factorization(R, P, Q, K, steps=5000, alpha=0.0002, beta=0.02):
    # numpy.ndarray.T means "transpose"
    Q = Q.T
    # Iterates throught given number of "steps" from the argument
    for step in range(steps):
        # Iterates through users list
        for i in range(len(R)):
            # Iterates through recipes list
            for j in range(len(R[i])):
                # only consider ratings greater than zero?
                if R[i][j] > 0:
                    # calculate the different between real rating and assumed
                    eij = R[i][j] - np.dot(P[i,:],Q[:,j])
                    # Iterates through each latent value, per user+recipe
                    for k in range(K):
                        # calculate gradient with alpha and beta parameter
                        P[i][k] = P[i][k] + alpha * (2 * eij * Q[k][j] - beta * P[i][k])
                        Q[k][j] = Q[k][j] + alpha * (2 * eij * P[i][k] - beta * Q[k][j])
        # what is this?
        # eR = np.dot(P,Q)
        # print("eR shape = {}".format(eR.shape))
        e = 0
        # Iterates through users list
        for i in range(len(R)):
            # Iterates through recipes list
            for j in range(len(R[i])):
                # only consider ratings greater than zero?
                if R[i][j] > 0:
                    #regularization formula
                    e = e + pow(R[i][j] - np.dot(P[i,:],Q[:,j]), 2)
                    for k in range(K):
                        e = e + (beta/2) * (pow(P[i][k],2) + pow(Q[k][j],2))
        # 0.001: local minimum
        if e < 0.001:
            break
    return P, Q.T

def MakeDataFrame(file_name,debug_details=False):
    path = "/Users/willmcintosh/DataSciencePractice/"
    df = pd.read_csv(path+file_name+".csv")
    df = df.sort_values(by="user_id")
    if debug_details:
        print(df.columns)
        print(df.head())
        print(df.shape)
    return df

def MakeAdjacencyMatrix(df):
    # Creates lists from the dataframe for the labels
    users = df['user_id']
    recipes = df['recipe_id']
    # Gets the lengths of the adjacency matrix
    u_recipes = recipes.unique()
    u_users = users.unique()
    #limits the max size of the adjacency matrix to the smaller of the two
    size = min(len(u_recipes),len(u_users))-1
    u_R = u_recipes[:size]
    u_U = u_users[:size]
    last_u_val = u_U[-1]
    u_index = df[df['user_id'] == last_u_val].index.to_numpy()[-1]
    last_r_val = u_R[-1]
    r_index = df[df['recipe_id'] == last_r_val].index.to_numpy()[-1]
    # Initializes the adjacency matrix to the unique size of the two dataframes
    real_ratings = pd.DataFrame(np.empty(shape=(size,size)), columns=u_R, index=u_U)
    real_ratings[:] = np.nan
    # Makes a csv from the actual, real ratings
    return real_ratings, last_u_val,last_r_val,u_U, u_R

def FillInMatrixValues(df,last_u_val,last_r_val,real_ratings,debug_time=False):
    users = df['user_id']
    recipes = df['recipe_id']
    ratings = df['rating']
    # Finds the last value in the unique users list and applies it to all users
    u_index = df[df['user_id'] == last_u_val].index.to_numpy()[-1]
    r_index = df[df['recipe_id'] == last_r_val].index.to_numpy()[-1]
    print("")
    print("")
    print("users shape = {}".format(users.shape))
    # Initializing these series so they're available outside the for loop
    user = users[0]
    recipe = recipes[0]
    for i in range(0, r_index):
        start = time.time()
        user = users[i]
        recipe = recipes[i]
        rating = ratings[i]
        real_ratings.at[user,recipe] = rating
        print("at iteration {} the size is {}".format(i,real_ratings.shape))
        stop = time.time()
        duration = stop-start
        if debug_time:
            print(duration)
    print(real_ratings)
    # returns the real_ratings adjacency matrix and the two trimmed series
    return real_ratings

if __name__ == "__main__":
    file_name = "first_hundred_interactions"
    df = MakeDataFrame(file_name)
    real_ratings,last_u_val,last_r_val,u_U,u_R = MakeAdjacencyMatrix(df)
    real_ratings = FillInMatrixValues(df,last_u_val,last_r_val,real_ratings)
    real_ratings.to_csv("real_ratings_matrx_"+file_name+".csv")
    # print(real_ratings)
    """ Example Adjacency Matrix
    R = [
     [5,3,np.NaN,1],
     [4,0,0,1],
     [1,1,0,5],
     [1,0,0,4],
     [0,1,5,4],
     [2,1,3,0],
    ]
    """

    print(real_ratings)
    # R = np.array(R)
    R = np.array(real_ratings)
    # N: num of User
    N = len(R)
    # R: num of Recipes
    M = len(R[0])
    # Num of Latent Features (I can set this to any number)
    # Keep trying to make the accuracy higher and higher, look for a stable number
    K = 5
    # Fills 2d array with random numbers (user by k) or (items by k)
    P = np.random.rand(N,K)
    Q = np.random.rand(M,K)

    user_latent_values, item_latent_values = matrix_factorization(R, P, Q, K)
    newR = np.dot(user_latent_values, item_latent_values.T)
    print("")
    print("R size = {}".format(R.shape))
    newR_df = pd.DataFrame(data=newR, index=real_ratings.index, columns=real_ratings.columns)
    print(newR_df)
    print("")
    print("NewR shape = {}".format(newR_df.shape))

    newR_df.to_csv("estimated_ratings_matrx_"+file_name+".csv")

