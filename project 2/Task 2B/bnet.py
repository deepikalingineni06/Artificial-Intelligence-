# importing libraries
import sys
import copy

# taking required variables
given_prob = {"B": 0.001,"E": 0.002,"A|B,E": 0.95,"A|B,nE": 0.94,"A|nB,E": 0.29,"A|nB,nE": 0.001,"J|A": 0.90,"J|nA": 0.05,"M|A": 0.70,"M|nA": 0.01}
super_node = {'A': ['B','E'], 'B': None, 'E': None, 'J': ['A'], 'M': ['A']}

# function to find probaility when given is there
def get_prob_with_given(argv):
    add_index = argv.index("given")
    after_given_val = argv[add_index+1:]
    before_given_val = argv[1:add_index] + after_given_val
    print("Probability = " + str(calculating_probability(get_notation(before_given_val))/calculating_probability(get_notation(after_given_val))))

# function to get probabilities
def get_prob(temp_data):
    temp_comp = temp_data[0]
    if temp_comp == "n":
        return (1 - get_prob(temp_data[1:]))
    if temp_data in given_prob:
        return given_prob[temp_data]

# function to get notation
def get_notation(current_data):
    res_list = []
    for node_val in current_data:
        temp_comp = node_val[1]
        if temp_comp == "t":
            temp_value_append = node_val[0]
            res_list.append(temp_value_append)
        else:
            temp_value_append = "n"+node_val[0]
            res_list.append(temp_value_append)
    return res_list

# function to get parent nodes
def get_parent_node(current_data):
    result_list = []
    for loop_var in current_data:
        temp_variable = loop_var + "|"
        parent_value = super_node[loop_var[1:]] if loop_var[0] == "n" else super_node[loop_var]
        if parent_value != None:
            for parent in parent_value:
                temp_variable = str(temp_variable + parent + ",") if parent in current_data else str(temp_variable + "n" + parent + ",")
        temp_variable = temp_variable[0:len(temp_variable)-1]
        result_list.append(temp_variable)
    return result_list  

# function to computer probabilities
def calculating_probability(current_data):
    if len(current_data) == 5:
        temp_probability = 1
        for loop_var in get_parent_node(current_data):
            temp_probability = temp_probability * get_prob(loop_var)
        return temp_probability
    else:
        for temp_loop_value in ['A', 'B', 'E', 'J', 'M']:
            if temp_loop_value in current_data: continue
            else:
                missing_node = False
                for array_of_node in current_data:
                    if temp_loop_value == array_of_node[1:]:
                        missing_node = True
                        break
                if missing_node == True:
                    continue
                else:
                    node_missed = temp_loop_value
                    break
        complete_list_data = copy.deepcopy(current_data)
        neg_list_data = copy.deepcopy(current_data)
        complete_list_data.append(node_missed)
        neg_list_data.append("n"+node_missed)
        return calculating_probability(complete_list_data) + calculating_probability(neg_list_data)

# main function
def __main__(argv):
    if "given" in argv:
        get_prob_with_given(argv)
    else:
        print("Probability = " + str(calculating_probability(get_notation(argv[1:]))))

# calling file
__main__(sys.argv)