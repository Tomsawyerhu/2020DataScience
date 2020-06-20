import json
import os
import urllib.request,urllib.parse
import zipfile
import math

#把src_zip解压缩，存到dest_dir中
def unzip(src_zip,dest_dir):
    if zipfile.is_zipfile(src_zip):
        zip_file=zipfile.ZipFile(src_zip,'r')
        for file in zip_file.namelist():
            zip_file.extract(file,dest_dir)
    else:
        print('第一个参数的路径'+src_zip+'不是压缩包，解压缩失败')

def remove_zip(zip_path):
    if os.path.exists(zip_path):
        os.remove(zip_path)
        print('路径'+zip_path+'解压后，完成删除操作')
    else:
        print('路径'+zip_path+'不存在，为什么要删除？')

def get_inner(dir):
    inner=[]
    for root,dirs,files in os.walk(dir):
        for file in files:
            inner.append(os.path.join(root,file))
    return inner

#Testcases Oriented Programming
def check_TO(path):
    fp=open(path,encoding="utf8")
    isTO=False
    suspected=0
    former_line=""
    line_num = 0 #suspected/line_num的比例高于阈值，判定为TO
    print_num=0 #print出现超过20次，判定为TO。print行数/总行数比例过高。

    for l in fp.readlines():
        l=l.lstrip()#用于截掉字符串左边的空格或指定字符
        if not(l.startswith("#")):#非注释
            line_num+=1
        else:#该行是注释，不算入行数，直接跳过
            former_line=l
            continue

        #看这行代码是否有TO的嫌疑
        if l.startswith("print"):
            print_num+=1

        if l.startswith("print") and former_line.startswith("if"):
            suspected += 1
        elif l.startswith("print") and former_line.startswith("elif"):
            suspected+=1
        elif l.startswith("print") and former_line.startswith("else"):
            suspected+=1

        former_line=l

    if print_num>20: isTO=True #print出现超过20次，判定为TO。
    elif line_num>0 and suspected/line_num>=0.3: isTO=True #suspected/line_num的比例高于阈值，判定为TO
    elif line_num>0 and print_num/line_num>=0.9: isTO=True #print行数/总行数比例过高。

    return isTO

def get_testCase_Nums(path):
    f = open(path, encoding="utf8")
    res = f.read()
    data = json.loads(res)
    return len(data)

def replace_char(dir):
    dir=dir.replace('*','_')
    # dir=dir.replace('\\',' ')
    dir = dir.replace('/', '_')
    dir = dir.replace('?', '_')
    dir = dir.replace(':', '_')
    dir = dir.replace('<', '_')
    dir = dir.replace('>', '_')
    dir = dir.replace('|', '_')
    dir = dir.replace('"', '_')
    return dir

def handle_pro(case):
    filename = urllib.parse.unquote(os.path.basename(case["case_zip"]))
    # url里最后一个/后的内容作为文件名,eg. 找相同字符_1578246661060.zip
    dir_filename=replace_char(filename)
    zip_url = pro_pre + dir_filename
    unzip_dir = zip_url + "_unzip\\" # eg     找相同字符_1578246661060.zip_unzip
    if not os.path.exists(unzip_dir):
        url = urllib.parse.quote(case["case_zip"], safe=";/?:@&=+$,")  # 编码url里的中文
        try:
            urllib.request.urlretrieve(url, zip_url)
            # url 下载的文件路径       #zip_url 文件下载到本地后，所在的路径
        except Exception as e:
            print("下载题目包失败", e)
        try:
            os.mkdir(unzip_dir)
        except Exception as e:
            print("在指定路径下创建文件夹失败",e)
        try:
            unzip(zip_url, unzip_dir)
            remove_zip(zip_url)
        except Exception as e:
            print("解压与删除，操作失败", e)
    inner_dict={}
    inner_dict["case_id"]=case["case_id"]
    inner_dict["case_type"]=case["case_type"]
    inner_dict["case_zip"]=case["case_zip"]
    inner_dict["case_name"]=filename #case_zip的url最后一个/后的内容
    testCases_url=unzip_dir+".mooctest\\testCases.json"
    inner_dict["testCase_Nums"]=get_testCase_Nums(testCases_url)
    pro_dict[inner_dict["case_id"]]=inner_dict

def handle_submit(case,user_id):
    records = case["upload_records"]
    # 将列表records里的字典元素，按照提交时间从先到后排序
    records.sort(key=lambda k: k["upload_time"])

    if len(records) == 0:
        return
    chosen_record = records[0]  #用选中的这次提交记录来判断是否TO
    # 从后向前遍历
    for i in range(len(records) - 1, 0, -1):
        if records[i]["score"] == case["final_score"]:
            chosen_record = records[i]
            break
    filename = urllib.parse.unquote(os.path.basename(chosen_record["code_url"]))  # url最后一个/后的内容，解码为中文
    # eg.文件名为单词分类_1582023289869.zip，下载的是个压缩包
    zip_url = submit_pre + "\\" + filename
    zip_url=replace_char(zip_url)
    unzip_dir = zip_url + "_unzip\\"
    if not os.path.exists(unzip_dir):
        if not os.path.exists(zip_url):
            try:
                urllib.request.urlretrieve(chosen_record["code_url"], zip_url)
                # 第一个参数：外部url
                # 第二个参数：指定了保存到本地的路径（如果未指定该参数，urllib会生成一个临时文件来保存数据）
            except Exception as e:
                print("下载提交代码失败", e)
        try:
            os.mkdir(unzip_dir)
        except Exception as e:
            print("在指定路径下创建文件夹失败", e)
        try:
            unzip(zip_url, unzip_dir)  # 外层解压
            remove_zip(zip_url)  # 解压后删除压缩包
            inner_zip = get_inner(unzip_dir)[0]  # 获取内层的压缩包
            unzip(inner_zip, unzip_dir)  # 内层解压缩，把inner_zip解压缩，存到unzip_dir中
            remove_zip(inner_zip)
        except Exception as e:
            print("外层解压并删除，获取内层并解压与删除，操作失败", e)
    record_dict={}
    record_dict["record_id"]=chosen_record["upload_id"]
    record_dict["case_id"]=case["case_id"]
    record_dict["user_id"]=user_id
    record_dict["record_url"]=chosen_record["code_url"]
    code_url = unzip_dir + "main.py"
    is_TO = check_TO(code_url)
    if is_TO:
        record_dict["is_TO"]=True
    else:
        record_dict["is_TO"]=False
        record_dict["final_score"]=chosen_record["score"]
        if int(record_dict["final_score"])!=100:
            record_dict["is_1A"]=False
            ln=len(records)
            record_dict["Nums_before_AC"]=ln
            idx1=math.ceil((ln-1)/4)          #向上取整
            idx2=ln-1
            record_dict["time_span"]=records[idx2]["upload_time"]-records[idx1]["upload_time"]
        elif int(records[0]["score"])==100:
            record_dict["is_1A"]=True
            record_dict["Nums_before_AC"]=0
            record_dict["time_span"]=0
        else:
            record_dict["is_1A"]=False
            for j in range(1,len(records)):
                if int(records[j]["score"])==100:
                    record_dict["Nums_before_AC"]=j-1
                    idx2=j
                    idx1=math.ceil(j/4)  #除以4，向上取整
                    record_dict["time_span"]=records[idx2]["upload_time"]-records[idx1]["upload_time"]
                    break
    record_lst.append(record_dict)


f=open("mini_sample.json",encoding="utf8")
res=f.read()
data=json.loads(res)
data=list(dict.values(data))

pro_dict={}
record_lst=[]

for user in data:
    cases=user["cases"]
    submit_pre = "mini_submit_code\\user_" + str(user["user_id"])
    pro_pre = "mini_answer_testCases\\"
    if not os.path.exists(submit_pre):
        os.mkdir(submit_pre)
    for case in cases:
        handle_pro(case)
        handle_submit(case,user["user_id"])

json_pro=json.dumps(pro_dict,ensure_ascii=False, indent=4, separators=(',', ': '))
#要加encoding="utf8" 否则输出到.json中中文乱码
with open('mini_pro_dict.json',mode='w',encoding="utf8") as f:
    f.write(json_pro)
json_record=json.dumps(record_lst,ensure_ascii=False,indent=4, separators=(',', ': '))
with open('mini_record_lst.json','w') as f:
    f.write(json_record)