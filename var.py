def write(name, value):
    try:
        f = open("var/" + name + ".dat", "w")
        f.write(value)
        f.close()
    except Exception as ex:
        print('VAR :: Failed to write to file ' + str(ex))
    
def read(name):
    try:
        f = open("var/" + name + ".dat", "r")
        return f.read()
    except:
        return "err0"