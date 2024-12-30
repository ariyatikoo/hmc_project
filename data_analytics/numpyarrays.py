import numpy as np
# can only store data of the same type, but stores dimensions, allowing for matrix creation
my_list = [1,2,3,4]
my_array = np.array(my_list)
type(my_array)
second_list = [5,6,7,8]
two_d_array = np.array([my_list,second_list])
print(two_d_array)
two_d_array.shape() #rows, columns
two_d_array.size() #num elements
two_d_array.dtype()

# watch video number 8 in playlist if you feel the need to go more in depth
