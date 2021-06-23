from getPredicted import predict
import tkinter as tk
from tkinter import messagebox
from Spider import getList  # page, url, score
from matplotlib import pyplot as plt


def produceData(page, url, score):
    badNum, goodNum, goodReviews = 0, 0, []
    data = getList(page, url, score)
    for _ in data:
        if predict(_) == '真实评论':
            goodNum += 1
            goodReviews.append(_)
        else:
            badNum += 1
    return goodNum, badNum, goodReviews


def Visualization(page, url, score, flag):  # 数据可视化 flag代表是否将数据加载到桌面
    goodNum, badNum, goodReviews = produceData(page, url, score)
    y = [goodNum, badNum]
    color = ['#e17f0e', '#3694af']
    labels = ['True', 'False']
    plt.subplot(121)
    plt.bar(range(2), y, width=0.5, color=color, tick_label=labels)
    plt.xlabel('Types')
    plt.ylabel('Number')
    plt.title('The number of different species', fontsize=12)
    for a, b in zip(range(2), y):
        plt.text(a, b + 0.1, b, ha='center', va='bottom')
    # 开始饼状图绘制
    plt.subplot(122)
    plt.pie(y, labels=labels, autopct='%1.1f%%', shadow=False, colors=color)
    plt.axis('equal')  # 让饼长和宽相等
    plt.title('The proportion of different species', fontsize=12)
    plt.show()
    if flag == 0:
        return
    else:  # 数据加载到桌面
        with open('views.txt', 'w') as f:
            for con in goodReviews:
                f.write(con + '\n')
                print('success')


# 用户退出
def user_exit():
    window.destroy()


# 检测函数
def get_result():
    content = text.get("1.0", "end")
    if content == '\n' or content == ' ':
        tk.messagebox.showerror(title="Error", message="请输入一段有效文本！")
        return
    elif len(content) <= 5:
        result = '虚假评论'
    else:
        result = predict(content)
    output.delete(1.0, tk.END)
    output.insert(tk.END, result)


# 设置可视化函数
def get_vis():
    temp = tk.messagebox.askquestion(title='Warning!', message='您是否将真实评论存放在本地？')
    if temp == 'yes':
        flag = 1
    else:
        flag = 0
    page = numInput.get("1.0", "end")[:-1]
    url = urlInput.get("1.0", "end")[:-1]
    if len(url) < 2:
        tk.messagebox.showerror(title="Error", message="请输入有效的url!")
        return
    if r_value.get() == 'A':
        score = 3
    elif r_value.get() == 'B':
        score = 2
    else:
        score = 1
    print(f'page:{page},url:{url},score:{score}')
    Visualization(int(page), url, score, flag)


# 设置整体布局
window = tk.Tk()
window.title("智慧虚假评论检测平台")
window.iconbitmap("img/favicon.ico")
window.geometry('550x700')
var = tk.StringVar()
tk.Label(window, text='请输入一段待检测的文本：', font=("Calibri", 10)).place(x=40, y=180)
tk.Label(window, text='检测结果：', font=("Calibri", 10)).place(x=130, y=410)
tk.Label(window, text='检测网址（url)：', font=("Calibri", 10)).place(x=90, y=470)
tk.Label(window, text='检测页数：', font=("Calibri", 10)).place(x=130, y=510)

# 设置图片
photo = tk.PhotoImage(file="img/smartView.png")
photoLabel = tk.Label(window, image=photo)
photoLabel.place(x=250, y=20)

# 设置输入框
text = tk.Text(window, font=("Calibri", 10))
text.place(x=200, y=180, width=300, height=180)  # place处理位置信息

# 设置输出框
output = tk.Text(window, font=("Calibri", 10))
output.place(x=200, y=410, width=300, height=20)

# 设置检测模块
btn_test = tk.Button(window, text='  开始检测  ', command=get_result)
btn_test.place(x=300, y=370)
btn_exit = tk.Button(window, text='  退出  ', command=user_exit)
btn_exit.place(x=310, y=640)

# 设置url输入模块
urlInput = tk.Text(window, font=("Calibri", 10))
urlInput.place(x=200, y=470, width=300, height=20)  # place处理位置信息

# 设置检测评论页数目
numInput = tk.Text(window, font=("Calibri", 10))
numInput.place(x=200, y=510, width=300, height=20)  # place处理位置信息

# 设置种类选择
r_value = tk.StringVar()
rad_but3 = tk.Radiobutton(window, text='好评',
                          variable=r_value, value='A')
rad_but2 = tk.Radiobutton(window, text='中评',
                          variable=r_value, value='B')
rad_but1 = tk.Radiobutton(window, text='差评',
                          variable=r_value, value='C')
rad_but3.place(x=200, y=550)
rad_but2.place(x=300, y=550)
rad_but1.place(x=400, y=550)
btn_vis = tk.Button(window, text='  开始检测  ', command=get_vis)
btn_vis.place(x=300, y=590)

window.mainloop()
