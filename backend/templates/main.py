import arrr
from pyscript import document


def translate_english(event):
    
    input_text = document.querySelector("#english")
    english = input_text.value
    output_div = document.querySelector("#output")
    output_div.innerText = english + " Jackson"
