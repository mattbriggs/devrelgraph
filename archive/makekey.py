

def create_unique_id(number):
    letters = "abcdefghijklmnopqrstuvwxyz"
    number = int(number)
    outstring = ""
    while number > -1:
        if number < 26:
            a = letters[number]
            outstring += a
            return outstring
        else:
            number = number-26

def def_make_alpha(number):
    letters = "abcdefghijklmnopqrstuvwxyz"
    outstring = ""
    instring = str(number)
    while len(instring) > 0:
        outstring += letters[int(instring[0])]
        instring = instring[1:]
    return outstring


for i in range(400):
    print(i, def_make_alpha(i))