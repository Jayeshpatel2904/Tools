input_string = "apple,banana,cherry,date,fig,grape,kiwi,lime,mango"

# Split the string into a list of elements
elements = input_string.split(',')

# Get the first 8 elements using slicing
first_8_elements = elements[:8]

# Combine the elements back into a single string with ","
combined_string = ",".join(first_8_elements)

print("Combined string:", combined_string)