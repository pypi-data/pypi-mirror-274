# -*- coding: utf-8 -*-
#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.txt', which is part of this source code package.
#

import os


def SetNumberOfThreadsPerInstance(nbThreads):
    """
    Function to enforce the number of threads for various multithreaded libraries.
    This function should be called before importing these multithreaded libraries.
    """

    os.environ["OMP_NUM_THREADS"] = str(nbThreads)
    os.environ["OPENBLAS_NUM_THREADS"] = str(nbThreads)
    os.environ["MKL_NUM_THREADS"] = str(nbThreads)
    os.environ["VECLIB_MAXIMUM_THREADS"] = str(nbThreads)
    os.environ["NUMEXPR_NUM_THREADS"] = str(nbThreads)


def GetNumberOfAvailableCpus():
    """
    Function to discover the number of computing cores available.

    """
    import BasicTools.Helpers.ParserHelper as PH

    SLURM_JOB_CPU_PER_NODE = os.environ.get('SLURM_JOB_CPU_PER_NODE')
    if SLURM_JOB_CPU_PER_NODE is None:
        import subprocess
        import platform
        try:
            out = subprocess.check_output(["/usr/bin/squeue","-h","-t","r","-u",str(os.environ.get("USER")),"-w",platform.node(),"-o","'%C'"], shell=False ).decode("utf-8","ignore")
            out = out.strip().strip("'")
            res = PH.ReadInt(out)
            os.environ['SLURM_JOB_CPU_PER_NODE'] = str(res)
            return res
        except:
            try :
                import psutil
                res = psutil.cpu_count(logical=False)
            except:
                import multiprocessing
                res = multiprocessing.cpu_count()
            os.environ['SLURM_JOB_CPU_PER_NODE'] = str(res)
            return res
    return  PH.ReadInt(SLURM_JOB_CPU_PER_NODE)



class CPU():
    """ Class to help doing the multithreading without using to many cpus
    """
    cpudispo = GetNumberOfAvailableCpus()

    def __init__(self, nbCPUNeeded=-1, WithError=True):
        self.nbCPUNeeded = nbCPUNeeded
        self.nbCPUAllocated = 0
        self.withError = WithError

    def __enter__(self):
        if self.nbCPUNeeded == -1:
            if CPU.cpudispo == 0:
                if self.withError:
                    raise Exception("No more cpus avilable")
                else:
                    self.nbCPUAllocated = 0
            else:
                self.nbCPUAllocated = self.cpudispo
                CPU.cpudispo =0
            return self


        if self.nbCPUNeeded <= CPU.cpudispo:
            self.nbCPUAllocated = self.nbCPUNeeded
            CPU.cpudispo -= self.nbCPUNeeded
        else:
            if CPU.cpudispo == 0:
                if self.withError:
                    raise Exception("No more cpus avilable")
                else:
                    self.nbCPUAllocated = 0
            else:
                self.nbCPUAllocated = self.cpudispo
                CPU.cpudispo =0

        return self

    def __exit__(self, type, value, traceback):
        CPU.cpudispo += self.nbCPUAllocated
        self.nbCPUAllocated = 0

def CheckIntegrity():
    try:
       with CPU(2) as cpu:
        print("CPU ask 2 Allocated :" + str( cpu.nbCPUAllocated))
        print("CPU dispo " + str( CPU.cpudispo))
        with CPU() as cpu2:
            print("cpu2 ask max available, Allocated : " + str( cpu2.nbCPUAllocated))
            print("CPU2 dispo " + str( CPU.cpudispo))

            with CPU(7,False) as cpu3:
                print("cpu3 ask 7 Allocated  " + str( cpu3.nbCPUAllocated))
                print("CPU3 dispo " + str( CPU.cpudispo))
    except Exception as e:
         print(e)

    #     pass
    print("CPU dispo " + str( CPU.cpudispo))
    print("GetNumberOfAvailableCpus", GetNumberOfAvailableCpus())
    return "ok"

if __name__ == '__main__':# pragma: no cover
    print(CheckIntegrity())
