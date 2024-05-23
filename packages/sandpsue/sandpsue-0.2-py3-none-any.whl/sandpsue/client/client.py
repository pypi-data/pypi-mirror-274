import math
import numpy as np
from sandpsue.errors.errors import ValuePropertyMissing

def get_bucket_amount(max_value, min_value, granularity): 
    return math.ceil((max_value - min_value) / granularity) #ceil ok?

def get_bucket_granularity(max_value, min_value, bucket_amount): 
    return (max_value - min_value) / bucket_amount


def get_bucket_index_by_value(max_value, min_value, bucket_amount, value):
    granularity = get_bucket_granularity(max_value, min_value, bucket_amount)
    if value < min_value:
        return 0
    elif value > max_value:
        return bucket_amount - 1
    else:
        return math.floor((value - min_value) / granularity)
    

def get_true_vector(max_value, min_value, bucket_amount, value):
    vector = np.zeros(bucket_amount)
    vector[get_bucket_index_by_value(max_value, min_value, bucket_amount, value)] = 1
    return vector
    
    
def get_private_vector(epsilon, max_value, min_value, bucket_amount, value, memo_dict = None):
    if np.isnan(value):
        return np.nan
          
    bucket_index = get_bucket_index_by_value(max_value, min_value, bucket_amount, value)
    
    if memo_dict is not None and bucket_index in memo_dict:
        return memo_dict[bucket_index]
    
    vector = np.zeros(bucket_amount)
    temp = math.exp(epsilon/2)
    
    for i in range(bucket_amount):
        if i == bucket_index:
            p_numerator  = temp
        else:
            p_numerator = 1
        p = p_numerator / (temp + 1)
        vector[i] = np.random.binomial(1,p,1)
        
    if memo_dict is not None:
        memo_dict[bucket_index] = vector
        
    return vector

def get_private_vector_multiple_attr(epsilon, max_value_per_attr_iter, min_value_per_attr_iter, bucket_amount_per_attr_iter, user_value_per_attr_iter, memo_dict_per_attr=None):
    k = len(max_value_per_attr_iter)
    if len(min_value_per_attr_iter) != k or len(bucket_amount_per_attr_iter) != k or len(user_value_per_attr_iter) != k:
        raise ValuePropertyMissing(f"One of your values is missing a property - Max value property list length {k}, Min. value property list length {len(min_value_per_attr_iter)}, Bucket number property list length {len(bucket_amount_per_attr_iter)}, User value property list length {len(user_value_per_attr_iter)}")
    if k == 0:
        raise ValuePropertyMissing("Must have at least 1 value with corresponding properties: max value, min. value, bucket number, user value")
    if memo_dict_per_attr is None:
        memo_dict_per_attr = [None for _ in range(k)]
    new_epsilon =  epsilon / k
    return [get_private_vector(new_epsilon, max_value_per_attr_iter[i], min_value_per_attr_iter[i], bucket_amount_per_attr_iter[i], user_value_per_attr_iter[i], memo_dict_per_attr[i]) for i in range(k)]