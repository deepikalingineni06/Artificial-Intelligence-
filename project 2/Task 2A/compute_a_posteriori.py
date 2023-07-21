import sys
command_line_argument = sys.argv
length_of_command_line_argument = len(command_line_argument)
if length_of_command_line_argument != 2:
    print("The number of arguments should be 1.\n !!Exiting the program..\n")
    sys.exit()
Q = command_line_argument[1]
length_of_Q_string = len(Q)
final_output_string = ""
prior_probabilities_of_bag = [0.1,0.2,0.4,0.2,0.1]
probability_cheery_per_bag = [1.0,0.75,0.5,0.25,0.0]
probability_line_per_bag = [0.0,0.25,0.5,0.75,1.0]
temp_probability_of_bag=prior_probabilities_of_bag.copy()
temp_sum_of_cheery_list_probability = 0.0
temp_sum_of_lime_list_probability = 0.0
final_output_string = "Observation sequence Q: "+Q;
final_output_string += "\nLength of Q: "+str(length_of_Q_string);
for x in range(5):
    temp_sum_of_cheery_list_probability += temp_probability_of_bag[x] * probability_cheery_per_bag[x]
    temp_sum_of_lime_list_probability += temp_probability_of_bag[x] * probability_line_per_bag[x]
for i in range(1,length_of_Q_string+1):
    final_output_string += "\n\nAfter Observation "+str(i) +" = "+ str(Q[i-1])+"\n"
    if Q[i-1] == 'C':
        for j in range(5):
            temp = (temp_probability_of_bag[j] * probability_cheery_per_bag[j])/temp_sum_of_cheery_list_probability
            temp_probability_of_bag[j] = temp
            final_output_string+="\nP(h"+str(j+1)+" | Q) = "+str(temp)
    else:
        for j in range(5):
            temp = (temp_probability_of_bag[j] * probability_line_per_bag[j])/temp_sum_of_lime_list_probability
            temp_probability_of_bag[j] = temp
            final_output_string+="\nP(h"+str(j+1)+" | Q) = "+str(temp)
    temp_sum_of_cheery_list_probability = 0.0
    temp_sum_of_lime_list_probability=0.0
    for x in range(5):
        temp_sum_of_cheery_list_probability += temp_probability_of_bag[x] * probability_cheery_per_bag[x]
        temp_sum_of_lime_list_probability += temp_probability_of_bag[x] * probability_line_per_bag[x]
    final_output_string+="\n\nProbability that the next candy we pick will be C, given Q: "+str(round(temp_sum_of_cheery_list_probability,12))
    final_output_string+="\nProbability that the next candy we pick will be L, given Q: "+str(round(temp_sum_of_lime_list_probability,12))
text_file = open("result.txt", "w")
text_file.write(final_output_string)
text_file.close()