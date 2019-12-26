def abc_to_number(string):
        
        string = string.lower()[::-1]  # reverse and make the string lower-case
        total = 0
        multiplier = 1

        for letter in string:

            if letter < 'a' or letter > 'z':
                raise TypeError("Expected a string of English letters only")

            cur_num = ord(letter) - 96  # 96 is the ascii value of the char before 'a'
            total += cur_num * multiplier
            multiplier = multiplier * 26  # 26 is the number of the letters in the english alphabet

        return total - 1  # -1 to start the counting from 0 -> 'a', and not 1 -> 'a'

def number_to_abc(number):

    string = ""

    while number >= 0:
        cur_chr_num = number % 26  # 26 is the number of the letters in the english alphabet
        cur_chr = chr(cur_chr_num + 97)  # 96 is the ascii value of the char before 'a'
        string = cur_chr + string

        number = int((number - cur_chr_num) / 26) - 1
    
    return string
