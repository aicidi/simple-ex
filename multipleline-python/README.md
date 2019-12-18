```python
# before
x = np.array(x) \
    .astype(np.float32) \
    .reshape((10, 10)) \
    .flatten()      

# after
x = (np.array(x)
    .astype(np.float32) 
    .reshape((10, 10)) 
    .flatten())

# before
if k and type(k) == int and k > 10 and k < 1000:
    print(k)

# after
if (
    k 
    and type(k) == int 
    and k > 10 
    and k < 1000
    ):
    print(k)
```
