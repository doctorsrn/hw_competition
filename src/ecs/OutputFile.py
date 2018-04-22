# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 20:27:04 2018

@author: DoctorSRn
@brief: output file class
"""
import copy
import sa
from Flavor import Flavor 

flavor_dict = {'1': {'core': 1, 'mem': 1},
               '2': {'core': 1, 'mem': 2},
               '3': {'core': 1, 'mem': 4},
               '4': {'core': 2, 'mem': 2},
               '5': {'core': 2, 'mem': 4},
               '6': {'core': 2, 'mem': 8},
               '7': {'core': 4, 'mem': 4},
               '8': {'core': 4, 'mem': 8},
               '9': {'core': 4, 'mem': 16},
               '10': {'core': 8, 'mem': 8},
               '11': {'core': 8, 'mem': 16},
               '12': {'core': 8, 'mem': 32},
               '13': {'core': 16, 'mem': 16},
               '14': {'core': 16, 'mem': 32},
               '15': {'core': 16, 'mem': 64},
               }

class OutputFile(object):
    def __init__(self,
                 vm_sum_,  # num
                 vm_type2num_): # dict
        self.vm_sum = vm_sum_
        self.vm_type2num = vm_type2num_
        self.ps_sum = 0
        
        #dict, (key:ps_id, value:{key:vm_type, value:vm_num})
        self.ps_id2distribution = {} 
    
    def data_pre(self):
        vm_keys = (self.vm_type2num).keys()
        vm_keys.sort()
        result = []
        for k in vm_keys:
            temp = Flavor(self.vm_type2num[k], 
                         (flavor_dict[k])['core'],
                         (flavor_dict[k])['mem'])
            result.append(temp)
        
        return result
    
    """
    @brief: 分配函数
    """
    def distribute(self, input_file):
        
        vm_pre = self.data_pre()
        
        if input_file.opti_type == 0:
            opt = 'CPU'
        else:
            opt = 'MEM'
            
        # 预测的结果
        result = sa.put_flavors_to_servers(vm_pre, 
                                        input_file.cpu, 
                                        input_file.mem,
                                        opt)
        print result
        self.ps_sum = len(result)
        
        vm_keys = (self.vm_type2num).keys()
        vm_keys.sort()
        distribution_dic = {}
        
        for i in range(len(result)):
            for k,j in zip(vm_keys, range(len(vm_keys))):
                distribution_dic[k] = result[i][j]
            print 'distribution dic' 
            print distribution_dic
            (self.ps_id2distribution)[str(i+1)] = copy.deepcopy(distribution_dic)
            distribution_dic.clear()
        
        print self.ps_id2distribution
        print 'ttt'
#        self.ps_id2distribution = {'1':{'1':1,'2':1}, '2':{'3':1}}
    
    
    """
    @brief:格式化输出
    """
    def outputfile_format(self):
        result = []
        result.append(str(self.vm_sum))
        
        vm_type = self.vm_type2num.keys()
        vm_type.sort()
        print vm_type
        for type_ in vm_type:
            result.append(("flavor"+type_+' '+str(self.vm_type2num[type_])))
        
#        result.append('\n')
        
        result.append('\n'+str(self.ps_sum))
        
        ps_id = (self.ps_id2distribution).keys()
        ps_id.sort()
        vm_str = []
        for id_ in ps_id:
            vm_type = (self.ps_id2distribution[id_]).keys()
            vm_type.sort()
            for vt in vm_type:
                vm_str.append("flavor"+vt)
                vm_str.append(str((self.ps_id2distribution[id_])[vt]))
            
            temp_str = ''
            temp_str = id_
            for temp in vm_str:
                temp_str += ' '
                temp_str += temp
            
            result.append(temp_str)
            
            temp_str = ''
            vm_str = []
        
        print result
        return result
    
    def show_output_data(self):
        print "vm_sum:%d"%self.vm_sum
        print "vm_type2num: ", self.vm_type2num
        print "ps_sum:%d"%self.ps_sum
        print "ps_dis",self.ps_id2distribution
 
 

    
def write_result(array, outpuFilePath):
    with open(outpuFilePath, 'w') as output_file:
        for item in array:
            output_file.write("%s\n" % item)
            

def main():
    output = OutputFile(2, {'1':1, '2':1})
    output.distribute(1)
    
    output.show_output_data()
    result = output.outputfile_format()
    write_result(result, './data/output_test.txt')
      
if __name__ == "__main__":
    main()
    
    