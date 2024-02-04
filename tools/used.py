"This file is the data preprocessing and other work done for each experiment."
#1.Remove the elements of the delete list and process the data in latex data formaty
#2.Separation of node attributes
#3.Sort by 'Similarity' column in each grouping
#4.CSV data deduplication
#5.Statistical data set text length
import ast
import re
import numpy as np
import csv
import pandas as pd
#
##################################################################################################
##Remove the elements of the deletion list and process the data in latex data format
# delete_list = ['RightAngle','Right','Isosceles','Equilateral','Regular', 'Red','Blue','Green','Shaded']
#
#
# def convert_latex_to_plain_text(latex_code, delete_list):
#
#     latex_code = re.sub(r'\\frac{([^{}]*)}{([^{}]*)}', r'\1/\2', latex_code)
#     latex_code = re.sub(r'\^{([^{}]*)}', r'**\1', latex_code)
#     latex_code = re.sub(r'\\sqrt{([^{}]*)}', r'√\1', latex_code)

#     delete_pattern = r'\b(?:' + '|'.join(re.escape(word) for word in delete_list) + r')\b\((.*?)\)'
#     latex_code = re.sub(delete_pattern, r'\1', latex_code)

#     return latex_code

# # example
# latex_code = "Isosceles(Triangle(A,B,C))"
# converted_code = convert_latex_to_plain_text(latex_code,delete_list)
# print(converted_code)
##################################################################################################


##################################################################################################

#################################################################################################################
# #Node attribute separation
# def attribute_handling(data):
# # Remove the '[' at the beginning and ']' at the end of the string
#     data = data[1:-1]
#
# # Separate string by first ','
#     split_data = data.split(',', 1)
#     print(split_data)
# # Remove the single quotes from the first element
#     first_element = split_data[0].strip("'")
#
# # Remove the first space from the second element
#     second_element = split_data[1].lstrip()
#     return first_element,second_element
#
#
# # Input file name and output file name
# input_file = 'Com_Graph_data.csv'
# output_file = 'output.csv'
#
# # Read the original CSV file data
# with open(input_file, 'r') as file:
#     reader = csv.reader(file)
#     next(reader) # Skip the first line
#     data = list(reader)
#
# #Expand two columns of data
# for row in data:
#     row.append(row[4]) # Add the 5th column of data to the "Source_Sign" column
#     row.append(row[5]) # Add the 6th column of data to the "Target_Sign" column
#     first_element, second_element = attribute_handling(row[4])
#     row[4] = first_element
#     row[6] = second_element
#     first_element, second_element = attribute_handling(row[5])
#     row[5] = first_element
#     row[7] = second_element
#
# # Write expanded data to a new CSV file
# with open(output_file, 'w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerows(data)
#
# print("CSV file has been created and saved as output.csv")
##########################################################################################################
#########################################################################################################
#Group by 'Batch' and sort by 'Similarity' column in each group
# df = pd.read_csv('Geo_sim_data_no_com.csv')
# df['sort'] = df.groupby('Batch')['Similarity'].rank(method='first')
# # Save the CSV file containing the sorted results
# df.to_csv('Geo_sorted_file_no_com.csv', index=False)

##########################################################################################################
#########################################################################################################################
# Deduplicate the first column of data
# df = pd.read_csv('Geo_Logic_form_language.csv')
#
# # Deduplicate the first column of data
# df.drop_duplicates(subset=df.columns[0], keep='first', inplace=True)
#
# # Save results to a new CSV file
# df.to_csv('Geo_Logic_form_language.csv', index=False)
#########################################################################################################################
# # Count word count
# df = pd.read_csv('geo_en_text.csv',encoding='latin-1')
# text_column = df['translated_subject']
#
# # Calculate the number of Chinese characters in each line
# word_counts = text_column.str.split().str.len()
#
# word_count = word_counts.sum()
# print(word_count / 4747)
# # Count the number of sentences with words greater than or equal to 3, 5, 10 and 12
#
# # count_ge_1 = (word_counts ==1).sum()
#
#
# word_counts_dict = {}
# for i in range(1, 101):
#     word_counts_dict[i] = (word_counts == i).sum()
#
# #Print results
# for word_count, row_count in word_counts_dict.items():
#     print(f'Number of rows with word number {word_count}: {row_count}')
#
# # Convert dictionary to DataFrame
# df1 = pd.DataFrame(list(word_counts_dict.items()), columns=['Number of words', 'Number of rows'])
#
# # Save DataFrame as CSV file
# df1.to_csv('word_counts.csv', index=False)