
def clean_multiple_space(string):
    multiple_space_list=["   ","  "]
    for spaces in multiple_space_list:
        string=string.replace(spaces," ")
    return string
