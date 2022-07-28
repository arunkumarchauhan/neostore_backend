import random
import string
lower = string.ascii_lowercase
upper = string.ascii_uppercase
num = string.digits
symbols = string.punctuation
all = lower + upper + num + symbols

def generate_password(length):
    temp = random.sample(all,length)
    password = "".join(temp)
    return password        