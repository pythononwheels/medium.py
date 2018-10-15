#
# generate model
#

import argparse
import tornado.template as template
import os.path
import timeit
import medium.powlib as lib
import medium.config as cfg


def camel_case(name):
    """
        converts this_is_new to ThisIsNew
        and this in This
    """
    return "".join([x.capitalize() for x in name.split("_")])

def generate_auth( model_type,  appname=None):
    """ 
        generates a small handler
    """
    
    #
    # set some attributes
    #
    loader = template.Loader(cfg.templates["stubs_path"])
    handler_class_name = camel_case(handler_name)

    print(40*"-")
    print(" generating Authentication: " + handler_class_name)
    print(40*"-")
    #
    # create the Model
    #
    print("...generating model: type: " + model_type )
    import medium.generate_model as gm
    import os.path
    ret = gm.generate_model("pow_user", model_type=None , appname=appname)    
    assert ret is True

    #
    # create the Auth class
    #
    

    
    
    print("... created: " + ofile_name)
    print(40*"-")
    return


def main():
    parser = argparse.ArgumentParser()
    #parser.add_argument('-n', "--name", action="store", 
    #                    dest="name", help='-n handler name',
    #                    required=True)
    #
    # db type
    # 
    parser.add_argument('-t', "--type", action="store", 
                        dest="type", help="-t type (" + "|| ".join(cfg.database.keys()) + " || none) default=none",
                        default="none", required=False)
    
    
    
    args = parser.parse_args()
    #
    # show some args
    #
    #print("all args: ", args)
    #print(dir(args))
    print("CamelCased handler name: ", camel_case(args.name))
    generate_handler(args.type, appname="pow")

if __name__ == "__main__":
    main()