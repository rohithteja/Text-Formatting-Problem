from tkinter import *
from tkinter import Toplevel,messagebox,ttk
from math import ceil,floor,inf
import numpy as np
from time import time, strftime, localtime
from datetime import timedelta
import sys
from itertools import combinations, chain
from collections import deque
import timeit

def secondsToStr(elapsed=None):
    if elapsed is None:
        return strftime("%Y-%m-%d %H:%M:%S", localtime())
    else:
        return str(timedelta(seconds=elapsed))

def align_spacing(line,threshold,align='L'):
    if align=='L':
        return line+' '*(threshold-len(line))
    elif align=='R':
        return ' '*(threshold-len(line))+line
    elif align=='C':
        return ' '*ceil((threshold-len(line))/2)+line+' '*floor((threshold-len(line))/2)
    else:
        raise ValueError('Please use only C or L or R for Center, Left and Right alignments')

class Dynamic:
    line=''
    threshold=0
    input_=''
    align=''
    breaks = []
    cost_array = []
    input_arr=[]
    total_cost=0

    def __init__(self,input_,threshold,align):
        self.input_=input_
        self.threshold=threshold
        self.align=align
        self.input_arr=input_.split()
        self.update_line_breaks()

    def space_cost(self,line,threshold):

        length_line = len(line) - 1

        for word in line:
            length_line += len(word)

        if length_line > threshold:
            return inf

        return (threshold - length_line)**3

    def update_line_breaks(self):
        #global cost_array
        #global input_arr
        #global breaks
        self.cost_array=[0]*(len(self.input_.split())+1)
        self.breaks=[0]*(len(self.input_.split())+1)
        for i in range(len(self.input_arr)-1,-1,-1):
            temp = [self.cost_array[j] + self.space_cost(self.input_arr[i:j],self.threshold) for j in range(i+1,len(self.input_arr)+1)]
            index = np.argmin(temp)
            self.breaks[i] = index + i + 1
            self.cost_array[i] = temp[index]

    def dynamic_formatter(self):

        lines = []
        linebreaks = []

        i = 0
        while True:

            linebreaks.append(self.breaks[i])
            i = self.breaks[i]
            if i == len(self.input_arr):
                linebreaks.append(0)
                break

        for i in range( len(linebreaks) ):
            lines.append( ' '.join( self.input_arr[ linebreaks[i-1] : linebreaks[i] ] ).strip() )

        lines.pop()
        return lines

def check_values():
    threshold=page_width.get()
    input_=text.get("1.0",END)
    if input_.isspace() or not input_:
        messagebox.showerror(title='Input Error', message='Please provide a valid input!, exiting program. Please re-run again')
        sys.exit()
    list_arr=input_.split()
    max_len=len(max(list_arr,key=len))
    if threshold =='':
        messagebox.showerror(title='Page Width Error', message='Please provide a valid page width!, exiting program. Please re-run again')
        sys.exit()
    if threshold < max_len:
        messagebox.showwarning(title='Page Width Warning', message='The longest word in the sentence is {0}, please provide a threshold equal or higher than the longest word to see proper alignment:'.format(max_len))



def run_greedy():
    check_values()
    new_window = Toplevel(root)
    new_window.title("Greedy Algorithm")
    #greedy_label = Label(new_window,justify=LEFT,anchor=W)
    #greedy_label.pack(side=LEFT)


    list_arr=text.get("1.0",END).split()
    threshold=page_width.get()
    align=radio_var.get()
    txt = Text(master=new_window,width=(threshold+35),height=30)
    txt.pack(side=LEFT)
    scroll=Scrollbar(new_window)
    scroll.pack(side=RIGHT,fill=Y)
    scroll.config(command=txt.yview)
    txt.config(yscrollcommand=scroll.set)
    txt.insert(END,'Please find the alignment and printing below:')
    txt.insert(END,str('\n'+'-'*(threshold+2)))
    #greedy_label.config(text=list_arr)
    start = time()
    wordcount = len(list_arr)
    counter = 0
    totallength = 0
    total_cost=0
    line=''
    final_line=''
    while counter < wordcount:
        length = len(list_arr[counter])
        totallength = totallength + length

        if totallength >= threshold:
            totallength = length
            #print('|',align_spacing(line,threshold,align),'|',', the cost for the line is:',(threshold-len(line))**3)
            #final_line=final_line+'\n'+'|'+align_spacing(line,threshold,align)+'|'+', the cost for the line is:'+str((threshold-len(line))**3)
            txt.insert(END,str('\n|'+align_spacing(line,threshold,align)+'|'+', the cost for the line is:'+str((threshold-len(line))**3)))
            total_cost+=(threshold-len(line))**3
            line=list_arr[counter]

        else:
            if counter == 0:
                line=list_arr[counter]
            else:
                totallength = totallength + 1
                line=line+' '+list_arr[counter]
        if counter==(wordcount-1):
            #print('|',align_spacing(line,threshold,align),'|',', the cost for the line is:',(threshold-len(line))**3)
            #final_line=final_line+'\n'+'|'+align_spacing(line,threshold,align)+'|'+', the cost for the line is:'+str((threshold-len(line))**3)
            txt.insert(END,str('\n|'+align_spacing(line,threshold,align)+'|'+', the cost for the line is:'+str((threshold-len(line))**3)))
            total_cost+=(threshold-len(line))**3
            #print('The total cost is:',total_cost)
        counter = counter + 1
    end = time()
    elapsed = end-start
    txt.insert(END,str('\n'+'-'*(threshold+2)))
    txt.insert(END,str('\nPage Width is: '+str(threshold)))
    txt.insert(END,str('\nThe Total Cost is: '+str(total_cost)))
    txt.insert(END,str('\nThe Execution Time is: '+secondsToStr(elapsed)+'s'))
    txt.config(state='disable')
    #greedy_label.config(text=final_line,width=(threshold+50))


def run_dynamic():
    check_values()
    new_window = Toplevel(root)
    new_window.title("Dynamic Algorithm")
    input_=text.get("1.0",END)
    #list_arr=text.get("1.0",END).split()
    threshold=page_width.get()
    align=radio_var.get()
    txt = Text(master=new_window,width=(threshold+35),height=30)
    txt.pack(side=LEFT)
    txt.insert(END,'Please find the alignment and printing below:')
    txt.insert(END,str('\n'+'-'*(threshold+2)))
    scroll=Scrollbar(new_window)
    scroll.pack(side=RIGHT,fill=Y)
    scroll.config(command=txt.yview)
    txt.config(yscrollcommand=scroll.set)
    start=time()
    dynamic_obj=Dynamic(input_, threshold, align)
    lines=dynamic_obj.dynamic_formatter()
    #elapsed = time()-start
    #print(lines)
    total_cost=0
    #end = time()
    #elapsed = end-start
    #start_time = time()
    for i in lines:
        txt.insert(END,str('\n|'+align_spacing(i,threshold,align)+'|'+', the cost for the line is:'+str((threshold-len(i))**3)))
        total_cost+=(threshold-len(i))**3
    elapsed = (time()-start)/10
    txt.insert(END,str('\n'+'-'*(threshold+2)))
    txt.insert(END,str('\nPage Width is: '+str(threshold)))
    txt.insert(END,str('\nThe Total Cost is: '+str(total_cost)))
    txt.insert(END,str('\nThe Execution Time is: '+secondsToStr(elapsed)+'s'))
    txt.config(state='disable')

def consecutiveCombinations(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def run_brute_force():
    check_values()

    input_=text.get("1.0",END)

    words = input_.split()
    wordcount = len(words)

    if wordcount > 25:
        messagebox.showinfo(title='Word Exceed Warning', message='Please provide a valid text input which has word count less than 25 or run another method.')

    else:
        new_window = Toplevel(root)
        new_window.title("Brute Force Algorithm")

        #list_arr=text.get("1.0",END).split()
        threshold=page_width.get()
        align=radio_var.get()
        txt = Text(master=new_window,width=(threshold+35),height=30)
        txt.pack(side=LEFT)
        txt.insert(END,'Please find the alignment and printing below:')
        txt.insert(END,str('\n'+'-'*(threshold+2)))
        scroll=Scrollbar(new_window)
        scroll.pack(side=RIGHT,fill=Y)
        scroll.config(command=txt.yview)
        txt.config(yscrollcommand=scroll.set)
        start=time()

        minimum = 10 ** 20
        breaks = ()

        for combination in consecutiveCombinations(range(1, wordcount)):
            cost = 0
            i = 0
            for j in chain(combination, (wordcount,)):
                lineLength = len(' '.join(words[i:j]))
                if lineLength > threshold:
                    break
                cost += (threshold - lineLength) ** 2
                i = j

            else:
                if cost < minimum:
                    minimum = cost
                    breaks = combination

        lines = []
        i = 0
        for j in chain(breaks, (wordcount,)):
            lines.append(' '.join(words[i:j]))
            i = j

        total_cost=0
        for i in lines:
            txt.insert(END,str('\n|'+align_spacing(i,threshold,align)+'|'+', the cost for the line is:'+str((threshold-len(i))**3)))
            total_cost+=(threshold-len(i))**3
        end = time()
        elapsed = end-start
        txt.insert(END,str('\n'+'-'*(threshold+2)))
        txt.insert(END,str('\nPage Width is: '+str(threshold)))
        txt.insert(END,str('\nThe Total Cost is: '+str(total_cost)))
        txt.insert(END,str('\nThe Execution Time is: '+secondsToStr(elapsed)+'s'))
        txt.config(state='disable')


def run_branch_and_bound():
    check_values()

    input_=text.get("1.0",END)

    words = input_.split()
    wordcount = len(words)


    if (wordcount > 25):
        messagebox.showwarning(title='Word Exceed Warning', message='Please provide a valid text input which has word count less than 25 or run another method.')

    else:
        new_window = Toplevel(root)
        new_window.title("Branch And Bound Algorithm")

        #list_arr=text.get("1.0",END).split()
        threshold=page_width.get()
        align=radio_var.get()
        txt = Text(master=new_window,width=(threshold+35),height=30)
        txt.pack(side=LEFT)
        txt.insert(END,'Please find the alignment and printing below:')
        txt.insert(END,str('\n'+'-'*(threshold+2)))
        scroll=Scrollbar(new_window)
        scroll.pack(side=RIGHT,fill=Y)
        scroll.config(command=txt.yview)
        txt.config(yscrollcommand=scroll.set)
        start=time()

        words = input_.split()
        wordcount = len(words)

        minimum = 10 ** 20
        breaks = ()

        for combination in consecutiveCombinations(range(1, wordcount)):
            cost = 0
            i = 0
            for j in chain(combination, (wordcount,)):
                lineLength = len(' '.join(words[i:j]))
                if lineLength > threshold:
                    break
                cost += (threshold - lineLength) ** 2
                i = j
                if cost > minimum:
                    break

            else:
                if cost < minimum:
                    minimum = cost
                    breaks = combination

        lines = []
        i = 0
        for j in chain(breaks, (wordcount,)):
            lines.append(' '.join(words[i:j]))
            i = j

        total_cost=0
        for i in lines:
            txt.insert(END,str('\n|'+align_spacing(i,threshold,align)+'|'+', the cost for the line is:'+str((threshold-len(i))**3)))
            total_cost+=(threshold-len(i))**3
        end = time()
        elapsed = end-start
        txt.insert(END,str('\n'+'-'*(threshold+2)))
        txt.insert(END,str('\nPage Width is: '+str(threshold)))
        txt.insert(END,str('\nThe Total Cost is: '+str(total_cost)))
        txt.insert(END,str('\nThe Execution Time is: '+secondsToStr(elapsed)+'s'))
        txt.config(state='disable')

def run_divide_and_conqure():
    check_values()
    new_window = Toplevel(root)
    new_window.title("Divide and Conquer")

    input_=text.get("1.0",END)
    #list_arr=text.get("1.0",END).split()
    threshold=page_width.get()
    align=radio_var.get()
    txt = Text(master=new_window,width=(threshold+35),height=30)
    txt.pack(side=LEFT)
    txt.insert(END,'Please find the alignment and printing below:')
    txt.insert(END,str('\n'+'-'*(threshold+2)))
    scroll=Scrollbar(new_window)
    scroll.pack(side=RIGHT,fill=Y)
    scroll.config(command=txt.yview)
    txt.config(yscrollcommand=scroll.set)
    start=time()

    words = input_.split()
    count = len(words)
    offsets = [0]
    for w in words:
        offsets.append(offsets[-1] + len(w))

    minima = [0] + [10 ** 20] * count
    breaks = [0] * (count + 1)

    def cost(i, j):
        w = offsets[j] - offsets[i] + j - i - 1
        if w > threshold:
            return 10 ** 10
        return minima[i] + (threshold - w) ** 2

    def search(i0, j0, i1, j1):
        stack = [(i0, j0, i1, j1)]
        while stack:
            i0, j0, i1, j1 = stack.pop()
            if j0 < j1:
                j = (j0 + j1) // 2
                for i in range(i0, i1):
                    c = cost(i, j)
                    if c <= minima[j]:
                        minima[j] = c
                        breaks[j] = i
                stack.append((breaks[j], j+1, i1, j1))
                stack.append((i0, j0, breaks[j]+1, j))

    n = count + 1
    i = 0
    offset = 0
    while True:
        r = min(n, 2 ** (i + 1))
        edge = 2 ** i + offset
        search(0 + offset, edge, edge, r + offset)
        x = minima[r - 1 + offset]
        for j in range(2 ** i, r - 1):
            y = cost(j + offset, r - 1 + offset)
            if y <= x:
                n -= j
                i = 0
                offset += j
                break
        else:
            if r == n:
                break
            i = i + 1

    lines = []
    j = count
    while j > 0:
        i = breaks[j]
        lines.append(' '.join(words[i:j]))
        j = i
    lines.reverse()

    total_cost=0
    for i in lines:
        txt.insert(END,str('\n|'+align_spacing(i,threshold,align)+'|'+', the cost for the line is:'+str((threshold-len(i))**3)))
        total_cost+=(threshold-len(i))**3
    end = time()
    elapsed = end-start
    txt.insert(END,str('\n'+'-'*(threshold+2)))
    txt.insert(END,str('\nPage Width is: '+str(threshold)))
    txt.insert(END,str('\nThe Total Cost is: '+str(total_cost)))
    txt.insert(END,str('\nThe Execution Time is: '+secondsToStr(elapsed)+'s'))
    txt.config(state='disable')

def run_binary_search():

    check_values()
    new_window = Toplevel(root)
    new_window.title("BinarySearch")

    input_=text.get("1.0",END)
    #list_arr=text.get("1.0",END).split()
    threshold=page_width.get()
    align=radio_var.get()
    txt = Text(master=new_window,width=(threshold+35),height=30)
    txt.pack(side=LEFT)
    txt.insert(END,'Please find the alignment and printing below:')
    txt.insert(END,str('\n'+'-'*(threshold+2)))
    scroll=Scrollbar(new_window)
    scroll.pack(side=RIGHT,fill=Y)
    scroll.config(command=txt.yview)
    txt.config(yscrollcommand=scroll.set)
    start=time()

    words = input_.split()
    count = len(words)
    offsets = [0]
    for w in words:
        offsets.append(offsets[-1] + len(w))

    minima = [0] + [10 ** 20] * count
    breaks = [0] * (count + 1)

    def c(i, j):
        w = offsets[j] - offsets[i] + j - i - 1
        if w > threshold:
            return 10 ** 10
        return minima[i] + (threshold - w) ** 2

    def h(l, k):
        low, high = l + 1, count
        while low < high:
            mid = (low + high) // 2
            if c(l, mid) <= c(k, mid):
                high = mid
            else:
                low = mid + 1
        if c(l, high) <= c(k, high):
            return high
        return l + 2

    q = deque([(0, 1)])
    for j in range(1, count + 1):
        l = q[0][0]
        if c(j - 1, j) <= c(l, j):
            minima[j] = c(j - 1, j)
            breaks[j] = j - 1
            q.clear()
            q.append((j - 1, j + 1))
        else:
            minima[j] = c(l, j)
            breaks[j] = l
            while c(j - 1, q[-1][1]) <= c(q[-1][0], q[-1][1]):
                q.pop()
            q.append((j - 1, h(j - 1, q[-1][0])))
            if j + 1 == q[1][1]:
                q.popleft()
            else:
                q[0] = q[0][0], (q[0][1] + 1)

    lines = []
    j = count
    while j > 0:
        i = breaks[j]
        lines.append(' '.join(words[i:j]))
        j = i
    lines.reverse()

    total_cost=0
    for i in lines:
        txt.insert(END,str('\n|'+align_spacing(i,threshold,align)+'|'+', the cost for the line is:'+str((threshold-len(i))**3)))
        total_cost+=(threshold-len(i))**3
    end = time()
    elapsed = end-start
    txt.insert(END,str('\n'+'-'*(threshold+2)))
    txt.insert(END,str('\nPage Width is: '+str(threshold)))
    txt.insert(END,str('\nThe Total Cost is: '+str(total_cost)))
    txt.insert(END,str('\nThe Execution Time is: '+secondsToStr(elapsed)+'s'))
    txt.config(state='disable')

def run_personal():
    check_values()
    threshold=page_width.get()
    input_=text.get('1.0',END)
    align=radio_var.get()
    new_window = Toplevel(root)
    new_window.title("Personal Algorithm")
    txt = Text(master=new_window,width=(threshold+35),height=30)
    txt.pack(side=LEFT)
    scroll=Scrollbar(new_window)
    scroll.pack(side=RIGHT,fill=Y)
    scroll.config(command=txt.yview)
    txt.config(yscrollcommand=scroll.set)
    txt.insert(END,'Please find the alignment and printing below:')
    txt.insert(END,str('\n'+'-'*(threshold+2)))
    start = time()
    index=0
    final=0
    wordcount=0
    blank_space=0
    list_arr = []
    for i in input_:
        if (i == " "):
            list_arr.append(input_[final:index])
            blank_space = index
            final = index + 1
            wordcount = wordcount + 1
        index = index + 1
    wordcount = wordcount + 1
    list_arr.append(input_[blank_space+1:])
    counter = 0
    totallength = 0
    total_cost=0
    line=''
    while counter < wordcount:
        length = len(list_arr[counter])
        totallength = totallength + length

        if totallength >= threshold:
            totallength = length
            txt.insert(END,str('\n|'+align_spacing(line,threshold,align)+'|'+', the cost for the line is:'+str((threshold-len(line))**3)))
            #print(str('\n|'+align_spacing(line,threshold,align)+'|'+', the cost for the line is:'+str((threshold-len(line))**3)))
            total_cost+=(threshold-len(line))**3
            line=list_arr[counter]

        else:
            if counter == 0:
                line=list_arr[counter]
            else:
                totallength = totallength + 1
                line=line+' '+list_arr[counter]
        if counter==(wordcount-1):
            txt.insert(END,str('\n|'+align_spacing(line.replace('\n',''),threshold,align)+'|'+', the cost for the line is:'+str((threshold-len(line))**3)))
            total_cost+=(threshold-len(line))**3
            #print('The total cost is:',total_cost)
        counter = counter + 1
    end = time()
    elapsed = end-start
    txt.insert(END,str('\n'+'-'*(threshold+2)))
    txt.insert(END,str('\nPage Width is: '+str(threshold)))
    txt.insert(END,str('\nThe Total Cost is: '+str(total_cost)))
    txt.insert(END,str('\nThe Execution Time is: '+secondsToStr(elapsed)+'s'))
    txt.config(state='disable')

def run_shortest_path():

    check_values()
    new_window = Toplevel(root)
    new_window.title("Shortest")

    input_=text.get("1.0",END)
    #list_arr=text.get("1.0",END).split()
    threshold=page_width.get()
    align=radio_var.get()
    txt = Text(master=new_window,width=(threshold+35),height=30)
    txt.pack(side=LEFT)
    txt.insert(END,'Please find the alignment and printing below:')
    txt.insert(END,str('\n'+'-'*(threshold+2)))
    scroll=Scrollbar(new_window)
    scroll.pack(side=RIGHT,fill=Y)
    scroll.config(command=txt.yview)
    txt.config(yscrollcommand=scroll.set)
    start=time()
    words = input_.split()
    count = len(words)
    offsets = [0]
    for w in words:
        offsets.append(offsets[-1] + len(w))

    minima = [0] + [10 ** 20] * count
    breaks = [0] * (count + 1)

    for i in range(count):
        j = i + 1
        while j <= count:
            w = offsets[j] - offsets[i] + j - i - 1
            if w > threshold:
                break
            cost = minima[i] + (threshold - w) ** 2
            if cost < minima[j]:
                minima[j] = cost
                breaks[j] = i
            j += 1


    lines = []
    j = count
    while j > 0:
        i = breaks[j]
        lines.append(' '.join(words[i:j]))
        j = i
    lines.reverse()

    total_cost=0
    for i in lines:
        txt.insert(END,str('\n|'+align_spacing(i,threshold,align)+'|'+', the cost for the line is:'+str((threshold-len(i))**3)))
        total_cost+=(threshold-len(i))**3
    end = time()
    elapsed = end-start
    txt.insert(END,str('\n'+'-'*(threshold+2)))
    txt.insert(END,str('\nPage Width is: '+str(threshold)))
    txt.insert(END,str('\nThe Total Cost is: '+str(total_cost)))
    txt.insert(END,str('\nThe Execution Time is: '+secondsToStr(elapsed)+'s'))
    txt.config(state='disable')

root=Tk()
root.title('Advanced Algorithms')
root.style=ttk.Style()
root.style.theme_use("alt")
f1 = Frame(root, width=300, height=110)

Label(f1, text="Text Alignment and Printing Neatly Project for Advanced Algorithms").pack(pady=10)
f2=Frame(root,width=300,height=110)
radio_var=StringVar()
Radiobutton(f2, text='Left Alignment', value='L', variable=radio_var).pack(side=LEFT)
Radiobutton(f2, text='Center Alignment', value='C', variable=radio_var).pack(side=LEFT)
Radiobutton(f2, text='Right Alignment', value='R', variable=radio_var).pack(side=LEFT)
radio_var.set('L')
f3=Frame(root,width=300,height=110)
text = Text(f3,height=10,width=100)
text.pack(fill=Y,side=LEFT)
scroll=Scrollbar(f3)
scroll.pack(side=RIGHT,fill=Y)
scroll.config(command=text.yview)
text.config(yscrollcommand=scroll.set)
f4=Frame(root,width=300,height=110)
page_width=IntVar()
Label(f4, text="Page Width:").pack(side=LEFT)
Entry(f4, width=4, textvariable=page_width).pack(side=LEFT)
page_width.set("")
f5=Frame(root,width=300,height=110)
b1=Button(f5, text="GREEDY\nAPROACH", state=NORMAL,command=run_greedy)
b1.pack(side=LEFT)
#b1.bind('<Button-1>',run_greedy)
b2=Button(f5, text="DYNAMIC\n PROGRAMMING", state=NORMAL,command=run_dynamic)
b2.pack(side=LEFT)
b3=Button(f5, text="BRANCH\n AND BOUND", state=NORMAL,command=run_branch_and_bound)
b3.pack(side=LEFT)
b4=Button(f5, text="BRUTE\n FORCE", state=NORMAL,command=run_brute_force)
b4.pack(side=LEFT)
b5=Button(f5, text="PERSONAL\nAPPROACH", state=NORMAL,command=run_personal)
b5.pack(side=LEFT)
b6=Button(f5, text="DIVIDE\nAND CONQUER", state=NORMAL,command=run_divide_and_conqure)
b6.pack(side=LEFT)
b7=Button(f5, text="BINARY\nSEARCH", state=NORMAL,command=run_binary_search)
b7.pack(side=LEFT)
b8=Button(f5, text="SHORTEST\nPATH", state=NORMAL,command=run_shortest_path)
b8.pack(side=LEFT)
f1.pack(expand=True)
f2.pack(expand=True)
f3.pack(expand=True)
f4.pack(expand=True)
f5.pack(expand=True)
root.mainloop()
