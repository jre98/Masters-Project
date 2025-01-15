
# Function that formats a string (the segmentation points) to be in
# the proper format for detectron2 model
def format_string(input_string):
    # Remove whitespace and newlines
    cleaned_string = input_string.replace('\n', '').replace(' ', '')

    # Split the string into individual values
    values = cleaned_string.split('],[')

    # Remove all the brackets
    values[0] = values[0][1:]
    values[-1] = values[-1][:-1]

    # Join the values into a single string with commas
    formatted_string = ', '.join(values)

    # Add brackets at the beginning and end to enclose list
    formatted_string = '[' + formatted_string + ']'

    # Return the formatted string
    # The string will now be formatted like: [ x1, y1, x2, y2, ... ]
    return formatted_string


# Input string to pass to function
segment = '''
[
                        [
                            1252.0,
                            746.6666666666666
                        ],
                        [
                            1142.6666666666665,
                            566.6666666666667
                        ],
                        [
                            833.3333333333333,
                            765.3333333333334
                        ],
                        [
                            941.3333333333334,
                            941.3333333333334
                        ]
                    ]
'''

# Call function and
formatted_output = format_string(segment)
print(formatted_output)



