n,m=map(int,input().split())
fl=[]
a,b=0,1
while b<=m:
    if b>=n:fl.append(b)
    a,b=b,a+b
if len(fl)>0:
    print(*fl)
else:print("В заданном диапазоне нет чисел Фибоначчи")
