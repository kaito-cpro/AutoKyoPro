# AutoKyoPro
automatically compile code, test on sample cases, and submit to AtCoder

This script is quoting online-judge-tools by https://github.com/kmyk  
I arranged online-judge-tools in order to play KyoPro confortably 'only' for myself

# How to use
1. Install the files into a directory  
   (Let this directory's name 'ABC' for example)  
2. Make a path to 'path/to/onlinejudge/cmd'

! in the following, run commands in the directory 'ABC' !

3. Login to AtCoder by `$ akp login`  
4. Initialize by `$ akp init`  
   Register the contest name etc.  
　　eg.- contest name: ABC123  
　　　 -alternate contest url: (just press Enter key)  
 　　　-number of problems: (just press Enter key)  
   If the contest serves problems A to H, number of problems: H  
5. Write a source code  
   If you solve problem A, write on A/a.cpp or A/a.py  
6. Submit by `$ akp a.cpp` or `$ akp a.py`  
   If you run the command above, AutoKyoPro automatically test the sample cases and submit  
   If AC: automatically submit code  
   If WA: automatically stop the process  

# Other usages
- If you run `$ akp standby`, AutoKyoPro automatically open the contest page(problem A) at the time when the contest starts  
- If you run `$ akp a.cpp nosub`, AutoKyoPro stops the process just before submission  
- If you run `$ akp a.cpp sub`, AutoKyoPro forcibly submit the code without testing AC/WA  
- If you run `$ akp info`, AutoKyoPro shows the internal information (this command is used for debug)  
- If you copy&paste C++DebugMacro(https://github.com/kaito-cpro/DebugMacro/blob/master/debug_structural_amended.cpp) in the source code, AutoKyoPro automatically remove the DebugMacro and Debug::functions before submission  
