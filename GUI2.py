#from multiprocessing.connection import wait
from shutil import move
import PySimpleGUI as sg
from zaber_motion import Library, Units
from zaber_motion.ascii import Connection
from zaber_motion.ascii import Lockstep
import time
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import Slider, Button, RadioButtons
import pandas as pd

''' to do: deal with not integer inputs
make other ok button go on enter
do send to specific location'''

Library.enable_device_db_store()

import sys
import glob
import serial

sg.theme('Reddit')

# max postions in mm
MAX_X = 151.49909375
MAX_Y = 151.49909375
MAX_Z = 40.000047

# move distance in mm
DIST = 15

left64 = 'iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAMAAACdt4HsAAAANlBMVEUAAAAAqv8AgL8chNkiiNUhhNYfhNcghNgghdgfhNggg9ggg9gghNgghNgghNgghNgghNj///90+N/XAAAAEHRSTlMAAwQbHh86j5CipanF3d/06MxMzgAAAAFiS0dEEeK1PboAAABcSURBVFjD7ZZJCoBAEMTc9yX/f60HfzABQa3cE+iBobuqQgjvodvO0fj9AQzSF4Hbn8vn3wHWJn78P/rtAbDUxR9okr4P6BH0I6aQwhcLdrn69e4PDH/ihBAe4QJu2Ax3gaY3zgAAAABJRU5ErkJggg=='
Left64 = 'iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAMAAACdt4HsAAAAPFBMVEUAAAAXi9Egh9cfg9gfhdkfg9kfhNchg9ghhNghhdgghNkfhNghhdgghNgghNgghNgfhNgghNgghNj///9MJE9iAAAAEnRSTlMACyAhSUpTVFVWV1tc2eT5+/yS4ZH/AAAAAWJLR0QTDLtclgAAAHJJREFUWMPtlUkOwCAMA6ErpQvB/39s75VCQDnWcxsJW8oFh0AIIR3Ma2y6xVFwx4ZbZAGw6N6VL5PqXXlJqlskAVBP1ZlnvsUmACSrbvJ83j+DeX+B+4SwC4B6qc4GNow1eL91/7D4p80/rv55J4T8ixeaxhdxB5W+RQAAAABJRU5ErkJggg=='
right64 = 'iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAMAAACdt4HsAAAANlBMVEUAAAAAqv8chNkhhNYfg9geh9ofhNcghNgghdgfhNgfg9ggg9ggg9gghNggg9gghNgghNj///+0c9rnAAAAEHRSTlMAAxsfISI6j5Cio6XG3+H03k1vTQAAAAFiS0dEEeK1PboAAABaSURBVFjD7ZZLDoAgFMRA8AeCvf9p3bqfREmY7tvkreaFYIwZnf2+kuJvQEtiQCsUtRBPgL664IILr0IFaItaOP4LqCfEAtCzffsz+vK4yvMuPxjyi2OM+ZgH5MEMTUJo/boAAAAASUVORK5CYII='
Right64 = 'iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAMAAACdt4HsAAAAOVBMVEUAAAAXi9Egh9cfg9gfhdkfg9kfhNchg9ghhNgghNkfhNghhdgghNgghNgghNgfhNgghNgghNj///9KJSBFAAAAEXRSTlMACyAhSUpTVFVXW1zZ5Pr7/OvXKIEAAAABYktHRBJ7vGwAAAAAcklEQVRYw+2VOwrAMAxD+2/TTxzd/7IdOiXguMVkqt72BgkMIeo6QgjR6Oex6mb+RAwVN5kASNDdZIh5onSbIHmidJtVAKRDdTaw4VvD8wYX1V82XLo3L/CesAmAtKvOPPMtv3X3sLinzT2u7nknhPyWG6qnFh1x6ykSAAAAAElFTkSuQmCC'
up64 ='iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAMAAACdt4HsAAAAQlBMVEUAAAAAqv8AgL8chNkjhNwiiNUhhNYeh9oehtgghNgghdgfhNgfg9ggg9ggg9gghNgghNgghNggg9gghNgghNj////j/00fAAAAFHRSTlMAAwQbHR4fIjuPkKKjpanF3d/h9OWAHaoAAAABYktHRBXl2PmjAAAAlElEQVRYw+2SyQ6AIAwFwX1f+//fqgaNGzRSjr65NjMUglIAAPAX4qqKQ/x0IJpyuZ+NtDJmYb68sO1vkN3CnN+20h3M+V2ka9kOh6+UrHD6ssLVlxTuvn/h6fsW3r5fweb7FOz+94LL/1rY/6+2zbT51Qkb6N3+UejZwMz4e2FmAyVRo93j7R1K/hGKImwOAADg5yylmw+GfHyoKgAAAABJRU5ErkJggg=='
Up64 = 'iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAMAAACdt4HsAAAAP1BMVEUAAAAXi9Egh9cfg9gfhdkfg9kfhNchg9ghhNghhdgghNkfhNghhdgghNgghdgghNgghNgfhNgghNgghNj///80NE/FAAAAE3RSTlMACyAhSUpTVFVWV1tc2eX5+vv8OHqK5gAAAAFiS0dEFJLfyTUAAACbSURBVFjD7ZTbCoAgEAW1e3axbf//XwOL6KKI61N05jGYIWE5SgEAPkEzz02O3xHzOub5OQXjfGYyGT6RuOD+fx1aEr7i8JUSFk5fWLj4osLNFxQefnLh5ScWPH5SwfhPZ//cxf1iCZyeK9giGqiCp+sKVTSgJ16Mfw96y5OOv0HXZWgPylpjD7AH2IOv7sENwR48SN4DAMCv2ADAghiPhcz6cgAAAABJRU5ErkJggg=='
down64 = 'iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAMAAACdt4HsAAAASFBMVEUAAAAAqv8AgL8fhdYchNkjhNwiiNUhhNYfg9gehtgghNgghdgfhNgfg9ggg9ggg9gghNgghNgghNgghNggg9gghNgghNj////IKi6QAAAAFnRSTlMAAwQZGx0eHyE7j5Cio6Wpxd3e3+H0b8Dv0gAAAAFiS0dEFwvWmI8AAAChSURBVFjD7ZVJEsIgEADBDZOYRWP6/0/1QJW4MBgmR6evVDcUUOCcYRiGYcg0zbbxFnovD/sLtMXAAgxiwQ/AUgxMFAp+AJiKgTDLhejPx/ImnK4A4y7j9wD3869jkAprfamw3s8Xavxcoc7/LtT6n4V6/72g8V8LOj8VtP7zVsf7GzRPQ1yDdv60Bu38qaD3nQu3bb5z+6472EdhGMbf8AC7bxEd9IMMvAAAAABJRU5ErkJggg=='
Down64 = 'iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAMAAACdt4HsAAAAQlBMVEUAAAAXi9Egh9cfg9gfhdkfg9kfhNkfhNchg9ghhNghhdgghNkfhNghhdgghNgghdgghNgghNgfhNgghNgghNj////GIpG9AAAAFHRSTlMACyAhSUpRU1RVVldbXNnl+fr7/OKBPssAAAABYktHRBXl2PmjAAAAp0lEQVRYw+2UyQ7DIAxEszcJzebM/39rD1WikBoB7qWVZo6g9ySDNUXBMAwTStnWoau6LRP4GZvTr8YVc9zQABDV4ARAExVUW8DgBMBaxWdwohrex0PKK/YCYJ/8w0EA7M+0f1AMWbxiyOQ/DNn8zWDgPYOJvxiM/Gkw88fqSHC1Ew1f8Ichl7/2QS/e/IY+6JblwT5gH7AP/rUP7u9gm1/tA4ZhfjovXZgaD96FIfoAAAAASUVORK5CYII='
uparrow64 = 'iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAMAAACdt4HsAAAANlBMVEUAAAAig9cfhNkfhNchg9ghhNgghNkfhNghhdghgtcgg9cghNgghdgfhNgghNgghdkghNj////GrReWAAAAEHRSTlMATFFTVFVXW1yFhuTl+/z8mxBGIgAAAAFiS0dEEeK1PboAAAC0SURBVFjD7dbRDoMgDIXholO3Acr7P+0GKFKTCS1L9KLn/v+MiU0EkN1+r2V5t/SD++7Z0FsPzGxhDL1zdmzrucKQet5bhH4Oz2cJsZ888OAIaw8eAIaw9RGgC6lfAaqw9xtAE7I+ARQh73egXkB9BtQKuM+BOqG3+NPPgXgctjsF9OF0EBAFXQLQ6WEgCOeAMqaH3wB0xijSTRwB8gQQQAABBBBAgD8DuvQ/UJqi/g/ILtkHVakW4BmoCSUAAAAASUVORK5CYII='
Uparrow64 = 'iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAAAXNSR0IArs4c6QAAAqpJREFUeF7tmb9v00AUx79nZ+FPQKAkBIm4IPEH0AV25kogQOqAOrMh5EpIWDAyVyyo/JI6s5cFdpbWYUidCP4GlsaHDjWS49q+5/TunNYvo/3y7r6fe+9r+06g5T/Rcv1gAFwBLSfALUApgH4UvwWwBeASJX4FYv4C2EnC4JluLtoK6EWHdwTEd12iVbwvIdcn4dqPqrkxAMrKtboFKIDOc4y2Bc6zOMrcGQCF0kWO4Qq4yKtL0dZoBXRfx+tqktMXQWMvWs0A2JN+bzR6LwQeKQAS+DC5MdzEhphRVs1kjHsAe9Lvj0a7EHi4IETiczIcPnENwS2Al/udvn/5EwQ2ilaxiUpwB6Bs5fMkHFeCGwBU8XMYDiHYB6Ap+zJDc9UOdgGUix8DGORMcAqBbvaaCwj2AFSI9zqze+mxP8mKTX3vunec7ruGYAeARvz4+a1pP4plFkASBqL75tfANQTzAAjilfAiAOq6awhmARDFVwFwDcEcgBridQBcQjADoKZ4CgBXEIwA6EXxrgAe557piUB69yi8ueD285gyD8i/F1yLDnoS3jdlGwuPSImPk+0gP2bt76QzAyg5N6gUT62AuZpSCIR9fx0RGwC04usCUPFFECgHH9YBnIhRR2dPAfz0OrMH6jmvG5jaAtk8/yFI7wsEbgN4Rzn60s3jzBWgG6Ds/jIAlh2r6n8MwAZVSk6ugIJvAQo40zHcAqaJUvNxC3ALnN4PoFaPyTj2AJM06+RiD2APYA84tSlap4VMxbIJmiJZNw+bIJsgmyCbYNY31NFYXR8xEd/IoMtsipoQW5SDAdgiq8vLj8Eo/g3gygmoP0kYXNVBs3G/sRYYvDq8n3piR4nyUrk13l77akOgLmdjAHQTc3WfAbgivarjcAWs6sq4mlfrK+AfAL9+UDFlSjgAAAAASUVORK5CYII='
Downarrow64 = 'iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAMAAACdt4HsAAAAS1BMVEUAAAAAqv8AgL8iiNUhhNYeh9ofhNcehtgig9cghNgfhNgfg9ggg9ggg9gghNggg9gghNgghNggg9gghNgghdgghNgghNgghNj///+4dvnuAAAAF3RSTlMAAwQeHyI6O0yPoqOlqcXG3d/h5OX09pS74+AAAAABYktHRBibaYUeAAAAvklEQVRYw+3W2Q6DIBRFUahURTtZh/3/f9oHa8HEpgxNbJN73s/iQgJBKcnPpx6GOgvooc8CAAQQQAABBNgRsOPVbAPFZbSf+yXQmS3AdEAZBDjBA0xHEKBaX3DA3G8CzkA3APfjGihuAOeDihQWIKa/Ep5AXN8XZiC27wkACX0nAKT0XwJAUn8RlsT3ldIn1z/plJvohLS+20XK/P4MqesvM7Q660mqKvlt/1XsRHAm++Y5D0/5fSB7C5Id8wDzHisbuT9pYwAAAABJRU5ErkJggg=='
downarrow64 = 'iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAMAAACdt4HsAAAANlBMVEUAAAAig9cfhNkfhNchg9ghhNgghNkfhNghhdghgtcgg9cghNgghdgfhNgghNgghdkghNj////GrReWAAAAEHRSTlMATFFTVFVXW1yFhuTl+/z8mxBGIgAAAAFiS0dEEeK1PboAAAC0SURBVFjD7de7EoMgEEBRjAaTwOr9/69NEXzgJCJrEYvd/p6CAQacs7n8NDE2p4AA4RQAYIABBhhggAEG/BNoYmz3gFvpvRBA/G/AS+m9EMiFHPBCCWglFzLACyC3/UXoBBge34C7AENfWsZcWAEH+42wAIf7XJiBij4TJqCqXwsJqOxXwgeo7hcBQNPPAoCqnwQAXZ+ENJo+bX3YHC+NoO0nQd871wH0Z+7E5zi+7ON3/XkDcjIW2MImT4kAAAAASUVORK5CYII='
home64 = 'iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAMAAACdt4HsAAABLFBMVEUAAAAA//8AgP8AgL8zmcwrgNUkktsggN8agMwrgNUnidgkgNseh9IbhtckhtsjgNwfhdYdgNgchNkiiNUgh9cjh9Uig9Yfg9ojhdYhhdgfgtsigtkhhNkfhtcfhNcihNkghtchhdYfhdoghNghhNghhdghhNkghdchhdkghNggg9ghhdgghdghhdggg9cgg9gghNghhNcgg9cghdgghNghhdchhNgghNgfg9ghhNggg9cgg9gghNgghNcghNgghNgghNgfhNchhNgghNghg9gghNgghNkghdghhdgghNgghNgghNgghNgghNgghNggg9gghNgfg9gghNgghNgghNgfhNgghNgghNgghNgfhNgghNgghNgghNgghNgfhNgghNgghNgghNgghNj////KA44JAAAAYnRSTlMAAQIEBQYHCAoMDQ4RExUWGRobHiAkJSksLjE1Njk6PD9FS09VXF1gZGhvdXd9gIiJjY6QkZScnaOkp6mqrrK1uLu8vsTFx8rM0tbY2dre4eLj5Obn6+3u8PP19vj6+/z9/khd6SIAAAABYktHRGNcvi2qAAABeUlEQVRYw+2V11YCMRRFo2JvWLGiYi/YRuyiYu8dBQuw//8jfAAXzEwgyfika/Zb7qxzXmbnRoj/Tqdldf4mH7qHp37v+XASIBn2mo+kASAd8Zaf+qRAZsZLfj4HEI0C5OaN41XLAJlZIaa/ANaqzfI1GwAfE0IIMf4OsBUwyTfsA6TG8qfRN4DDJv18yzHA88DPue8R4KxNN99xAXDbU5x0XwNcdunrB+ftpbPWU9CVcugF4KjZPm08AHgdUefHUgB79c557baelJOfADHJX69a0ZFyLguwJP+4AJBb1NJPjkrKmvWifnLyUm4GdPSTU0lKp35yyktZ0K9X9ZvKSRm6c+snRy7lcBIgoXXhmhIAyUHbMA2wU6d3Wep2AK5ss3L6yamOAbgKTDaOX/AnCoLWrgMraFRwgosTo4KsuyBrVIAE44KJEjwVmJz9Ar/AL/hfBc4FslqCasFIV5gKoViiKmxLVrbGVdjWvOshid88OLiJV3po/jTfY5lgbQUAo8kAAAAASUVORK5CYII='
centre64 = 'iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAMAAACdt4HsAAABSlBMVEUAAAAA//8AgP8Aqv8AgL8zmcwrgNUggNUfhdYeh9odg9sjh9Uig9Yihtcghtkfg9oehtsegtUigtchgtkghdofgtsfhNcehtgihNkhhtkhhNoghtcig9ohhdYghdcgg9gfhdkghNgfhNkfg9chg9ghhNgghNkghdkghNcfhdcfhNghhdgfg9khhNcghNggg9khhdgghNkgg9cgg9gghNgfg9gfhNgghNgghdgghNgghdgghNkfhNcfhNghhNgghNgghNkfhNggg9cghNggg9gfhdgghdkghNcghdgghNgghdghhNcghNgghNgghNgfhNgghNggg9gghNkghdcghNgghNgghNgghNgfhNkghNgghNgghdgghNgghNgghNkghNgghNgghNgghNgghNgghNgfhNgghNgghNgghNgfhNgghNgghNgghNj///9Gky58AAAAbHRSTlMAAQIDBAUGGBkiIyQlJigpKistLzAxOjs8PT4/REVHSElPUVJUVVdYWVpbXGtsbnF9foCIiYqLj5CRmJmam5ydn6KnqKmrra6vsLG0tba3w8XGx8jP0NHS29zd5ebn6O3u7/Dx8vP2+Pn7/P1/wT9DAAAAAWJLR0RtuwYArQAAAnlJREFUWMPtl91bUkEQxhdFBBElLU0tv0WQwtQI6EMQkKJIsQTFjyQwQPj9/9ddnNQDnl0OnQufepy7mT3ve3ZmZ2dmhfjfxRmNOi0R5CFviaAFLUsEAA8EVggeBTYBNv3evwDbZuI/uJHz7WlbT/A+/xEdUlztgeLJdwzkYNzs7tcbGqKa2wJ4natqeiNkahMDOwBcJZ/3X5+CfTbVBCBhN4H/DMCuq/0Y3RkAsl0ZbDsAFwt382DpJ0CimxfrAMcuo0RylwBCavzjBnA8aJyJgyWgoTyLvm/AhevWUIParTZUBvIqJ/wACzpDBCI6dRHAp4jgEbDbZpqcbFMzQFG+hRngyqXy0d0EpqTLcSCpjnIaeC/14Bx4piaYA85ki16g0q+3OIKxWNCht9gvgVEJQQD4ojeMFAEKHr1tD1iVEGwCW/r/F7VbWNDvIQxsdPavfKvj6tciQggRvFYDQggRqXV81Mpfd72oQfWYEELEgGQKiAohJgw+ipogSKVNEMhcWDPrgjSIBe3LwwGd8Y1BEPVXKac3eAoAh8Nmj9ELVNtqlmMtFvUPtFW8S2BElcqz6lSeB06lq9tAqvtleiddnQaabhXeo77OtiKQURWULFBQ1DQfwJK8pC0DrKiKah4ou2VFdbgC7Cs7w3gdKEnKuvMEqI+poxwCKA0ZEQyfALzo1toSAOXFuwTLFYB41+ZqzwLw0d1O4NHMn0y0Z3sCgGZqzn7T3ufTWnuPm8ALYQv9GTAuv4YBwnu/NL3+0uyIM35gNOLsj/Uwo/mKnfDCSm9zmm3qw9kt+vTt097gmoyubgC88o08TOv3SmD50WX52Wf54fkvyG+va0SRS+VzUwAAAABJRU5ErkJggg=='
stop64 = 'iVBORw0KGgoAAAANSUhEUgAAAEAAAABABAMAAABYR2ztAAAAHlBMVEUAAAAAgP8hhNgghNggg9khhNcghNgghNgghNj///8bgLFtAAAACHRSTlMAAlVwcY2oqu9aCT4AAAABYktHRAnx2aXsAAAAT0lEQVRIx2NgGAV0BYxu5RggRQBJAXMHFmCApIANm4IEJAXs2BQUoChoVUIDEWgKmtDdrTGqYFTBqIJRBUQWIASKIIKFGMFikGBBOgroAAA3+qM7sLvmjAAAAABJRU5ErkJggg=='
tick64 = 'iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAMAAACdt4HsAAAByFBMVEUAAAAA//8AgP8Aqv8AgL8zmcwkktsggN8cjuMXi9EnidgkgNsiiN0ggN8jgNwggNUfhdYdgNgchNkiiNUhhNYgh9cfg9geh9odg9sjh9UhhdghgtkghdofhdYihNgggtoghNYfhtcfhNcehtgihNkhhtkhhNoghtcgg9cfhdghhdYhg9cghdcgg9gfhdkfg9khg9gghNkfhdcfhNghhdghhNkhhdkghNcghdcgg9gfhdghhdcgg9cgg9gfhNkfg9khhNchg9cghNggg9gghNggg9kghNgghNkfhdgghdkgg9cfhNghg9ggg9gghNgfhNgghNgghdgghdgghNkfhNcfhNghhNgghNgghNkgg9cfhNgfg9ghhNggg9gghNkgg9cghNggg9gfhdgghdkghdgghNgghdgghNgfhNkhhNcghNgghNgghNgghNggg9gghNcgg9gfhNghg9gghNggg9gghdcghNgfhNgghNgghNcghNgghNgghNgfhNgghNgghNgfhNkghNgghNgghNgghNgfhdgghNgghdgghNgghNgghNgghNgghNgfhNgghNgghNgghNgghNgghNgfhNgghNgghNgghNj///+zTMzgAAAAlnRSTlMAAQIDBAUHCAkLDQ4PEBYYGRobHh8gISIjJC4vMDI0Nzg5Ojs8PT4/QEFFRkdISUpUV1pbXF1eX2BhYmZnaWprbG1ub3Bxdnh7f4CDhIiJi4+WmJmam5yeoKGio6Slpqeoqautr7CxsrO0tba+v8DBwsPExcbIycvNztDR0tPZ2tvc3d7f4+Tl5u/w8fLz9PX29/r7/P4SVPWEAAAAAWJLR0SX5m4brwAAA0lJREFUWMPdl9dDE0EQxjcSlKagJAJWVMAIRqoKYgFBAQsqKCJyUgJSVLoiViAoRSAB5Pf3+nApV7K5u1fnaXdmv7nd2ZnvZoX4n+W4v6m9U1E625v8xx2DD9cpa2hkTanLcgC/1L+DSXb6fTbh5XNIZNZvA54/Hl2+OdHZUl9VVd/yfHIzqhu1jEZjWF252Fbojmvd5x4sqfrwnaTwrAAA+yPFLqPJVTK6D8Bgphx/9BsA708kNp+aAOBrjgxfsAKwXu2SLXBd3QAI5ic2H1sB+ORNdsa8eYBgwj0c/g4QOJg8yGnDAF8SxMEVAHiZYnVNKd0AA2bDXYBAinWipAwD3DLlzw7w6ZCdTE2bB0LGUI0B6zaLLn8DGDbkP0CN3WK7DlCmU80AUy67DlwfgDmtxgfsn7Rf76f3gRKNYgB464RwxoE3mhzaAYotUbmz208jw4tAOJ5NdcCiZQQ8K8D5SBSCwLWYSQHabOGjDsRDoCdmWwXO2sK/jk6LgNUYfwObbovzLwMMxFalbgG5kckVYNIZXohpTS41A50O8aILaIyMnwD3HeJFC9AeGXcANx3ixS3gWWTcC1Q7xIsazZ3oHaSX66vaEwRQjFSjdaA7QvoPdiut8boj6IJ4BdirNODfmKlOG8Qm7TV6d7UepHjRBTRExn5dIlXuxT3I8bpE8upTuWIP+Fsjjb85lcUqUChMHpLg9cUkFOCBxqqeolm+fyEeAa9is1pgSUsoFXvRjiLx91VCibN4VtjAkeoe5N8XPiCUEZ/3A6PC7EGGF++AXiOtnzJ5kOLPYGThGWBaT6u+7nsHZD+WCWBWp/KjY1kLqQMo1etGgfU8e/iCDWDI2LuEgXl7v/cFYNtjVDcAjLhtNBgBEjPYIEC3ZYvi7gHoS2DJ/AowZHGKtBGAhYxEtiM/AT4XJMN7PwIsZ0talyDARq280bzxB2BZels5XwCYOi3JvxkAFrLlO8wcUJvtsYvmZtv3Tq2vvoykQbodUpctP7yQquGfokcrqj500+qavCNRKtiaetFaX1Vd39o1vRXVDXtsZNrladmTZ6rUZrGUKGEzOqQUC/uSebXntxb961VNhuO3o6es8XFHb2/H48ay3P/6hf0PrgDmLxzMGhUAAAAASUVORK5CYII='
tick164 ='iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAMAAACdt4HsAAAAQlBMVEUAAAAXi9Egh9cfg9gfhdkfg9kfhNkfhNchg9ghhNghhdgghNkfhNghhdgghNgghdgghNgghNgfhNgghNgghNj////GIpG9AAAAFHRSTlMACyAhSUpRU1RVVldbXNnl+fr7/OKBPssAAAABYktHRBXl2PmjAAAAoElEQVRYw+2WSRKDMAwExRYgJmzR/9+ahaUSwGA0l6Rq5qzugz1yWYRhGAZIkkUQf221RgyuV9UU5NsY4/vSzJcv/l6RJ/+7fJQl+/13B3ytnQN4Sb1DYbzEnWcskPcOBvMixfuob8D9bRhO3v/KcLo/C4Ohf18GU38/DMb+zwbz/owGYP+G6oT3x2MA+Mlg54dzAN6fZy5Nk/MjxTD/lQdsFhRovEUwRAAAAABJRU5ErkJggg=='
axis64 = 'iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAMAAABg3Am1AAABU1BMVEUAAAAA//8Aqv8AgL8rgNUkktscjuMagMwzgMwkktsggN8khtsjgNwfhdYchNkkgNsjjdwng9geh9odg9skitMjh9UjhdYfhdsihNgfhtchhtkfhdgig9ohg9cfhdohhNcghNgfh9whhdghhdkghNcfg9gfhtghg9khhdcgg9cfhdYghNggg9kfhdchhNchhNoghdgfhtkhhNgghNkhgtghhNgfg9gfhNghg9kghNohhNghhNoghdgggtgfhNgfhNgghNchhdgghNghhNgfhdgfhNcgg9cgg9gghNgghNghg9cghNgghNkfhNghhNgfhdchg9gfhNgghNgghNkghNkghNgghNgghNgghdgghNghhdkhg9gghNcghdkhhNghhNgghNgghdgghNgghNkghNghg9kghNgghNgghNcfhNgfhNkghNgghNcghNgghdgghNj///8PhQorAAAAb3RSTlMAAQMEBgcJCgoOEBUWGRscHSEiIyMkLDI0OT1BREZLTU9RVl5fY2NlZmdrcHFzdHR3enx+g4OKi4yPkZGWl5ykpqmqqqusra+4ubm/wcPJzMzN0NDU1tjc4eLi4+bo6evs7O/v8PP29/j7/f3+/v7kcviWAAAAAWJLR0Rw2ABsdAAAAQRJREFUSMdjYKAikNZkYmCQVSZeg3CYJQO/QyBRahktzBkZGEzjBUwTRYjSYJyfb8TAwOYd7GNHlHr57Jy8bDkGBsXoWFZi1Ium5Ofm5icJMzB7OhNlgW6+U36+S74OA7OHI1Ea2BXY8vPZFNiJ1gAE+fkgkinInjQNJABUDUIaXAwMSpLEaxCL02fQipIiwUnuXuKRVqT4gTPBP4CPJE/bZpiQFkohqTYspGgwDNeOUCNBA0eMGYOfKy/xGtxCuRkEk61J8QOPHjdpnjbIj5QgSQO3b366CoyjmplPBMjKz9eAalAnVQPJTqKJp0kOVlpn0VENoxroqCEtjUQNMjIMQwYAAIAPYGJ54gHnAAAAAElFTkSuQmCC'


#with Connection.open_serial_port("/dev/cu.usbmodem1101") as connection:
with Connection.open_serial_port("/dev/tty.usbmodem11301") as connection:
    device_list = connection.detect_devices() 
    xy_device = device_list[0]
    z_device = device_list[1]

    

    axis1 = xy_device.get_axis(1)  # x
    axis2 = xy_device.get_axis(2)  # y
    axis3 = z_device.get_axis(1)   # z
    
    def is_in_bounds_r(axis, step):
        ''' checks if next step is in bounds '''
        if axis == axis1:   max = MAX_X
        if axis == axis2:   max = MAX_Y
        if axis == axis3:   max = MAX_Z
        
        current_pos = axis.get_position(Units.LENGTH_MILLIMETRES)
        if current_pos + step - max >= 0:
            return False
        return True

    def is_in_bounds_l(axis, step):
        ''' checks if next step is in bounds '''
        current_pos = axis.get_position(Units.LENGTH_MILLIMETRES)
        if current_pos - step >= 0:
            return True
        return False

    def move_right(axis, step):

        if axis == axis1:   max, coord = MAX_X, "x"
        if axis == axis2:   max, coord = MAX_Y, "y"
        if axis == axis3:   max, coord = MAX_Z, "z"
        
        if (is_in_bounds_r(axis, step)):
            axis.move_relative(step, Units.LENGTH_MILLIMETRES, wait_until_idle=False)
        else:
            axis.move_absolute(max, Units.LENGTH_MILLIMETRES, wait_until_idle=False)
            sg.popup_no_wait("You are at max {} position".format(coord), title="max", button_color=("White", "Red"))
            

    def move_left(axis, step):

        if axis == axis1:   max, coord = MAX_X, "x"
        if axis == axis2:   max, coord = MAX_Y, "y"
        if axis == axis3:   max, coord = MAX_Z, "z"

        if is_in_bounds_l(axis, step):
            axis.move_relative(-step, Units.LENGTH_MILLIMETRES, wait_until_idle=False)
        else:
            axis.move_absolute(0)
            sg.popup_no_wait("You are at min {} position".format(coord), title="max", button_color=("White", "Red"))
                
    def move_small_end(axis):
        if axis == axis1:   coord = "x"
        if axis == axis2:   coord = "y"
        if axis == axis3:   coord = "z"

        if axis.get_position(Units.LENGTH_MILLIMETRES) != 0:
            axis.move_absolute(0, wait_until_idle=False)
        else:
            sg.popup_no_wait("You are at min {} position".format(coord), title="max", button_color=("White", "Red"))

    def move_big_end(axis):
        if axis == axis1:   max, coord = MAX_X, "x"
        if axis == axis2:   max, coord = MAX_Y, "y"
        if axis == axis3:   max, coord = MAX_Z, "z"

        if axis.get_position(Units.LENGTH_MILLIMETRES) != max:
            axis.move_absolute(max, Units.LENGTH_MILLIMETRES, wait_until_idle=False)
        else:
            sg.popup_no_wait("You are at max {} position".format(coord), title="max", button_color=("White", "Red"))


        axis1.move_absolute(MAX_X, Units.LENGTH_MILLIMETRES, wait_until_idle=False)
    
    def move_to_abs(x, y, z):
        ''' Moves to specified absolute positon. If an input is invalid, it will be ignored and other valid movements will occur '''
        if x != "":
            try:
                if float(x) < 0 or float(x) > MAX_X:
                    sg.popup_no_wait("Please enter a valid X postion.\n X: (0 to 151.49) mm", title="X error", button_color=("White", "Red"))
                else:
                    axis1.move_absolute(float(values["-INX-"]), Units.LENGTH_MILLIMETRES, wait_until_idle=False)

            except:
                sg.popup_no_wait("Please enter a valid X postion.\n X: (0 to 151.49) mm", title="X error", button_color=("White", "Red"))

        if y != "":
            try:
                if float(y) < 0 or float(y) > MAX_Y:
                    sg.popup_no_wait("Please enter a valid Y postion.\n Y: (0 to 151.49) mm", title = "Y error", button_color = ("White", "Red"))
                else: 
                    axis2.move_absolute(float(values["-INY-"]), Units.LENGTH_MILLIMETRES, wait_until_idle=False)

            except:
                sg.popup_no_wait("Please enter a valid Y postion.\n Y: (0 to 151.49) mm", title = "Y error", button_color = ("White", "Red"))
                

        if z != "":
            try:
                if float(z) < 0 or float(z) > MAX_Z:
                    sg.popup_no_wait("Please enter a valid Z postion.\n Z: (0 to 40.00) mm", title = "Z error", button_color = ("White", "Red"))
                else: 
                    axis3.move_absolute(float(values["-INZ-"]), Units.LENGTH_MILLIMETRES, wait_until_idle=False)

            except:
                sg.popup_no_wait("Please enter a valid Z postion.\n Z: (0 to 40.00) mm", title = "Z error", button_color = ("White", "Red"))

    def move_rel(x,y,z):
        if x != "":
            try:
                if float(x) < 0:
                    move_left(axis1, abs(float(x)))
                else:
                    move_right(axis1, float(x))

            except:
                sg.popup_no_wait("Please enter a valid X postion.\n X: (0 to 151.49) mm", title="X error", button_color=("White", "Red"))

        if y != "":
            try:
                if float(y) < 0:
                    move_left(axis2, abs(float(y)))
                else:
                    move_right(axis2, float(y))

            except:
                sg.popup_no_wait("Please enter a valid Y postion.\n X: (0 to 151.49) mm", title="Y error", button_color=("White", "Red"))
 

        if z != "":
            try:
                if float(z) < 0:
                    move_left(axis3, abs(float(z)))
                else:
                    move_right(axis3, float(z))

            except:
                sg.popup_no_wait("Please enter a valid Z postion.\n Z: (0 to 40.00) mm", title = "Z error", button_color = ("White", "Red"))


    def set_step(step):
        try:
            if float(step) >= 0:
                global DIST 
                DIST = float(step)
                window["-mm-"].update("{} mm".format(DIST))
            else:
                sg.popup("Please enter a valid step size.", title="Step size error", button_color=("White", "Red"))
        except:
            sg.popup("Please enter a valid step size.", title="Step size error", button_color=("White", "Red"))

    def centre():
        axis1.move_absolute(MAX_X/2, Units.LENGTH_MILLIMETRES, wait_until_idle=False)
        axis2.move_absolute(MAX_Y/2, Units.LENGTH_MILLIMETRES, wait_until_idle=False)
        axis3.move_absolute(MAX_Z/2, Units.LENGTH_MILLIMETRES, wait_until_idle=False)



    def load_csv(csv_path):
        df = pd.read_csv(csv_path)
        t = df["t"]
        x = df["x"]
        y = df["y"]
        z = df["z"]

        return t,x,y,z

    def plotter(x,y,z):
        fig = plt.figure()
        plt.subplots_adjust(bottom=0.25) 
        
        ax = fig.add_subplot(111, projection='3d') 
        ax.set_xlabel('x position')
        ax.set_ylabel('y position')
        ax.set_zlabel('z position')

        l=ax.plot(x[0],y[0],z[0], "bo")
        ax.plot(x,y,z, alpha=0.2)

        return plt, fig, ax


    def create_slider(plt,fig,ax):

        # Make a horizontal slider to control the time.
        axtime = plt.axes([0.15, 0.1, 0.65, 0.03])
        freq_slider = Slider(
            ax=axtime,
            label='Time',
            valmin=0,
            valmax=2500,
            valinit=0,
            valstep=1
        )

        return freq_slider

    def display(filename):
        t,x,y,z = load_csv(filename)

        plt, fig, ax = plotter(x,y,z)
        freq_slider = create_slider(plt,fig,ax)

        def update(val): 
            h = freq_slider.val 
            ax.clear()
            l=ax.plot(x[h],y[h],z[h], "bo")
            ax.plot(x,y,z, alpha=0.2)
            ax.set_xlabel('x position')
            ax.set_ylabel('y position')
            ax.set_zlabel('z position')
            
            fig.canvas.draw_idle()
            
        freq_slider.on_changed(update)

        plt.show()









    col2 = [
        [sg.Button('', image_data=Uparrow64,button_color=('white', 'white'), pad=(0,0), key='-ZREND-')],
        [sg.Button('', image_data=uparrow64,button_color=('white', 'white'), pad=(0,0), key='-ZRIGHT-')],
        [sg.Text('Z', font = 'Any 16')],
        [sg.Button('', image_data=downarrow64,button_color=('white', 'white'), pad=(0,0), key='-ZLEFT-')],
        [sg.Button('', image_data=Downarrow64,button_color=('white', 'white'), pad=(0,0), key='-ZLEND-')],
    ]

    col_buffer = [
        [sg.Text('', size=(10,20))],
    ]

    col1 = [
        #[sg.Text('Column1', background_color='red', size=(20,20))],
        [
            sg.Button('', image_data=Up64,button_color=('white', 'white'), pad=(0,0), key='-YREND-'),
        ],
        [
            sg.Button('', image_data=up64,button_color=('white', 'white'), pad=(0,0), key='-YRIGHT-'),
        ],
        [
            #sg.Button("End", key="-XLEND-"), 
            sg.Button('', image_data=Left64,button_color=('white', 'white'), pad=(0,0), key='-XLEND-'),
            #sg.Button(" Left ", key="-XLEFT-"), 
            sg.Button('', image_data=left64,button_color=('white', 'white'), pad=(0,0), key='-XLEFT-'),
            #sg.Text("            ", font='Any 16'),
            sg.Button('', image_data=axis64, button_color=('white', 'white'), pad=(0,0), size=(1,1)),
            #sg.Button("Right", key="-XRIGHT-"),
            sg.Button('', image_data=right64,button_color=('white', 'white'), pad=(0,0), key='-XRIGHT-'), 
            #sg.Button("End", key="-XREND-"),
            sg.Button('', image_data=Right64,button_color=('white', 'white'), pad=(0,0), key='-XREND-'), 
            #sg.Column(col_layout)
        ],
        [
            
            #sg.Button("Right", key="-YRIGHT-"),
            sg.Button('', image_data=down64,button_color=('white', 'white'), pad=(0,0), key='-YLEFT-'),
            #sg.Button("End", key="-YREND-"),  
        ],
        [
            sg.Button('', image_data=Down64,button_color=('white', 'white'), pad=(0,0), key='-YLEND-'), 
        ],
    ]
        
        
        
    layout = [
        [
            #sg.Button("STOP pls", key="-STOP-", )
            sg.Button('', image_data=stop64,button_color=('white', 'white'), pad=(0,0), key='-STOP-'),
            sg.Button('', image_data=home64,button_color=('white', 'white'), pad=(0,0), key='-HOME-'),
            sg.Button('', image_data=centre64,button_color=('white', 'white'), pad=(0,0), key='-CENTRE-'),
        ],

        [sg.HorizontalSeparator(color='#2084d8')],

        [
            sg.Text("X position:", font = 'Any 16'),
            sg.Text("{:.2f} mm".format(axis1.get_position(Units.LENGTH_MILLIMETRES)),key="-CURRENTX-", font = 'Any 16')
        ], 
        [
            sg.Text("Y position:", font = 'Any 16'),
            sg.Text("{:.2f} mm".format(axis2.get_position(Units.LENGTH_MILLIMETRES)),key="-CURRENTY-", font = 'Any 16')
        ],
        [
            sg.Text("Z position:", font = 'Any 16'),
            sg.Text("{:.2f} mm".format(axis3.get_position(Units.LENGTH_MILLIMETRES)),key="-CURRENTZ-", font = 'Any 16')
        ],
        [   
            sg.Text("Set step size:", font='Any 16'),
            sg.InputText(key="-STEP-", size=(5,1)),
            sg.Text("{} mm".format(DIST), key="-mm-", font='Any 16'), 
            sg.Button("OK", key="-OK-", bind_return_key=True),
            #sg.Button('', image_data=tick164,button_color=('white', 'white'), pad=(0,0), key='-OK-'),
        ],
        [sg.Column(col1, element_justification='c' ), sg.Column(col_buffer), sg.Column(col2, element_justification='c' )],
        [
            sg.Text("Relative movements (x,y,z):", font = 'Any 16'), 
            sg.InputText(key='-INXRel-', size=(3,1)), 
            sg.InputText(key='-INYRel-', size=(3,1)), 
            sg.InputText(key='-INZRel-', size=(3,1)),
            sg.Button("OK", key="-OK2-", bind_return_key=True)
        ],
        [
            sg.Text("Move to absolute position (x,y,z):", font = 'Any 16'), 
            sg.InputText(key='-INX-', size=(3,1)), 
            sg.InputText(key='-INY-', size=(3,1)), 
            sg.InputText(key='-INZ-', size=(3,1)),
            sg.Button("OK", key="-OK1-", bind_return_key=True)
        ],
    ]

    plot=[
        [
            sg.Text('Select csv file', font = 'Any 16',),
            sg.Input(), 
            sg.FileBrowse('FileBrowse', file_types=(("CSV files", "*.csv"),)), 
            sg.Button("Display", key="-FILE-")
        ],
    ]

    tabgrp = [
    [sg.TabGroup([[sg.Tab('Movement', layout, element_justification= 'center'),
                    sg.Tab('Modelling', plot,),
                    ]], tab_location='centertop',
                        border_width=1)]
        ]  

    window = sg.Window('Zaber GUI', tabgrp, size = (750,750), element_justification='c')

    while True:
        event, values = window.read()
        
        if event == "Exit" or event == sg.WIN_CLOSED:
            break

        if event == "-XLEND-":
            move_small_end(axis1)

        if event == "-XRIGHT-":
            move_right(axis1, DIST)

        if event == "-XLEFT-":
            move_left(axis1, DIST)

        if event == "-XREND-":
            move_big_end(axis1)

        #####################

        if event == "-YLEND-":
            move_small_end(axis2)
            
        if event == "-YRIGHT-":
            move_right(axis2, DIST)

        if event == "-YLEFT-":
            move_left(axis2, DIST)

        if event == "-YREND-":
            move_big_end(axis2)

        #####################
        
        if event == "-ZLEND-":
            move_small_end(axis3)

        if event == "-ZRIGHT-":
            move_right(axis3, DIST)

        if event == "-ZLEFT-":
            move_left(axis3, DIST)

        if event == "-ZREND-":
            move_big_end(axis3)


        ####################
        
        if event == "-HOME-":
            connection.home_all(wait_until_idle=False)
        
        if event == "-CENTRE-":
            centre()

        if event == "-OK-":
            set_step(values['-STEP-'])
            window["-STEP-"].update("")

        if event == "-OK1-":
            move_to_abs(values['-INX-'], values['-INY-'], values['-INZ-'])
            window["-INX-"].update("")
            window["-INY-"].update("")
            window["-INZ-"].update("")

        if event == "-STOP-":
            connection.stop_all()

        if event == "-OK2-":
            move_rel(values["-INXRel-"], values["-INYRel-"], values["-INZRel-"])
            #window["-INXRel-"].update("")
            #window["-INYRel-"].update("")
            #window["-INZRel-"].update("")
        
        if event == "-FILE-":
            pathname = values['FileBrowse']
            if pathname.lower().endswith((".csv")):
                display(pathname)
            else:
                sg.popup_no_wait("Only CSV file types are supported.", title="max", button_color=("White", "Red"))

                


        #axis1.wait_until_idle()
        #axis2.wait_until_idle()
        #axis3.wait_until_idle()
            
        # note : these only update directly after action when axis is set to idle. However, when set to idle, stop button will not work
   
        window["-CURRENTX-"].update("{:.2f} mm".format(axis1.get_position(Units.LENGTH_MILLIMETRES)))
        window["-CURRENTY-"].update("{:.2f} mm".format(axis2.get_position(Units.LENGTH_MILLIMETRES)))
        window["-CURRENTZ-"].update("{:.2f} mm".format(axis3.get_position(Units.LENGTH_MILLIMETRES)))