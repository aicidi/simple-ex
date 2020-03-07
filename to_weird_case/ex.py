"""
to_weird_case
"""

def to_weird_case(input_str: str) -> str:
    """
    to_weird_case for loop style
    """
    word_arr = input_str.split(' ')
    result_arr = []

    for word in word_arr:
        temp_arr = []

        for idx, item in enumerate(word):
            if idx % 2 == 0:
                temp_word = item.upper()
            else:
                temp_word = item.lower()

            temp_arr.append(temp_word)

        result_arr.append(''.join(temp_arr))

    return ' '.join(result_arr)

def to_weird_case2(input_str: str) -> str:
    """
    to_weird_case map style
    """
    word_arr = input_str.split(' ')

    result = map(lambda x: ''.join(map(
        lambda y:
        y[1].upper() if y[0] % 2 == 0 else y[1].lower(),
        enumerate(x))), word_arr)

    return ' '.join(result)

print(to_weird_case("Hello hIIi"))
print(to_weird_case("HeDlV VVVV vVv"))

print(to_weird_case2("Hello hIIi"))
print(to_weird_case2("HeDlV VVVV vVv"))
