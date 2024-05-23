import json
import numpy as np
import pandas as pd
import sandpsue.client.client as client
import sandpsue.server.server as server
from io import StringIO


def privatize_json(input_json_str, epsilon, max_value_per_attr_iter, min_value_per_attr_iter, bucket_amount_per_attr_iter):
    def privatize(worker_values):
        if type(worker_values) != list and pd.isna(worker_values):
            return None
        return client.get_private_vector_multiple_attr(epsilon, max_value_per_attr_iter, min_value_per_attr_iter, bucket_amount_per_attr_iter,worker_values)
    df = pd.read_json(StringIO(input_json_str))
    df = df.applymap(privatize)
    json_str = df.to_json()
    parsed_json = json.loads(json_str)
    privatized_json = {"data": parsed_json}
    privatized_json["epsilon"] =  epsilon
    privatized_json["attr_data"] =  [(max_value_per_attr_iter[i], min_value_per_attr_iter[i], bucket_amount_per_attr_iter[i]) for i in range(len(max_value_per_attr_iter))]
    return json.dumps(privatized_json)
        
def privatize_json_file(input_json_file_path, epsilon, max_value_per_attr_iter, min_value_per_attr_iter, bucket_amount_per_attr_iter):
    with open(input_json_file_path, 'r') as input_json_str:
        input_json_str = input_json_str.read()
    return privatize_json(input_json_str, epsilon, max_value_per_attr_iter, min_value_per_attr_iter, bucket_amount_per_attr_iter)
        
def _get_tensor_list_from_privatized_json_obj(input_json_obj):
    data_dict = input_json_obj["data"]
    attr_bucket_number_list = [attr_data[2] for attr_data in input_json_obj["attr_data"]]

    user_dict_keys = data_dict.keys()

    if len(user_dict_keys) == 0:
        raise AttributeError("No JSON object if file.")

    first_key = list(user_dict_keys)[0]
    timestamp_dict_keys = data_dict[first_key].keys()
    attr_num = len(attr_bucket_number_list)
    n_l_k_tensor_list_per_attr = []
    for attr_data_index in range(attr_num):
        specific_attr_matrix_list_per_user = []
        for user_key in user_dict_keys:
            specific_attr_histogram_array_list_per_timestamp = []
            for timestamp_key in timestamp_dict_keys:
                curr_list = data_dict[user_key][timestamp_key]
                if curr_list is None:
                    curr_array = np.full(attr_bucket_number_list[attr_data_index], np.nan)
                else:
                    curr_array = np.array(curr_list[attr_data_index])
                specific_attr_histogram_array_list_per_timestamp.append(curr_array)    
            specific_attr_matrix_list_per_user.append(np.array(specific_attr_histogram_array_list_per_timestamp)) # append specific attribute - specific worker - Lxk matrix
        n_l_k_tensor_list_per_attr.append(np.array(specific_attr_matrix_list_per_user)) # append specific attribute - NxLxk tensor
    return n_l_k_tensor_list_per_attr

def get_tensor_list_from_privatized_json_str(input_json_str):
    input_json_obj = json.loads(input_json_str)
    return _get_tensor_list_from_privatized_json_obj(input_json_obj)

def avg_estimation_with_json_str(input_json_str, return_avg_histogram=False):
    input_json_obj = json.loads(input_json_str)
    attr_data_list = input_json_obj["attr_data"]
    epsilon = input_json_obj["epsilon"]
    tensor_list = _get_tensor_list_from_privatized_json_obj(input_json_obj)
    max_value_per_attr_iter = [attr_data[0] for attr_data in attr_data_list]
    min_value_per_attr_iter = [attr_data[1] for attr_data in attr_data_list]
    bucket_amount_per_attr_iter = [attr_data[2] for attr_data in attr_data_list]
    return server.average_estimation_multiple_attr(tensor_list, epsilon, max_value_per_attr_iter, min_value_per_attr_iter, bucket_amount_per_attr_iter, return_avg_histogram)

def avg_estimation_with_json_file(input_json_file, return_avg_histogram=False):
    with open(input_json_file, 'r') as json_file:
        input_json_str = json_file.read()
    return avg_estimation_with_json_str(input_json_str, return_avg_histogram)
    
def get_granularity_dataframe(min_value, max_value, number_of_buckets):
    granularity = client.get_bucket_granularity(max_value, min_value, number_of_buckets)
    granularity_dict = {str(j): [f"{j * granularity}-{(j+1) * granularity}"] for j in range(number_of_buckets)}
    df = pd.DataFrame.from_dict(granularity_dict)  
    return df