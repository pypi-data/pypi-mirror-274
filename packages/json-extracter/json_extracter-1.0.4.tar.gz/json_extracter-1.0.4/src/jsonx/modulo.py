import re

def split_json_by_bracket(text, bracket_open):
    # cut string by open
    open_text_clean = text[bracket_open:]

    key_close_bracket = open_text_clean.rfind("}")
    key_close_square_bracket = open_text_clean.rfind("]")

    # here we defined in inversed because the find is reversed
    if key_close_bracket < key_close_square_bracket:
        return open_text_clean[:key_close_square_bracket] + open_text_clean[key_close_square_bracket]

    if key_close_bracket > key_close_square_bracket:
        return open_text_clean[:key_close_bracket] + open_text_clean[key_close_bracket]


def json_extract(txt):
    txt_2 = str(txt.replace("\n", ""))
    text = re.sub(r'\s+', '', txt_2)

    # when open is {
    key_open_bracket = text.find("{")

    # when open is [
    key_open_square_bracket = text.find("[")

    # We find key open
    # if we do not have a key open return an error
    if key_open_bracket == -1 and key_open_square_bracket == -1:
        return "bad_json dont have a key open"

    # Use case when text is a object and the first key is '{'
    # key_open_square_bracket = [
    # key_open_bracket = {

    # start with [
    if key_open_square_bracket != -1:
        print(key_open_square_bracket, key_open_bracket)
        return split_json_by_bracket(text, key_open_square_bracket)
    if key_open_bracket != -1:
        return split_json_by_bracket(text, key_open_bracket)
    return key_open_bracket, key_open_square_bracket

