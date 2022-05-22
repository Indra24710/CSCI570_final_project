from numpy import char
import time
import psutil
import sys

delta=30
alpha = [[0,110,48,94],
         [110,0,118,48],
         [48,118,0,110],
         [94,48,110,0]]
char_to_index = {'A':0,'C':1,'G':2,'T':3}



    
def align(str1,str2):
    if str2=="":
        return [[str1,"_"*len(str1)],len(str1)*delta]
    elif len(str2)==1:
        comb_val=combine(str1,str2)
        return [comb_val[0],comb_val[1]]
    elif len(str1)==1:
        comb_val=combine(str2,str1)
        return [comb_val[0][::-1],comb_val[1]]


    prefix=space_eff(str1[:(len(str1)//2)],str2)
    suffix=space_eff(str1[-1:(len(str1)//2)-1:-1],str2[::-1])
    mincost=100000
    best=0
    curr=0
    for i in range(len(prefix)):
        curr=prefix[i]+suffix[::-1][i]
        if curr<mincost:
            mincost=curr
            best=i

    comb_val1=align(str1[:len(str1)//2],str2[:best])
    comb_val2=align(str1[(len(str1)//2):],str2[best:])
    return [[comb_val1[0][0]+comb_val2[0][0],comb_val1[0][1]+comb_val2[0][1]],comb_val1[1]+comb_val2[1]]

def combine(str1,str2):
    index=-1
    min_val=0
    fin_val=0
    for i in range(len(str1)):
        if str2==str1[i]:
            index=i
    if index==-1:
        min_val=1000000
        for i in range(len(str1)):
            val= alpha[char_to_index[str1[i]]][char_to_index[str2]]
            fin_val+=val
            if val<min_val:
                min_val=val
                index=i
    return [[str1,"_"*index+str2+("_"*(len(str1)-index))],(len(str1)-1)*delta+min_val]

        

def space_eff(str1,str2):
    row=1
    dptable=[[i*delta for i in range(len(str2)+1)],[30]]
    while row<=len(str1):
        for i in range(1,len(str2)+1):
            dptable[1].append(min(dptable[0][i-1]+alpha[char_to_index[str1[row-1]]][char_to_index[str2[i-1]]],dptable[1][i-1]+delta,dptable[0][i]+delta))
            
        row+=1
        if row>len(str1):
            # print(dptable[1])
            return dptable[1]
        dptable=[dptable[1]]
        dptable.append([dptable[0][0]+30])
        
            
def makeStrings(stringInfo):
        for i in stringInfo:
            if "A" in i:
                string = i
            else:
                string = string[:int(i)+1] + string + string[int(i)+1:]
        return string
def process_memory():
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_consumed =  int(memory_info.rss/1024)
    return memory_consumed
if  __name__ =="__main__":
    infile = open(sys.argv[1], "r")
    outfile = open(sys.argv[2], "w")
    lines = infile.read().splitlines()
    for i in range(1, len(lines)):
        if "A" in lines[i]:
            stringInfo1 = lines[:i]
            stringInfo2 = lines[i:]
    
    start_time = time.time()
    
    str1=makeStrings(stringInfo1)
    str2=makeStrings(stringInfo2)
    # print(str1,str2)

    output=align(str1,str2)
    cost = output[1]
    str1, str2 = output[0][0],output[0][1]
    # print(str1,str2)
    memory= process_memory()
    end_time = time.time()
        

    time_taken = (end_time - start_time) * 1000
    print(cost)
    print(time_taken)
    print(memory)
    L = [str(cost),"\n",str1,"\n",str2,"\n",str(time_taken),"\n",str(memory)]
    outfile.writelines(L) 
    
    
    infile.close()
    outfile.close()