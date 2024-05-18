#!/usr/bin/env python
# -*- coding:utf-8 -*-
# v5.16
import os,sys, cns

class ProX(cns.DataX):

    def __init__(self, init_path='', **kwargs):
        '''初始化'''
        kwargs = dict(
            conn = kwargs.get('conn', 0),
            usr = kwargs.get('usr', 'test'),
            pwd = kwargs.get('pwd', 'test'),
            host = kwargs.get('host', 'localhost'),
            db = kwargs.get('db', 'test'),
            port = kwargs.get('port', 3307),
        ) 
        super().__init__(**kwargs)  # 调用父类的初始化方法  
        self.status = 0             # 系统状态 0 正常，其他不正常
        self.file_path = os.path.realpath(sys.argv[0])   # 文件完整路径
        self.file_dir = os.path.dirname(self.file_path)       # 文件所在目录

        self.timex = cns.DateTimeX(kwargs.get('date', None)) # 时间对象
        self.cmdx = cns.cmdX(self.file_dir)
        self.strx = cns.strX()


    def to_db(self, **kwargs):
        '''EXCEL, csv 文档写入数据库, 增加复制模板'''
        kwargs = dict(       
            path = kwargs.get('path', ''),       # 读取路径
            header = kwargs.get('header', 0),    # 表头行
            ydrop = kwargs.get('ydrop', 0),      # 删除列
            xdrop = kwargs.get('xdrop', 0),      # 删除行，合计
            mode = kwargs.get('mode', 'append'), # 模式: 增量|覆盖|覆盖+增量(多文件单表)  append | replace | repapp
            recol = kwargs.get('recol', 0),      # 需修改字段名
            columns = kwargs.get('columns', 0),  # 选择字段
            fnames = kwargs.get('fnames', 0),    # 文件名
            ext = kwargs.get('ext', None),       # 文件扩展名            
            tname = kwargs.get('tname', None),   # 目标表名Mysql
            addcol = kwargs.get('addcol', 0),    # 增加列，通常是日期
            delrec = kwargs.get('delrec', 0),    # 根据表中某一列关键字删除数据,防止重复
            filt_col_str = kwargs.get('filt_col_str', ['\n',',',' ']),  # 过滤字段中字符
            converters = kwargs.get('converters', None),  # 可以在读取的时候对列数据进行变换 converters={"编号": lambda x: int(x) + 10})
            # EXCEL部分
            sheet_name = kwargs.get('sheet_name', 0), # 读 取EXCEL插页名字 数字按插页索引,字符串按插页名字
            # csv 部分 -S
            sep = kwargs.get('sep', ',\t'),      # 分隔符
            dtype = kwargs.get('dtype', None),   # 指定字段的类型  {'c1':np.float64, 'c2': str})        
            encoding = kwargs.get('encoding', 'gb18030'),   # 字符编码 tab  'utf-16'
            engine = kwargs.get('engine', 'python'), # 解释引擎
            
            # 本类定义
            fm_copy = kwargs.get('fm_copy', 0),  # 复制表
            del_tab = kwargs.get('del_tab', 0),  # 删除 tname  
            )
        
        if self.status == 0:            
            fm_copy = kwargs.get("fm_copy", 0)   # 复制的模板表
            tname = kwargs.get("tname", None)    # 到目标表
            del_tab = kwargs.get("del_tab", 0)   # 删除表， 默认0 不删除
            
            if fm_copy:
                print('\n复制:', fm_copy)
                super().copy_tab(fm_copy, tname, del_tab=1)  # 复制表结构前--先删除表
            
            if del_tab:
                super().del_tab(tname)  # 删除表                 
            super().to_db(**kwargs)     # 写表
         
            
    def to_pro(self, task_nm='任务名空', **kwargs):
        ''' 数据处理 '''
        if self.status == 0:            
            tname = kwargs.get("tname", None)   # 目标表            
            fm_copy = kwargs.get("fm_copy", 0)  # 复制表          
            del_tab = kwargs.get("del_tab", 0)  # 删除表， 默认0 不删除                  
            param = kwargs.get("param", None)   # 到目标表            
            sqld = kwargs.get("sqld", 0)        # 待执行的SQL            
            ren_tab = kwargs.get("ren_tab", 0)  # 重命名表名      
            
            if del_tab:
                super().del_tab(tname)  # 删除表
                
            if fm_copy:
                super().copy_tab(fm_copy, tname, del_tab=1) # 复制表
            
            if sqld:
                sql = sqld[task_nm]
                sql = sql.format(tname=tname, param=param)  # 格式化SQL ,双参数过度用
                #print(f"\n*********sql:", sql) 
                super().run_sql(sql, task_nm = task_nm)     # 执行SQL

            if ren_tab:
                super().ren_tab(to_copy, ren_tab)           # 修改表名, 用于临时表修改正式表名


    def run_sqls(self, run_sql, SQLD):        
        '''
        run_sql = {'1.更新_慧眼_渠道名称':'x12_0慧眼销售分月',  '2.更新_品类': 'x12_0慧眼销售分月'}
        SQLD = {'更新_慧眼_渠道名称':'select * from xxx'}
        批量运行SQL
        '''
        for sql_nm, param in run_sql.items():
            sql_nm = sql_nm.split('.')  # 取任务名
            print('执行:', sql_nm[0])
            if len(sql_nm) == 1:
                task_nm = sql_nm[0]
            else:
                task_nm = sql_nm[1]
            #print(param)
            self.to_pro(task_nm, param=param, sqld=SQLD) # 任务名称, 参数, 主脚本  setdefault(key[,default])


    def write_sql(self, **kwargs):  #write
        '''
        生成SQL, 减少重复性代码编写        
        '''
        sql_main = kwargs.get("sql_main", '')  # SQL需要重复的核心部分
        sql_main_index = kwargs.get("sql_main_index", [])  # 主要 SQL切换的关键字，当发现时选择list中下标1，默认下标0         
        file_nm = kwargs.get("file_nm", '')    # 输出的文件名
        old_nms = kwargs.get("old_nms", '')    # sql_main 中的原始替换字符      
        rep_nms = kwargs.get("rep_nms", [])    # 需要替换并重复增加的名字序列       
        sql_head = kwargs.get("sql_head", '')  # SQL 头部
        sql_tail = kwargs.get("sql_tail", '')  # SQL 尾部

        txt_obj = cns.TextX(f"{self.file_dir}/{file_nm}.sql")        
        txt_obj.write(sql_head)     # 添加头部
        for s_nm in rep_nms:
            if isinstance(sql_main, list):
                for index, value in enumerate(sql_main_index):
                    if value in s_nm:
                        s_nm = s_nm.replace(value, '') # 去除关键字
                        t_sql = sql_main[index].replace(old_nms, s_nm)
                    else:
                        t_sql = sql_main[0].replace(old_nms, s_nm)
            else:
                t_sql = sql_main.replace(old_nms, s_nm)
            txt_obj.append(t_sql)   # 添加中间重复层
        txt_obj.append(sql_tail)    # 添加尾部
        return ''.join(txt_obj.read())

    def sql_make(self, **kwargs):
        ''' 生产SQL '''
        file_nm = kwargs.get("file_nm", '')    # 输出的文件名          
        sql_head = kwargs.get("sql_head", '')  # SQL 头部
        sql_main = kwargs.get("sql_main", '')  # SQL需要重复的核心部分  
        sql_tail = kwargs.get("sql_tail", '')  # SQL 尾部
        params = kwargs.get("params", '')      # SQL 传参
        interval= kwargs.get("interval", 'UNION ALL')      # 间隔

        txt_obj = cns.TextX(f"{self.file_dir}/{file_nm}")
        txt_obj.write(sql_head)        # 创建文档
        for index, value in enumerate(params):
            if index:
                txt_obj.append(interval)
            sql_temp = sql_main.format(param=value)
            txt_obj.append(sql_temp)    # 循环增加
        txt_obj.append(sql_tail)        # 尾部
        return txt_obj
        

    def paste(self, **kwargs):
        ''' SQL 粘贴数据到指定插页单元格'''
        sql = kwargs.get("sql", '')            # sql代码
        param = kwargs.get("param", '')        # sql参数
        excel = kwargs.get("excel", '')        # excel对象
        sheet = kwargs.get("sheet", '')        # 插页名称
        paste_xy = kwargs.get("paste_xy", '')  # 粘贴位置
        header = kwargs.get("header", 0)       # 是否带表头

        sql = sql.format(param=param)          
        df1 = self.read_sql(sql)               # data_type="list" 
        excel.set_sheet(sheet)
        excel.paste(df1, paste_xy, header=header)  # 粘贴(数据, 粘贴位置, 是否要表头)



        
