

import time;

h = int( time.strftime('%H') )
m = int( time.strftime('%M') )
s = int( time.strftime('%S') )
if(h >=0  and h < 12) :
    print("\nGOOD MORNING.... Sir!! \n") 
    print("It is ", h,':',m,':',s, ' AM','\n') 
elif(h >= 12 and h < 17) :
    print("\nGOOD AFTERNOON.... Sir!! \n")
    print("It is ", h,':',m,':',s, ' PM','\n') 
elif(h >= 17 and h < 20) :
    print("\nGOOD EVENING.... Sir!! \n")
    print("It is ", h,':',m,':',s, ' PM','\n') 
else: 
    print("\nGOOD NIGHT !! ... Sir \n")
    print("It is ", h,':',m,':',s, ' PM','\n') 