from wave_helper import *
import numpy
import math

'''the max/min value that a wav format can get in audio list'''
MAX_VOL = 32767
MIN_VOL = -32768

def reverse_list(list):
    '''get a list and return reversed list'''
    new_list = list[::-1]
    print(new_list)
    return new_list


def reverse_audio(list):
    '''get a audio list and reverse it'''
    new_audio = reverse_list(list)
    return new_audio


def is_odd(number):
    '''check if number is odd or not'''
    if number%2 == 0:
        return False
    return True


def speed_audio(audio_list):
    '''spped the audio by taking just the even index in the audio list'''
    new_audio_list = []
    for list in audio_list:
        index = audio_list.index(list)
        if not is_odd(index):
            new_audio_list.append(list)
    return new_audio_list


def average_of_lists(*lists):
    '''return the average between given list with 2 values'''
    lists_count = len(lists)
    first_average = 0
    second_average = 0
    for list in lists:
        first_average += list[0]
        second_average += list[1]
    first_average = int(first_average/lists_count)
    second_average = int(second_average/lists_count)
    average_list = [first_average, second_average]
    return average_list


def slow_audio(audio_list):
    '''slow the audio down by adding the avarage of two audio list between
        them'''
    new_audio_list =[]
    for index in range(len(audio_list)-1):
        new_audio_list.append(audio_list[index])
        current_list = audio_list[index]
        next_list = audio_list[index+1]
        average_list = average_of_lists(current_list,next_list)
        new_audio_list.append(average_list)
    new_audio_list.append(audio_list[-1])
    return new_audio_list


def change_volume(audio_list,change_value):
    '''get an audio list and increase it by 1.2 and makes sure we dont pass
        the max\min value'''
    new_audio_list = audio_list
    increase_value = change_value
    new_audio_list = increase_value*numpy.array(new_audio_list)
    new_audio_list = new_audio_list.astype('int')
    new_audio_list = numpy.clip(new_audio_list,a_min= MIN_VOL, a_max=MAX_VOL)
    new_audio_list = new_audio_list.tolist()

    return new_audio_list


def increase_vol(audio_list):
    '''increase vol by 1.2'''
    return change_volume(audio_list,change_value=1.2)


def low_vol(audio_list):
    '''low vol by 1.2'''
    return change_volume(audio_list,change_value=(1/1.2))


def audio_fade(audio_list):
    '''fade the audio by doing an average of 3 followers in the sequence'''
    new_list = []
    new_list.append(average_of_lists(audio_list[0],audio_list[1]))
    for i in range(1,len(audio_list)-1):
        new_list.append(average_of_lists(audio_list[i-1],audio_list[i],
                                       audio_list[i+1]))
    new_list.append(average_of_lists(audio_list[-2],audio_list[-1]))
    return new_list


def num_of_data_for_merge(sample_rate_1,sample_rate_2):
    '''check the gcd of samples rate and how many of each audio_data u
    should take (sample_rate/gcd) '''
    gcd = math.gcd(sample_rate_1,sample_rate_2)
    num_audio_data1 = int(sample_rate_1/gcd)
    num_audio_data_2 = int(sample_rate_2/gcd)
    num_audio_data = [num_audio_data1,num_audio_data_2]
    return num_audio_data


def step_list_from_list(audio_list,step,num_of_sample):
    '''provide a new list from a list by step and how much sample to take'''
    step_list = []
    len_audio = len(audio_list)
    for i in range(0,len_audio,step):
        for num in range(num_of_sample):
            if i+num < len_audio:
                step_list.append(audio_list[i+num])

    return step_list

def audio_for_merge(audio_data1,sample_rate1,audio_data2,sample_rate2):
    '''compare the sample_rate and tell us how much arguments to take from
    the audio_data'''
    step_by_gcd = num_of_data_for_merge(sample_rate1,sample_rate2)
    step = max(step_by_gcd)
    num_of_sample = min(step_by_gcd)
    if sample_rate1 > sample_rate2:
        first_audio = step_list_from_list(audio_data1,step,num_of_sample)
        return [first_audio,audio_data2]
    if sample_rate1 < sample_rate2:
        second_audio = step_list_from_list(audio_data2,step,num_of_sample)
        return [audio_data1,second_audio]
    return [audio_data1,audio_data2]


def merge_list(audio_data_1,audio_data_2):
    '''merge 2 list to one average_list'''
    new_list = []
    min_length = min(len(audio_data_1),len(audio_data_2))
    for i in range(min_length):
        new_list.append(average_of_lists(audio_data_1[i],audio_data_2[i]))
    if len(audio_data_1) > len(audio_data_2):
        for value in audio_data_1[min_length:]:
            new_list.append(value)
    if len(audio_data_1) < len(audio_data_2):
        for value in audio_data_2[min_length:]:
            new_list.append(value)
    return new_list


def merge_audio(audio_data1,sample_rate1,audio_data2,sample_rate2):
    audio = audio_for_merge(audio_data1,sample_rate1,audio_data2,sample_rate2)
    new_audio = merge_list(audio[0],audio[1])
    return [new_audio,min(sample_rate1,sample_rate2)]



# print(low_vol([[-32760, -100], [-55, -55], [0, 0], [4, -2017], [32767,
# 10002]]))


# print(merge_audio([[20, 20], [40, 40], [60, 60]],2000,[[1, 1], [3, 3], [5,
#                                                                       5],
#
#                                                   [7, 7], [9, 9]],2000))
'''
print(merge_audio([[0, 0], [0, 0], [0, 0], [0, 0]],2200,[[10, 10], [20, 20],
                                                         [30, 30], [40, 40],
                                                         [50, 50], [60, 60],
                                                         [70, 70], [80, 80],
                                                         [90, 90], [100,100]],5500))

print(merge_audio([[20, 20], [40, 40], [60, 60], [80, 80], [100, 100]],2,
                  [[1, 1], [3, 3], [5, 5], [7, 7], [9, 9], [11, 11], [13,
                                                                      13],
                   [15, 15], [17, 17], [19, 19]],3))


'''