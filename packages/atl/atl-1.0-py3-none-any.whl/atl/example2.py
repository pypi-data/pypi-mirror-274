from atl.example1 import example1_add as example1_add

def example2_greet():
    return "Hello from Module 2!"

def example2_subtract(a, b):
    return a - b

def example2_depending_on_example1_add(a, b):
    return example1_add(a,b)