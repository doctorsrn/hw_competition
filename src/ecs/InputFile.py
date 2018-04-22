# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 09:47:04 2018

@author: DoctorSRn
@brief: input file parser
"""
import re
import os 

class InputFile(object):
    def __init__(self, 
                 cpu_ = 0, 
                 mem_ = 0,
                 harddriver_ = 0,
                 vm_num_ = 0,
                 vm_type_ = [],
                 opti_type_ = 0, #0:cpu, 1:mem
                 start_date_ = '', #%Y-%m-%d
                 end_date_ = ''):
        self.cpu = cpu_
        self.mem = mem_
        self.harddriver = harddriver_
        self.vm_num = vm_num_
        self.vm_type = vm_type_
        self.opti_type = opti_type_
        self.start_date = start_date_
        self.end_date = end_date_
        
    def file_parser(self, input_file_array):
        if input_file_array is None:
            print "Input file is None"
            return -1
        #解析物理服务器参数
        r1 = input_file_array[0]
        pattern = re.compile(r'\d+')
        r1_p = re.findall(pattern, r1)
        self.cpu = int(r1_p[0])
        self.mem = int(r1_p[1])
        self.harddriver = int(r1_p[2])
        
        #解析要预测的虚拟数量和规格
        self.vm_num = int(input_file_array[2])
        vm_ls = []
        for vm_ in input_file_array[3:(3+self.vm_num)]:
            pattern = re.compile(r'(?<=flavor)\d+\b')
            temp_str = re.findall(pattern, vm_)
#            print temp_str[0]
            vm_ls.append(temp_str[0])
        self.vm_type = vm_ls
        
        #解析优化的类型：CPU or MEM
        pattern = re.compile(r'CPU')
        temp_str = re.findall(pattern, input_file_array[4+self.vm_num])
        if len(temp_str) == 1:
            self.opti_type = 0
        else:
            self.opti_type = 1
#        print self.opti_type
        
        #解析预测起始时间
        pattern = re.compile('(\d{4}-\d{1,2}-\d{1,2})')
        start_ = input_file_array[6+self.vm_num]
        end_ = input_file_array[7+self.vm_num]
        self.start_date = re.findall(pattern, start_)[0]
        self.end_date = re.findall(pattern, end_)[0]
#        print self.start_date, self.end_date
        
    def show_input_data(self):
        print "cpu:%d"%self.cpu
        print "mem:%d"%self.mem
        print "harddriver:%d"%self.harddriver
        print "vm_num:%d"%self.vm_num
        print "vm_type:",self.vm_type
        print "opti_type:", self.opti_type
        print "start_date:", self.start_date
        print "end_date:", self.end_date
    

 

def read_lines(file_path):
    if os.path.exists(file_path):
        array = []
        with open(file_path, 'r') as lines:
            for line in lines:
                array.append(line)
        return array
    else:
        print 'file not exist: ' + file_path
        return None

def main():
    inputFilePath = './data/input_5flavors_cpu_7days.txt'
    input_file_array = read_lines(inputFilePath)
    input_file = InputFile()
    input_file.file_parser(input_file_array)
    input_file.show_input_data()
    
if __name__ == "__main__":
    main()