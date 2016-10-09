from subprocess import call, PIPE, Popen

dependlist = ('pexpect',)

def install_package():
    for package in dependlist:
        try:
            retcode = call("pip install %s" %package, shell=True)
            if retcode < 0:
                print("%s install faild" %package)
            else:
                print("%s install sucess" %package)

        except OSError as e:
            print >>sys.stderr, "Execution failed:", e
install_package()
