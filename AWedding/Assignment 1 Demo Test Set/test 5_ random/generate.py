import numpy as np

n = 40
arr = np.random.randint(1,5,(n,n))

# just use bottom half
bot_tri = np.tril(arr, k=-1)

# fill top

arr_all = bot_tri + bot_tri.T
# arr_all[arr_all == 0] = np.nan

np.savetxt('preferences.csv', arr_all,fmt='%i', delimiter=',')
