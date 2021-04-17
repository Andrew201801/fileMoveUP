import json
import os
import shutil
image_path = 'F:\\test\\frames'

# 文件树
filedic={}


def get_filelist(dir):
    '''
    递归遍历获得文件树
    :param dir: 根目录
    :return: None
    '''
    if os.path.isdir(dir):
        temp = []
        for s in os.listdir(dir):
            newDir = os.path.join(dir, s)
            temp.append(s)
            get_filelist(newDir)
        filedic[dir] = temp


def remove_empty_dir(workDir):
    """
    删除空文件夹
    若文件夹A下只有一个文件夹B，则将B下文件挪到A中，将B删除
    :return:None
    """
    global filedic
    while True:
        Flag=False
        filedic={}
        get_filelist(workDir)
        for key, value in filedic.items():
            # 空文件夹，删除
            if len(value) == 0:
                os.rmdir(key)
                father = os.path.dirname(key)
                curentPath = key.split("\\")[-1]
                filedic[father].remove(curentPath)
            #  单文件夹的文件夹，把底层向上移动
            elif len(value) == 1:
                currentDir = os.path.join(key, value[0])
                # 文件夹A/文件夹B/一堆文件CDEF =》 文件夹A/一堆文件CDEF
                # currentDir=文件夹A/文件夹B
                if os.path.isdir(currentDir):
                    for i in filedic[currentDir]:
                        # C:\Users\Myth\Desktop\test\test1\test1\新建文本文档.txt
                        old = os.path.join(currentDir, i)
                        # C:\Users\Myth\Desktop\test\test1\新建文本文档.txt
                        new = os.path.join(key, i)
                        shutil.move(old, new)
                    try:
                        os.rmdir(currentDir)
                    except OSError:
                        print("%s 删除失败！"%(currentDir))
                # 文件夹A/文件夹B+文件夹C/一个文件D =》 文件夹A/一个文件D+文件夹C
                # currentDir=文件夹A/文件夹B/一个文件
                else:
                    old=currentDir
                    new=os.path.join(os.path.dirname(key),value[0])
                    shutil.move(old, new)
                    os.rmdir(key)
                Flag=True
                break

        if not Flag:
            break

def store_data():
    with open("file_dic.json", "w", encoding="utf-8") as f:
        json.dump(filedic, f, ensure_ascii=False, indent=4)


def merge_dir(workDir):
    '''
    将A11/B/A11文件目录中最后一个A11文件夹下的所有文件移到第一个A11文件夹下
    流程：
        从叶节点开始遍历，每次遍历以当前节点为根节点的子树，
        如果发现子树中的节点与根节点值相同，则进行合并文件夹操作
        完成后，重新生成文件树，重新遍历
        直到某次遍历完成后，没有进行过合并操作，退出循环
    :return: None
    '''
    global filedic
    while True:
        Flag = False
        filedic = {}
        get_filelist(workDir)
        # 从叶节点开始遍历
        for i in filedic.keys():
            childList = filedic[i]
            currentKey = i.split("\\")[-1]
            queue = []
            # 只遍历文件夹
            for j in childList:
                if "." not in j:
                    queue.append(j)
            while len(queue) > 0:
                now = queue[0]
                del queue[0]
                childDir = "%s\\%s" % (i, now)
                childKey = now.split("\\")[-1]
                # 发现相同文件夹名
                if childKey == currentKey:
                    newDir = i
                    oldDir = childDir
                    for j in filedic[oldDir]:
                        old = os.path.join(oldDir, j)
                        new = os.path.join(newDir, j)
                        shutil.move(old, new)
                    try:
                        os.rmdir(oldDir)
                    except OSError:
                        pass
                    Flag = True
                    break
                if os.path.isdir(childDir):
                    for j in filedic[childDir]:
                        if "." not in j:
                            # 合成新路径
                            queue.append("%s\\%s" % (now, j))
            if Flag:
                break
        if not Flag:
            break


if __name__ == '__main__':
    # workDir=input("输入要整理的目录：")
    workDir=r"C:\Users\Myth\Desktop\test"
    get_filelist(workDir)
    store_data()
    remove_empty_dir(workDir)
    merge_dir(workDir)



