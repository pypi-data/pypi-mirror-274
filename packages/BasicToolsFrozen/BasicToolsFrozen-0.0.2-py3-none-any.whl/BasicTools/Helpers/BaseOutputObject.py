# -*- coding: utf-8 -*-
#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.txt', which is part of this source code package.
#

""" Base object to Help output

"""
from __future__ import print_function
import sys
import time
import inspect
from functools import wraps

_startTime = time.time()
useDifferentialTime = True
useFroze_itDecorator = False

from BasicTools.Helpers.TextFormatHelper import TFormat

def ResetStartTime():
    """
    Function to reset the start time of a program.

    """
    global _startTime
    _startTime = time.time()

def SetUseDifferentialTime(val):
    """
    Function to set the printing format

    :param [val]: True to print the time from the begining of the program or False to print the current time, defaults to [True]
    :type [val]: [Bool]
    """
    global useDifferentialTime
    useDifferentialTime = val


##https://stackoverflow.com/questions/3603502/prevent-creating-new-attributes-outside-init
##https://hynek.me/articles/hasattr/
sentinel = object()
## for the moment if a class is frozen no heritage is possible ... working on a solution
def froze_it(cls):
    """
    Decorator to make the class immutable (no more attributes can be added after initialization)

    For the moment if a class is frozen no heritage is possible.
    """
    if not useFroze_itDecorator:
        setattr(cls, "UnFrozen", lambda x: None )
        setattr(cls, "IsFrozen", lambda x: False )
        return cls

    cls.__frozen = False

    def frozensetattr(self, key, value):

        y = getattr(self, key, sentinel)

        if self.__frozen and y is sentinel:
            raise(Exception("Class {} is frozen. Cannot set {} = {}"
                  .format(cls.__name__, key, value)))
        else:
            object.__setattr__(self, key, value)

    def init_decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            func(self, *args, **kwargs)

            def UnFrozen():
                self.__frozen = False
            setattr(self, "UnFrozen", UnFrozen)

            def IsFrozen():
                return self.__frozen
            setattr(self, "IsFrozen", IsFrozen)

            self.__frozen = True
        return wrapper

    cls.__setattr__ = frozensetattr
    cls.__init__ = init_decorator(cls.__init__)

    return cls

class BaseOutputObject(object):
    """
    Base class for almost all the classes in BasicTools. The principal functionality of this class is to handle output to the console with different level of verbosity. the user can change verbose level for a specific instance or to all the instances in a program.

    """
    __globalDebugMode = False
    __verboseLevel = 1
    # constants
    # please do not change this values
    RETURN_SUCCESS = 0
    RETURN_FAIL = 1
    RETURN_FAIL_EXTERNAL_TOOL = 2

    def __init__(self, other = None):
        super(BaseOutputObject,self).__init__()
        if other is not None:
            self.__classDebugMode = other.__classDebugMode
        else:
            self.__classDebugMode = False
        #only for debuging
        self.desc =""

    @classmethod
    def SetVerboseLevel(cls,level):
        BaseOutputObject.__verboseLevel = level

    @classmethod
    def GetVerboseLevel(cls):
        return BaseOutputObject.__verboseLevel

    @classmethod
    def SetGlobalDebugMode(cls, mode = True):
        BaseOutputObject.__globalDebugMode = mode

    @classmethod
    def IsGlobalDebugMode(cls):
        return BaseOutputObject.__globalDebugMode

    def SetInstanceDebugMode(self, mode = True):
        self.__classDebugMode = mode

    def PrintProgress(self,val,  maxx = 100,minn= 0):
        per = (float(val) -minn)*100/(maxx-minn)
        if per == round(per):
            self.Print(str(round(per)) +"%")

    def PrintDebug(self, mess):
        self.PrintInternal( mess, 3)

    def PrintVerbose(self, mess):
        self.PrintInternal(mess, 2)

    def Print(self, mess):
        self.PrintInternal(mess, 1)

    def PrintError(self, mess):
        self.PrintInternal(TFormat.InRed("Error: ") + str(mess), 1)

    def InDebugMode(self):
        return (BaseOutputObject.__globalDebugMode or self.__classDebugMode)

    @classmethod
    def Print2(cls,mess):
        a = BaseOutputObject()
        a.PrintInternal(mess,1)

    @classmethod
    def GetDiffTime(obj = None):
        global __startTime
        return  (time.time() - _startTime)

    def PrintInternal(self, mess, level=1):
        if BaseOutputObject.__globalDebugMode or self.__classDebugMode :
            res = ""

            stnumber = 1
            stack = inspect.stack()[stnumber]

            # check if the we call PrintInternal directly of using the PrintDebug proxys
            if 'PrintInternal' in stack[4][0] :
                stnumber += 1
            # the real stack
            stack = inspect.stack()[stnumber]

            #res += (": "+str(stack[1]) + ":" +str(stack[2]) )
            res += '  File "' + str(stack[1]) + '", line ' +str(stack[2])

            # nice date
            global useDifferentialTime
            if(useDifferentialTime):
                res += (" [%f]" % self.GetDiffTime() )
            else:
                m, s = divmod(time.time(), 60.)
                h, m = divmod(m, 60)
                d, h = divmod(h, 24)
                res += ("[%d:%02d:%02d]" % (h+1, m, s))

            try:
                import psutil
                res += " [%.2fMB]" % (psutil.Process().memory_info().rss/ (1048576))
            except:
                pass

            if level == 1 :
                res += (TFormat.InBlue(" --> "))
            elif level == 2:
                res += (TFormat.InGreen(" V-> "))
            else:
                res += (TFormat.InRed(" D-> "))
            # we recover the code of the line to print it
            # some cleaning
            if type(mess) is not str:
                stack = inspect.stack()[stnumber]
                # we replace BaseOutputObject() to "" in case is present
                st = str(stack[4][0]).replace("BaseOutputObject()","")
                res += (")".join("(".join(st.split("(")[1:]).split(")")[0:-1]) )
                res += (" -> ")
            #print(" [" + str(memory()) + "]"),
            res = res +  ("\n" + res).join(str(mess).splitlines())
            res += "\n"
            print((res), end='')
            return
        elif level <= BaseOutputObject.__verboseLevel :
            print(mess)

        sys.stdout.flush()
    def  __str__(self):
        res = str(type(self)) + "\n"
        for prop in self.__dict__:
            res += str(prop) + " : " + str(self.__dict__[prop])
            res += "\n"
        return res

def CheckIntegrity(GUI=False):

    myObj = BaseOutputObject()
    VLevel = myObj.GetVerboseLevel()
    myObj.Print("Print 1")
    myObj.PrintVerbose("PrintVerbose 1")
    myObj.PrintDebug("PrintDebug 1")
    myObj.SetVerboseLevel(2)
    myObj.Print("Print 2")
    myObj.PrintVerbose("PrintVerbose 2")
    myObj.PrintDebug("PrintDebug 2")
    myObj.SetInstanceDebugMode()
    myObj.Print("Print 3")
    myObj.PrintVerbose("PrintVerbose 3")
    myObj.PrintDebug("PrintDebug 3")
    myObj.SetInstanceDebugMode(False)
    myObj.Print("Print 4")
    myObj.PrintVerbose("PrintVerbose 4")
    myObj.PrintDebug("PrintDebug 4")
    myObj.SetGlobalDebugMode(True)
    myObj.Print("Print 5")
    myObj.PrintVerbose("PrintVerbose 5")
    myObj.PrintDebug("PrintDebug 5")

    myObj.Print([3+1,8])
    myObj.PrintVerbose([3+2,8])
    myObj.PrintDebug([3+3,8])

    myObj.Print(list(range(4)))

    var = 4
    myObj.Print(var)

    myObj.Print2("Print 5")
    myObj.PrintError("Print 6")
    myObj.InDebugMode()

    myObj.PrintProgress(50)
    global useDifferentialTime
    SetUseDifferentialTime(False)
    myObj.PrintProgress(50)

    myObj2 = BaseOutputObject(myObj)

    class TOTO():
        tata = ["titi","tutu"]
    toto = TOTO()

    BaseOutputObject().PrintDebug(toto.tata)

    @froze_it
    class FrozenTest(BaseOutputObject):
        def __init__(self):
            self.a = 3

    @froze_it
    class FrozenSubClass(FrozenTest):
        def __init__(self):
            super(FrozenSubClass,self).__init__()
            print(self.UnFrozen())
            self.b = 50

    if useFroze_itDecorator:

        obj = FrozenTest()
        obj.a = 5
        try:
            obj.b = 7
            return "Error in a frozen class"
        except Exception as inst:
            pass
            print(inst)
            print("this error message is normal")
        obj.__frozen = False
        obj.b = 7



        obj = FrozenSubClass()
        obj.b = 5
        try:
            obj.c = 7
            return "Error frozing subclass"
        except Exception as inst:
            pass

        obj.UnFrozen()
        obj.c = 7

    myObj.SetVerboseLevel(VLevel)
    myObj.SetGlobalDebugMode(False)
    myObj.SetInstanceDebugMode(False)
    return "OK"

if __name__ == '__main__':
    print(CheckIntegrity(GUI=True))# pragma: no cover
