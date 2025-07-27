#!/bin/sh

ParasytePath="/mnt/SDCARD/.tmp_update/lib/parasyte"
export PYTHONPATH=$ParasytePath/python2.7:$ParasytePath/python2.7/site-packages:$ParasytePath/python2.7/lib-dynload
export PYTHONHOME=$ParasytePath/python2.7:$ParasytePath/python2.7/site-packages:$ParasytePath/python2.7/lib-dynload
export LD_LIBRARY_PATH=$ParasytePath:$ParasytePath/python2.7/:$ParasytePath/python2.7/lib-dynload:$LD_LIBRARY_PATH

/mnt/SDCARD/.tmp_update/bin/parasyte/python2 RHCompletionMMP.py
