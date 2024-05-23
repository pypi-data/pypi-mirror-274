import math
import numpy as np
import sandpsue.client.client as client
from sandpsue.errors.errors import ValuePropertyMissing


def get_avg_vector_estimation(tenzor, epsilon):
    n, l, d = tenzor.shape
    temp = math.exp(epsilon/2)
    p = temp / (temp + 1)
    temp = np.sum(tenzor, axis=2)
    nan_count = np.isnan(temp).sum()
    v_hat_sum_timestamp_axis = np.nansum(tenzor, axis=1)
    v_hat_sum = np.nansum(v_hat_sum_timestamp_axis, axis=0)
    return ( ( v_hat_sum / (n * l - nan_count) ) - (1-p) ) / (2*p-1)


def get_weights_vector(max_value, min_value, bucket_amount):
    granularity = client.get_bucket_granularity(max_value, min_value, bucket_amount)
    return np.array([(min_value + granularity * (i + 0.5)) for i in range(bucket_amount)])


def average_estimation(tenzor, epsilon, max_value, min_value, bucket_amount, return_avg_histogram=False):
    weights_vector = get_weights_vector(max_value, min_value, bucket_amount)
    avg_vector = get_avg_vector_estimation(tenzor, epsilon)
    if return_avg_histogram:
        return [np.nansum(np.multiply(weights_vector,avg_vector)), avg_vector]
    return np.nansum(np.multiply(weights_vector,avg_vector))


def average_estimation_multiple_attr(tenzor_list, epsilon, max_value_per_attr_iter, min_value_per_attr_iter, bucket_amount_per_attr_iter, return_avg_histogram=False):
    k = len(max_value_per_attr_iter)
    if len(min_value_per_attr_iter) != k or len(bucket_amount_per_attr_iter) != k:
        raise ValuePropertyMissing(f"One of your values is missing a property - Max value property list length {k}, Min. value property list length {len(min_value_per_attr_iter)}, Bucket number property list length {len(bucket_amount_per_attr_iter)}")
    if k == 0:
        raise ValuePropertyMissing("Must have at least 1 value with corresponding properties: max value, min. value and bucket number")
    res = []
    for i in range(k):
        res.append(average_estimation(tenzor_list[i], (epsilon/k), max_value_per_attr_iter[i], min_value_per_attr_iter[i], bucket_amount_per_attr_iter[i], return_avg_histogram))
    return res