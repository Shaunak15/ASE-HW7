from tests import *
import inputs
import utils

def main(inputs, help, funcs, saved = {}, fails = 0):
    for k, v in utils.cli(utils.settings(help)).items():
        inputs[k] = v
        saved[k] = v
    if inputs["help"]:
        print(help)
    else:
        print("Testing...")
        for what in funcs:
            if inputs["go"] == "data" or what == inputs["go"]:
                for k,v in saved.items():
                    inputs[k] = v
                if funcs[what]() == False:
                    fails = fails + 1
                    print(what, ": failing")
                else:
                    print(what, ": passing")
    exit(fails)

egs = {}
def eg(key, str, func):
    egs[key] = func
    inputs.help_string = inputs.help_string + ("  -g  %s\t%s\n" % (key,str))


eg("ok","check test_ok",test_ok)
eg("num","check test_num",test_num)
eg("sample","show test_sample", test_sample)
eg("gaussian","check test_gaussian",test_gaussian)
eg("bootstrap","check test_bootstrap",test_bootstrap)
eg("basic","check test_basic", test_basic)
eg("pre","check test_pre",test_pre)
eg("five","check test_five", test_five)
eg("six","check test_six", test_six)
eg("tiles","check test_tiles", test_tiles)
eg("sk","check test_sk", test_sk)

print(egs)
main(inputs.the, inputs.help_string, egs)