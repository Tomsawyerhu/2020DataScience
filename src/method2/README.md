### **运行顺序：**

**pre1.py -> pre2.py -> scrapy.py -> handle_data.py -> relation_analysis.py -> model.py**



### 各文件主要功能与重要方法功能

#### 1、pre1.py

从https://atcoder.jp上全部grand contests001-046中挑选18场比赛，并获取选中比赛的题目难度分值，写入contests文件夹下对应比赛文件夹下的.csv中

##### get_difficulty()

#### 2、pre2.py

将pre1.py爬取的各场比赛的题目分值合并，得到pro.csv

#### 3、scrapy.py

获取所有比赛的提交记录

##### get_records()

获取每场比赛的提交记录，并分别写入contests\agc004\record_004.csv中

###### get_time_and_pages()

获取比赛开始和结束时间 以及 总页数

###### get_all_records()

爬取每场比赛的提交记录,仅取比赛时间内的提交

#### 4、handle_data.py

根据每场比赛的提交记录，在pro.csv基础上得到pro_with_features.csv

#### 5、relation_analysis.py

双变量相关性分析

spearman相关评估两个连续变量之间的单调关系

#### 6、model.py

###### param()

对AdoBoost框架学习器个数进行择优

###### param2()

对CART分类树的深度进行择优

###### AdaBoost()

###### assessment()

准确率评估

