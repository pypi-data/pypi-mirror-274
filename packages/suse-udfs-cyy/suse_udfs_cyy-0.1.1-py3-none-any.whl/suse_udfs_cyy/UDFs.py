def change_directorySlash(path,last_slash=True):
    """

    :param path: folder path, copied directly from the system, r"G:\insuranceimg\921", there must be r in front of this path string
    :param last_slash: whether or not add / to right, default true
    :return: forward-slash path, can be used in importing
    import os
    path = '/path/to/file/filename.txt'
    filename = os.path.basename(path)
    print(filename)   # 输出：filename.txt
    """
    list_path=path.split("\\")
    forward_slash_path=""
    for i in list_path:
        if forward_slash_path=="":
            forward_slash_path =  i
        else:
            forward_slash_path=forward_slash_path+"/"+i
    if last_slash==True and forward_slash_path[-1]!="/":
        forward_slash_path=forward_slash_path+"/"
    elif last_slash==False and forward_slash_path[-1]=="/":
        forward_slash_path = forward_slash_path[:-1]
    return forward_slash_path
# a=r"G:\insuranceimg\921"
# print(change_directorySlash(a))

def search_mode(array):
    import statistics
    """
    find the mode for high-d array
    :param array: array or list
    :return: the mode
    """
    flt = array.flatten()
    return statistics.mode(flt)

def plot_scatter_withxy(list_xy,xlabel="",ylabel="",title="",c="red",mk="o",large=10,reverse=False, dpi=1000):
    import matplotlib.pyplot as plt
    plt.figure(dpi=dpi)
    for xy in list_xy:
        if not reverse:
            x = int(xy[0])
            y = int(xy[1])
        else:
            x = int(xy[1])
            y = int(xy[0])
        plt.scatter(x, y, color=c,marker=mk, s=large)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()


def plot_scatter_overlap(dpi=1000,*xylst,**parameters):
    """
    [matplotlib.pyplot]draw one or multiple layers of points on an image, each layer has a list of xy coordinate for drawing.
    :param dpi: cant use dpi=1000 as input, just one value as input!
    :param xylst: for each layer, it should be like [[a1,b1],[a2,b2]....]
    for different layers, the len of this list can be different.
    :param parameters: paraGroup1=[color,marker,markersize,reverse_xy,["annotate1","annotate2",....]] (values for plt.scatter() parameters)
    :return: na
    exp code:
    2-layer
        combined_list=[list_sp2dindex,list(point_mid)]
        para_dic={"paraGroup1":["black","o",0.1,False,[]],"paraGroup2":["red","x",0.1,False,list(feature_name)]}, the fifth position is [] means no annotation
        for this set of coordinates
        suse_udfs_cyy.plot_scatter_overlap(1000,*combined_list,**para_dic)
        **"paraGroup1" can be anyother string.
    3-layer
        combined_list=[list_sp2dindex,list(point_mid),component_list]
    para_dic={"paraGroup1":["black","o",0.1,False,[]],\
             "paraGroup2":["red","x",0.1,False,list(feature_name)], \
            "paraGroup3":["yellow","x",0.08,False,[]]}
    suse_udfs_cyy.plot_scatter_overlap(1000,*combined_list,**para_dic)
    """
    assert len(xylst)==len(list(parameters.keys())), "suse_udfs_cyy warning: each input xy lst must have one and only one parameter list"
    import matplotlib.pyplot as plt
    from tqdm import tqdm
    plt.figure(dpi=dpi)
    # for i in tqdm(range(len(xylst)),desc="suse_udfs_cyy.plot_scatter_overlap working in progress"):
    for i in range(len(xylst)):
        one_xylist=xylst[i]
        para_list=parameters[list(parameters.keys())[i]]
        round=0
        for xy in tqdm(one_xylist,desc="suse_udfs_cyy.plot_scatter_overlap working in progress "+str(i+1)+" /"+str(len(xylst))):
            if not para_list[3]: # para_list[3]: reverse or not
                # x = int(xy[0])
                # y = int(xy[1])
                x=xy[0]
                y=xy[1]
            else:
                x = int(xy[1])
                y = int(xy[0])
            plt.scatter(x, y, color=para_list[0], marker=para_list[1], s=para_list[2])
            if len(para_list[4])!=0:
                plt.annotate(para_list[4][round], xy=(x, y), xytext=(x, y))
            round=round+1
    plt.show()


def colorful(s,color):
    """
    print(colorful("123","black")
    :param s: "string"
    :param color: "red","green","yellow","blue","magenta","green","white","black"
    :return:
    """
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
    #  前景色:红色  背景色:默认
    if color=="red":
        return Fore.RED + s + Fore.RESET

    #  前景色:绿色  背景色:默认
    elif color=="green":
        return Fore.GREEN + s + Fore.RESET

    #  前景色:黄色  背景色:默认
    elif color=="yellow":
        return Fore.YELLOW + s + Fore.RESET

    #  前景色:蓝色  背景色:默认
    elif color=="blue":
        return Fore.BLUE + s + Fore.RESET

    #  前景色:洋红色  背景色:默认
    elif color=="magenta":
        return Fore.MAGENTA + s + Fore.RESET

    #  前景色:青色  背景色:默认
    elif color=="green":
        return Fore.CYAN + s + Fore.RESET

    #  前景色:白色  背景色:默认
    elif color=="white":
        return Fore.WHITE + s + Fore.RESET

    #  前景色:黑色  背景色:默认
    elif color=="black":
        return Fore.BLACK

    #  前景色:白色  背景色:绿色
    elif color=="white+green":
        return Fore.WHITE + Back.GREEN + s

    elif color == "bright+green":
        return Style.BRIGHT + Fore.GREEN + s


def remove_create_folder(path):
    """
    :param path:
    :return:
    """
    import os
    import shutil
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)

def swap_columns(df,col1,col2):
    """
    switch existing col1 and col2 in the df
    :param df:
    :param col1: the index
    :param col2:
    :return:
    """
    import pandas as pd
    swap_df=pd.DataFrame()
    for i in range(len(df.columns)):
        if i==col1:
            swap_df[df.columns[col2]]=list(df.iloc[:,col2])
        elif i==col2:
            swap_df[df.columns[col1]] = list(df.iloc[:, col1])
        else:
            swap_df[df.columns[i]] = list(df.iloc[:, i])

    return swap_df

def insert_column(df,colname,colcontent,colindex):
    """

    :param df:
    :param colname: string
    :param colcontent: list
    :param colindex: starting from 0, left to right
    :return:
    """
    import pandas as pd
    new_df=pd.DataFrame()
    assert colindex<=df.shape[1]-1,"colindex exceeds the df col num"
    count=0
    for i in df.columns:
        if count == colindex:
            new_df[colname]=colcontent
            new_df[i] = df[i]
        else:
            new_df[i]=df[i]
        count=count+1
    return new_df

def del_col_bystr(df, accurate_del=[], vague_del=[]):
    """
    using str to del columns from a df
    :param df:
    :param accurate_del: elements should be exactly inside df.columns
    :param vague_del: as long as df.columns contain the element, the corresponding col is deleted
    :return:
    """
    for i in accurate_del:
        print("delete col: " + i)
        del df[i]
    for j in vague_del:
        for i in df.columns:
            if j in i:
                print("delete col: " + i)
                del df[i]
def del_row_byindex(df,list_index_ToBeDeleted=[]):
    """

    :param df:
    :param list_index_ToBeDeleted: [0,1,2,3].....
    :return:
    """
    import pandas as pd
    # need a default index sequence
    if list(df.index[:df.shape[0]])!=list(range(df.shape[0])):
        df.reset_index(inplace=True)
        del df["index"]
    assert list(df.index[:df.shape[0]])==list(range(df.shape[0])), "error terminate"
    df.drop(list_index_ToBeDeleted, axis=0, inplace=True)
    return df

def sort_dic(dic,descend=True,by="key"):
    """
    sort dic, by key or value, descend or ascend
    :param dic:
    :param descend:
    :param by: "key" or "value"
    :return:
    """
    import operator
    match by:
        case "key":
            by=0
        case "value":
            by=1
    l=sorted(dic.items(), key=operator.itemgetter(by), reverse=descend)
    return l
def combination(*group_list):
    """
    assume n boxes, each box contains unique balls.
    Take only one ball from each box, how many combinations in total?
    n is the len of group_list, each box is the elemental list of group_list
    :param group_list: combination([["s","b"],["a","b"]])
    :return:  ['s-a', 's-b', 'b-a', 'b-b']
    """
    import itertools as it
    c_list=[]

    for i in it.product(*eval(str(*group_list))):
        temp=""
        for j in i:
            if temp=="":
                temp=j
            else:
                temp=temp+"-"+j
        c_list.append(temp)
    # print(*group_list) # combination([["s","b"],["a","b"]])= [['s', 'b'], ['a', 'b']]
    # print(group_list) # combination([["s","b"],["a","b"]])= ([['s', 'b'], ['a', 'b']],)
    return c_list

#
# a=combination([["f1","f2","f3"],["a1","a2","a3"],["s1","s3"]])
# a=combination([["f1","f2","f3"],["a1","a2","a3"]])
# for i in a:
#     elements=i.split("-")
#     score=0
#     for j in elements:
#         score=score+int(j[-1])-2
#     print(i+"   "+str(score))

def display_info(labels, values):
    """
    result:
    1 2 3 labels
    1 2 3  index
    :param labels: list
    :param values: list
    :return:
    we can directly use this inside other functions
    in suse_udfs_cyy
    """
    import pandas as pd
    print("index-label relationship")
            # for i in range(len(labels)):
            #     print(str(i)+" : "+str(labels[i]))
    temp_list=[labels,values]
    info_df = pd.DataFrame(temp_list)
    info_df[" "]=["labels","index"]
    info_df.columns=[" " for i in range(info_df.shape[1])]
    print(info_df.to_string(index=False)) # to_string: cancel colname, index=false, cancel index



def affine_rotate(theta=45,center=(112,112),LR_amount=1,UD_amount=1,img_path='G:/clock project/augmentation_106/croppedimages/146 001.jpg',display=False):
    """
    a comprehensive rotation function bases on Affine
    support: Anticlock rotation on a designated center (ACR)
            left-right move
            up-down move
    separatedly or simutaneously
    :param theta: angle 0-360
    :param center: (x,y), think the system is x left-postive and y up-positive system
    :param LR_amount: pos=left
    :param UD_amount: pos=left
    :param img_path: the img
    :param display: display the result on IDE?
    :return: output the img in the same folder
    """
    import matplotlib.pyplot as plt
    import os
    from PIL import Image
    import numpy as np
    # Open your image
    image = Image.open(img_path)
    image=image.convert("RGB")
    name=img_path.split("/")[-1].split(".")[0]
    output_folder=img_path.strip(img_path.split("/")[-1])
    # Define the shift amount (1 pixel to the right)
    cx=center[0]
    cy = center[1]
    LR_amount=LR_amount
    # Shift the image
    shifted_image = image.copy()
    postfix="-"
    # rotate
    if theta!=0:
        shifted_image = shifted_image.transform(
            shifted_image.size,
            Image.Transform.AFFINE,
            (np.cos(theta*np.pi/180),-np.sin(theta*np.pi/180),
                -cx*np.cos(theta*np.pi/180)+cy*np.sin(theta*np.pi/180)+cx,
                np.sin(theta*np.pi/180),np.cos(theta*np.pi/180),
                -cx*np.sin(theta*np.pi/180)-cy*np.cos(theta*np.pi/180)+cy),
            resample=Image.Resampling.BICUBIC,
            fillcolor=(255,255,255))
        postfix = postfix + "ACR"+str(int(theta))
    # left-right
    if LR_amount!=0:
        shifted_image = shifted_image.transform(
            shifted_image.size,
            Image.Transform.AFFINE,
            (1, 0, LR_amount, 0, 1, 0),
            resample=Image.Resampling.BICUBIC,
            fillcolor=(255,255,255))
        postfix = postfix+"L" + str(int(LR_amount)) if LR_amount > 0 else "R" + str(int(abs(LR_amount)))
    # up-down
    if UD_amount != 0:
        shifted_image = shifted_image.transform(
            shifted_image.size,
            Image.Transform.AFFINE,
            (1, 0, 0, 0, 1, UD_amount),
            resample=Image.Resampling.BICUBIC,
            fillcolor=(255,255,255))
        next_postfix="U"+str(int(UD_amount)) if UD_amount>0 else "D"+str(int(UD_amount))
        postfix = postfix +next_postfix

    shifted_image.save(output_folder+name+postfix+".jpg")

    if display:
        plt.imshow(shifted_image)
        plt.title(postfix)
        plt.show()
def pie_enhanced(df, colname, load_mode="value-desc",
                 split_index_list=[],name_overwrite_forsplit=[],explode=[],
                 wd=10,title="",titlefont=40, labelfont=20,
                 swtich_last_values=0, pdist=0.9, ld=1.1, rd=1):
    """

    :param df:
    :param colname: the column you want to draw pie chart on
    :param load_mode: how to sort key-value frame
    "value-desc" use value's descending order
    "value-asc"
    "key-asc"
    "key-desc"
    :param split_index_list: [[0],[1,9],[10,11]]
    one-element sublist means only this key in a sector
    1,9 means unique keys 1-9 in one sector
    no overlap on end points
    must form a complete interval
    :param name_overwrite_forsplit: leave it blank will use unique keys as labels
    if not blank, make sure the length of it equal to the length of split_index_list
    ["overwrite1",0,0,0], 1st interval overwrite with the string, the other labels continue using unique keys
    :param explode: decide which part flies out
     if not blank, make sure the length of it equal to the length of split_index_list
    [0,0,0,0] make the value deviate from 0 will result in the sector flying out. 0.1 is large enough
    :param title: major title of pie chart
    :param titlefont: ft size of major title of pie chart
    :param labelfont: ft size of labels
    :param swtich_last_values: insert the last sectors to the former part
    :param pdist: pct value distance from the circle center
    :param ld: label string distance from the circle center
    :param rd: the radius of pie
    :return:
    """
    # value_count by default will sort by value, desc

    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    # read mode
    labels=[]
    counts=[]
    target=[]
    match load_mode:
        case "value-desc":
            target=df[colname].value_counts()
        case "value-asc":
            target = df[colname].value_counts(ascending=True)
        case "key-asc":
            target=df[colname].value_counts().sort_index()
        case "key-desc":
            target = df[colname].value_counts().sort_index(ascending=False)

    labels = list(target.index)
    counts = list(target.values)
    # print index-label
    print("index-label relationship")
            # for i in range(len(labels)):
            #     print(str(i)+" : "+str(labels[i]))
    temp_list=[labels,list(range(len(labels)))]
    info_df = pd.DataFrame(temp_list)
    info_df[" "]=["labels","index"]
    info_df.columns=[" " for i in range(info_df.shape[1])]
    print(info_df.to_string(index=False))
    # merge sectors
    if len(split_index_list)!=0:
        for sublist in split_index_list:
            assert len(sublist)<=2,"illegal split input"+str(sublist)
        new_labels=[]
        new_counts=[]
        for sublist in split_index_list:
            if len(sublist)==1:
                i=sublist[0]
                new_labels.append(labels[i])
                new_counts.append(counts[i])
            elif len(sublist)==2:
                new_labels.append(str(labels[sublist[0]])+"~"+str(labels[sublist[1]]))
                new_counts.append(np.sum(counts[sublist[0]:sublist[1]+1]))
        labels=new_labels
        counts=new_counts
    # sector name overwrite
    if len(name_overwrite_forsplit)!=0:
        assert len(name_overwrite_forsplit)==len(split_index_list)
        for i in range(len(name_overwrite_forsplit)):
            if name_overwrite_forsplit[i]==0:
                continue
            else:
                labels[i]=name_overwrite_forsplit[i]
    # interpolation
    if swtich_last_values != 0:
        last_labels = labels[len(labels) - swtich_last_values:]
        last_counts = counts[len(labels) - swtich_last_values:]
        labels = labels[:len(labels) - swtich_last_values]
        counts = counts[:len(counts) - swtich_last_values]
        for i in range(len(last_labels)):
            labels.insert(2 * i + 1, last_labels[i])
            counts.insert(2 * i + 1, last_counts[i])
    # adjust explosion for non-case
    if len(explode)==0:
        explode=list(np.zeros(len(counts)))
    # adjust tile for non
    if title=="":
        title=colname
    # realize display pct + values
    def func(pct, allvals):
        absolute = int(pct / 100. * sum(allvals))
        return "{:.1f}%\n({:d})".format(pct, absolute)
    # drawing area
    plt.rcParams["figure.figsize"] = (wd, wd)

    # plt.pie(x=counts, labels=labels, textprops={"fontsize":labelfont},autopct="%1.2f%%",
    #         explode=explode,pctdistance=pdist, labeldistance=ld, radius=rd)
    plt.pie(x=counts, labels=labels, textprops={"fontsize":labelfont},autopct=lambda pct: func(pct, counts),
            explode=explode,pctdistance=pdist, labeldistance=ld, radius=rd)
    # plt.legend()
    plt.title(title, fontsize=titlefont)
    plt.show()

def box_plot(NestedList_data,list_boxNames,positions,xlabel="",ylabel="",title=""):
    import matplotlib.pyplot as plt
    plt.grid(True)  #
    plt.boxplot(NestedList_data,
                medianprops={'color': 'red', 'linewidth': '1.5'},
                meanline=True,
                showmeans=True,
                showfliers=True,
                meanprops={'color': 'blue', 'ls': '--', 'linewidth': '1.5'},
                flierprops={"marker": "o", "markerfacecolor": "red", "markersize": 10},
                labels=list_boxNames,
                positions=positions)
    # plt.yticks(np.arange(0.4, 0.91, 0.1))
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()


def wordcloud(text):
    from wordcloud import WordCloud
    import matplotlib.pyplot as plt
    # 你想要显示的词汇
    text = text

    # 创建词云对象
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

    # 显示生成的词云图
    plt.figure(figsize=(8, 4))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')  # 关闭坐标轴
    plt.show()


def binary_class_metrics(real_list,predict_list,prt=False):
    TP=0
    TN=0
    FP=0
    FN=0
    for i in range(len(real_list)):
        real=real_list[i]
        predict=predict_list[i]
        if real==1:
            if predict==1:
                TP=TP+1
            else:
                FP=FP+1
        else:
            if predict==0:
                TN=TN+1
            else:
                FN=FN+1
    Acc=(TP+TN)/len(real_list)
    Precision=TP/(TP+FP)
    Recall=TP/(TP+FN)
    F1=2*Precision*Recall/(Precision+Recall)
    if prt:
        print(f"Accuracy: {Acc}\nPrecision: {Precision}\nRecall: {Recall}\nF1: {F1}")
    return Acc,Precision,Recall,F1


def multiBar(X_names, bar_names, data, xlabel, ylabel, title):
    """
    :param X_names: values of X, list, len=len(data)
    :param bar_names: names of each bar
    :param data: [[],[],[]]
    :return:
    """
    import matplotlib.pyplot as plt
    import numpy as np

    # Sample data
    X_names = X_names  # X-axis Names
    bar_names = bar_names  # legend Names
    data = np.array(data)

    num_years = len(X_names)
    x = np.arange(num_years)  # the label locations
    width = 0.2  # the width of the bars

    fig, ax = plt.subplots()
    for i in range(len(bar_names)):
        ax.bar(x + i * width, data[:, i], width, label=bar_names[i])

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.set_xticks(x + width + width / 2)
    ax.set_xticklabels(X_names)
    ax.legend()

    # Display the plot
    plt.show()

def list_ongoing_process():
    """
    list all ongoing programs, alphabetic ascending order, lowercase
    :return:
    """
    import psutil
    program_name_list=[]
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            program_name_list.append(proc.info['name'].lower())
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    program_name_list.sort()
    return program_name_list
def is_process_running(process_name):
    import psutil
    detect=False
    task_list=list_ongoing_process()
    # 遍历当前活动的进程
    for proc in task_list:
        if process_name.lower() in proc:
            detect=True
            break
    return detect

def pandas_df_display_full():
    import pandas as pd
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('max_colwidth', 1000)
    pd.set_option('expand_frame_repr', False)
