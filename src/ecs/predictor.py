# coding=utf-8
#std lib
from datetime import datetime
import re
import math

#visual lib
from matplotlib import pyplot
from matplotlib.dates import AutoDateLocator, DateFormatter,datestr2num

#algorithm lib
##least square
from LeastSquare import LeastSquare
from InputFile import InputFile
from OutputFile import OutputFile


def predict_vm(ecs_lines, input_lines):
    # Do your work from here#
    now = datetime.now()
    
    result = []
    if ecs_lines is None:
        print 'ecs information is none'
        return result
    if input_lines is None:
        print 'input file information is none'
        return result
    
    # new code
    
    # 解析训练数据
    train_data = train_data_parser(ecs_lines)
    
    #训练数据可视化函数
#    data_visualize(train_data)
    
    #数据预处理
    data_preprocess(train_data)
    
    #解析input file
    input_file = InputFile()
    input_file.file_parser(input_lines)

    #预测
    t = predict_func(train_data,
                 input_file.vm_type,
                 input_file.start_date,
                 input_file.end_date,
                 order=2)
    print t
    print 'predict end'
    
    vm_sum =  sum(t.values())
    print 'distribution starting'
    output = OutputFile(vm_sum, t)
    output.distribute(input_file)
    result = output.outputfile_format()
    
    
    #打印程序运行消耗的时间
    print datetime.now()-now
    return result


"""
@brief: 从训练数据中解析出有用的数据，并存储至字典中
@oridata: 原始数据是直接从文件中读取的str list数据
@return: train_data:字典结构{key: vm_type, value: {key: date, value:numbers}
"""
def train_data_parser(origindata):
    train_data = {}
    for temp_data in origindata:
        
        #解析数据
#        pattern = re.compile(r'/flavor\d+') #匹配flavorn"
        pattern = re.compile(r'(?<=flavor)\d+\b') # 匹配flavor后的数字
        vm_type = (pattern.findall(temp_data))[0]

    
        pattern = re.compile(r"(\d{4}-\d{1,2}-\d{1,2})")
        vm_date = (pattern.findall(temp_data)[0])
    
#        print vm_type
#        print vm_date
        # 只存储flavor1~flavor15的虚拟机
        if (int(vm_type) < 16):
            if train_data.has_key(vm_type):
                if train_data[vm_type].has_key(vm_date):
                    (train_data[vm_type])[vm_date] += 1
                else:
                    (train_data[vm_type])[vm_date] = 1
            else:
                train_data[vm_type] = {vm_date: 1}
    
    return train_data


#将时间格式数据转化为时间差（天为单位）数据
# para: list_: sorted str list of date
def date2num(list_):
    result = []
    if list_ is None:
        return result
    if len(list_) == 1:
        result.append(0)
        return result
    else:
        start_date = datetime.strptime(list_[0], "%Y-%m-%d")
        for date_str in list_:
            date_ = datetime.strptime(date_str, "%Y-%m-%d")
            result.append((date_ - start_date).days)
    return result


"""
@brief: 使用3σ准则对数据进行预处理，剔除坏点

"""
def data_preprocess(dict_):
    if dict_ is None:
        return -1
    
    for key_ in dict_.keys():
        data_value = dict_[key_].values()
        data_len = len(data_value)
        data_min = min(data_value)
        data_max = max(data_value)
        data_mean = sum(data_value)/data_len
        data_std_err = math.sqrt(sum([(x-data_mean)*(x-data_mean) for x in data_value])/data_len)
        
        print "data_mean:",data_mean
        print "data_std_err:",data_std_err
        
        for date_key in dict_[key_].keys():
            temp = (dict_[key_])[date_key]
            if (temp-data_mean) > 3*data_std_err:
                (dict_[key_])[date_key] = data_mean+3*data_std_err
            elif (temp-data_mean) < 3*data_std_err:
                (dict_[key_])[date_key] = data_mean-3*data_std_err
            
            if (dict_[key_])[date_key] < 0:
                (dict_[key_])[date_key] = 0
        
    print 'data preprocess is done'

"""
@brief: 最小二乘法预测模型函数
@train_data: 训练数据
@vm_type_: list,要预测的虚拟机类型
@prdict_start_date,predict__end_time:str，预测的起始时间
@order:模型阶次，默认为5阶
@return: result: dict,结构{key:vm_type, value:sum_of_num}
"""
def predict_func(train_data_,
                 vm_type_,
                 predict_start_date,
                 predict_end_date,
                 order=5):
    if train_data_ is None or vm_type_ is None:
        print "Input data error"
        return -1
    
    x_date = [] #"%Y-%m-%d"格式时间数据
    y_num = []  #int list
    x_num = []  #将x_date转化为与起始时间的差值数据
    
    x_pre = [] #要预测的时间点
    y_pre = [] #预测的值
    
    result = {} #用于返回的预测结果
    
    
    for target in vm_type_:
        x_date = train_data_[target].keys()  #获取当期vm的时间列表数据
        x_date.sort()
        
        #获取排序后对应的num
        for key in x_date:
            y_num.append((train_data_[target])[key])
            
        x_num = date2num(x_date)

        pre_st = (date2num([x_date[0], predict_start_date]))[1]
        peroid_num = (date2num([predict_start_date, predict_end_date]))[1]
        
        x_pre = [x+pre_st for x in range(peroid_num+1)]
        #最小二乘法模型
        lq = LeastSquare(x_num, y_num, defaultOrder=order)

        #得到预测结果
        y_pre = lq.predict(x_pre)
        
        print x_num, y_num
        print x_pre, y_pre
        
        #可视化原始数据和预测结果，可注释
        draw_predict(x_num, y_num, x_pre, y_pre,type_=target)
        
        y_sum = int(math.ceil(sum(y_pre)))
        if y_sum < 0:
            y_sum = 0
        result[target] = y_sum
        
        x_date = []
        x_num = []
        y_num = []
        x_pre = []
        y_pre = []
    
    return result
        

"""
@brief: 绘制拟合情况

"""
def draw_predict(x_, y_, x1_, y1_, type_='',title='Data Visualization'):
    
    pyplot.subplot(2, 1, 1)
    pyplot.plot(x_, y_, 'yo-', x1_, y1_, 'r.-')
    pyplot.title(title)  
    pyplot.ylabel('Numbers')  
    pyplot.xlabel('Date')
    pyplot.legend(type_)
  
#    pyplot.subplot(2, 1, 2)
#    pyplot.plot(x1_,y1_,'r.-')
#    pyplot.xlabel('time (s)')  
#    pyplot.ylabel('Undamped')  
  
    pyplot.show()  
    

"""
@brief: 将原始的训练数据进行可视化
@tips：可手动修改程序target2plot设置要绘制出来的vm类型
"""
def data_visualize(train_data={}):
    x_date = []
    y_num = []
    
    if len(train_data) == 0:
        return -1
    #要绘制的Vm类型
    #target2plot = train_data.keys()时将在一张图绘制所有vm数据
    #可赋值['num']绘制对应的vm数据
    target2plot = train_data.keys() #['4'] #['5','6','7','8','9']
    
    #绘图属性设置
    figure = pyplot.figure()
    autodates = AutoDateLocator()
    yearsFmt = DateFormatter('%Y-%m-%d')  
    ax = figure.add_subplot(212)
    ax.xaxis.set_major_locator(autodates)    #设置时间间隔  
    ax.xaxis.set_major_formatter(yearsFmt)    #设置时间显示格式 
    ax.set_xlabel('Time')
    ax.set_ylabel('Numbers')
    ax.set_title('Data Visualizaiton')
#    figure.axes.
    for target in target2plot:
#        for key in train_data[target]:
##            x_date.append(datetime.strptime(key, "%Y-%m-%d")) # datetime类型list
#             x_date.append(key)  #str类型list
        x_date = train_data[target].keys()
        #对时间数据进行排序处理，便于绘图
        x_date.sort()
        print date2num(x_date)
        for key in x_date:
            y_num.append((train_data[target])[key])

        print y_num
        ax.plot_date(datestr2num(x_date), y_num, '-',label="flavor"+target)
        ax.legend()
        figure.autofmt_xdate()
        
#        x_num = date2num(x_date)
#        if len(x_num) < 2:
#            print "train data not enough"
#        else:
#            lq = LeastSquare(x_num, y_num, defaultOrder=4)
#            y_pre = lq.predict(x_num)
#        
#        
##        print x_num, y_num, y_pre
#        bx = figure.add_subplot(212)
#        bx.scatter(x_num, y_num)
#        bx.plot(x_num, y_pre)
#        
#        x_test = arange(x_num[0],x_num[len(x_num)-1],0.1)
#        y_test = lq.predict(x_test)
#        bx.plot(x_test, y_test)
        
#        print x_date
#        print datestr2num(x_date)
        #清空list下个循环再见
        x_date = []
        y_num = []
