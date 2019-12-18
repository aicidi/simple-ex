import numpy as np

x = list(range(100))

x = np.array(x)
x = x.astype(np.float32)
x = x.reshape((10, 10))
x = x.flatten()

x = np.array(x) \
    .astype(np.float32) \
    .reshape((10, 10)) \
    .flatten()      
    
x = (np.array(x)
    .astype(np.float32) 
    .reshape((10, 10)) 
    .flatten())
    
# print(x)


k = 100

if k and type(k) == int and k > 10 and k < 1000:
    print(k)

if (
    k 
    and type(k) == int 
    and k > 10 
    and k < 1000
    ):
    print(k)
