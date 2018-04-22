#coding:utf-8
"""
@brief: 模拟退火算法
"""
import random
import copy
import math

from Flavor import Flavor  

def put_flavors_to_servers(vpc_r,cpu_n,cpu_m,opt):
    T=100.0
    Tmin=1.0
    r=0.999
    vpc_p=[]
    for i in range(len(vpc_r)):
        for j in range(int(vpc_r[i].num) ):
            vpc_p.append([i,vpc_r[i].core,vpc_r[i].mem])
    #print vpc_p
    min_cpu=len(vpc_p)+1
    dice=[]
    for i in range(len(vpc_p)):
        dice.append(i)
    while T > Tmin:
        random.shuffle(dice)
        vpc_np=copy.deepcopy(vpc_p)
        mswap(vpc_np,dice[0],dice[1])
        cpu_fp=[]
        vpc_num_init=[0 for i in range(len(vpc_r))]
        cpu_fp.append(vpc_num_init+[cpu_n]+[cpu_m])
        
        for i in range(len(vpc_np)):
            for j in range(len(cpu_fp)):
                if cpu_fp[j][-1]>=vpc_np[i][2] and cpu_fp[j][-2]>=vpc_np[i][1]:
                    cpu_fp[j][vpc_np[i][0]]+=1
                    cpu_fp[j][-1]-=vpc_np[i][2]
                    cpu_fp[j][-2]-=vpc_np[i][1]
                    break
                if j==len(cpu_fp)-1:
                    cpu_fp.append(vpc_num_init+[cpu_n]+[cpu_m])
                    cpu_fp[j+1][vpc_np[i][0]]+=1
                    cpu_fp[j+1][-1]-=vpc_np[i][2]
                    cpu_fp[j+1][-2]-=vpc_np[i][1]
                
        #print cpu_fp
        cpu_total=len(cpu_fp)
        if opt == 'CPU':
            sc=cpu_total-1+(cpu_n-cpu_fp[-1][-2])/float(cpu_n)
        else:
            sc=cpu_total-1+(cpu_m-cpu_fp[-1][-1])/float(cpu_m)
        
        #print sc
        if sc<min_cpu:
            vpc_p=copy.deepcopy(vpc_np)
            min_cpu=sc
            cpu_fp_res=cpu_fp            
        else:
            #print math.exp((min_cpu - sc) / float(T))
            if math.exp((min_cpu - sc) / float(T))  > random.random():
                vpc_p=copy.deepcopy(vpc_np)
                min_cpu=sc
                cpu_fp_res=cpu_fp
        
        T*=r
        #print T
        
    return cpu_fp_res
        
        
def mswap(list, a, b):
    temp=copy.deepcopy(list[a])
    list[a]=copy.deepcopy(list[b])
    list[b]=copy.deepcopy(temp)
    
    
def main():
    vl = []
    temp = Flavor(2, 1, 1)
    temp1 = Flavor(3, 1, 2)
    temp2 = Flavor(3, 2, 2)
    temp3 = Flavor(10, 8, 8)
    vl.append(temp)
    vl.append(temp1)
    vl.append(temp2)
    vl.append(temp3)
    result = put_flavors_to_servers(vl, 56, 128, 'CPU')
    print result
        
      
if __name__ == "__main__":
    main()