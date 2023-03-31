from tests import *
import inputs
import utils


def run_test(inputs, functions, saved):
    fails = 0
    for function in functions:
        if inputs["go"] == "data" or function == inputs["go"]:
            for k, v in saved.items():
                inputs[k] = v
            if functions[function]() == False:
                fails = fails + 1
                print(function, ": failing")
            else:
                print(function, ": passing")
    return fails


def main(inputs, help, functions, saved={}):
    for k, v in utils.cli(utils.settings(help)).items():
        inputs[k] = v
        saved[k] = v
    if inputs["help"]:
        print(help)
    else:
        print("Testing...")
        fails = run_test(inputs, functions, saved)
        exit(fails)


test_functions = {}

def add_test_function(key, description, function):
    """
    A helper function to add test functions to the dictionary.
    :param key: str, key name for the function
    :param description: str, description of the function
    :param function: function, the test function to be added
    """
    test_functions[key] = function
    # Update help message with the added test function
    inputs.help_string = inputs.help_string + ("  -g  %s\t%s\n" % (key, description))

add_test_function("ok", "check test_ok", test_ok)
add_test_function("num", "check test_num", test_num)
add_test_function("sample", "show test_sample", test_sample)
add_test_function("gaussian", "check test_gaussian", test_gaussian)
add_test_function("bootstrap", "check test_bootstrap", test_bootstrap)
add_test_function("basic", "check test_basic", test_basic)
add_test_function("pre", "check test_pre", test_pre)
add_test_function("five", "check test_five", test_five)
add_test_function("six", "check test_six", test_six)
add_test_function("tiles", "check test_tiles", test_tiles)
add_test_function("sk", "check test_sk", test_sk)

print(test_functions)
main(inputs.the, inputs.help_string, test_functions)