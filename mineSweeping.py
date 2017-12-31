# Write By Sunwl
# 2017/10/19
#
# 扫雷
# 输入行号，列号确认坐标
# python 3.6.2
# 运行环境 Win，Mac
# 注意：在 Mac 环境下  需要将 78行：temp+='■' 改为  temp+='■ '否则会出现移位错误

from random import randint
from os import system

mine = 13
length = 10
OriginMatrix = [] # 保存原始地雷矩阵
NumberMatrix = [] # 保存计算后的数字矩阵
StateMatrix = []  # 保存矩阵的显示状态

# 生成地雷矩阵
for i in range(0, length):
	temp = []
	for j in range(0, length):
		temp.append('.');
	OriginMatrix.append(temp)
for i in range(0, mine):
	x = randint(0, 9)
	y = randint(0, 9)
	OriginMatrix[x][y] = '*'
del randint # randint不再使用

# 生成对应的数字矩阵
# 函数定义，该函数返回某点相邻地雷数（包括自身）
def number(x, y):
	counter = 0
	for i in [0, 1, -1]:
		for j in [0, 1, -1]:
			if x + i < 0 or x + i >= length:
				continue
			elif y + j < 0 or y + j >= length:
				continue
			elif OriginMatrix[x + i][y + j] != '*':
				continue
			else:counter += 1
	return counter

# 计算
for x in range(0, length):
	temp = []
	for y in range(0, length):
		temp.append(number(x, y))
	NumberMatrix.append(temp)
# 剔除地雷点（将其相邻地雷数设为9，表示该点为地雷）
for i in range(0, length):
	for j in range(0, length):
		if OriginMatrix[i][j] == '*':
			NumberMatrix[i][j] = 9
del OriginMatrix # 原始矩阵不再使用

# 定义一些用到的函数
# 显示函数，用于显示矩阵
def display(verdict):# verdict参数用于在挖中地雷时显示地雷
	system('cls') # 清屏
	temp = '  '
	for i in range(0, length):
		temp += (str(i) + ' ')
	print(temp)
	for i in range(0, length):
		temp = str(i)+' '
		for j in range(0, length):
			if NumberMatrix[i][j] == 9 and not verdict:
				temp += '* '
				continue
			if StateMatrix[i][j]:
				if NumberMatrix[i][j] == 0:
					temp += '  '
				else:temp += (str(NumberMatrix[i][j])+' ')
			else:
				temp += '■'
		print(temp)


# 剔除函数，用于剔除显而易见的不为地雷的位置
CheckSet = set()

def openWhile(x, y):
	if (x,y) in CheckSet:
		return
	elif NumberMatrix[x][y] > 1:
		return
	else:
		StateMatrix[x][y] = True
		CheckSet.add((x, y))
		# 与0相邻的都显示
		if NumberMatrix[x][y] == 0:
			for i in [-1, 0, 1]:
				for j in [-1, 0, 1]:
					if x + i >= 0 and x + i < length and y + j >= 0 and y + j < length:
						StateMatrix[x + i][y + j] = True
		# 迭代显示
		if x - 1 >= 0:
			openWhile(x - 1, y)
		if y - 1 >= 0:
			openWhile(x, y - 1)
		if x + 1 < length:
			openWhile(x + 1, y)
		if y + 1 < length:
			openWhile(x, y + 1)


# 判定函数，用于判断是否已经找到了全部的地雷
def estimate():
	temp=[]
	for e in StateMatrix:
		temp.append(e.copy())
	for i in range(0, length):
		for j in range(0, length):
			if NumberMatrix[i][j] == 9:
				temp[i][j] = True
	for i in range(0, length):
		for j in range(0, length):
			if not temp[i][j]:
				return True
	return False

# 下面开始游戏
# 初始化_矩阵
for i in range(0, length):
	temp=[]
	for j in range(0, length):
		temp.append(False)
	StateMatrix.append(temp)

# 游戏主要部分
while estimate():
	display(True)
	x = int(input('请输入行号:'))
	y = int(input('请输入列号:'))
	if NumberMatrix[x][y] == 9: # 挖中地雷
		display(False)
		print(' 很遗憾，你失败了!')
		print(' 游戏结束 ╮(╯﹏╰)╭')
		system('pause') # 从程序里调用“暂停”命令
		exit()
	else:# 没挖中地雷
		StateMatrix[x][y] = True
		openWhile(x, y)
		CheckSet.clear()
display(True)
print('你赢了!!! ( ^_^ )/~~')
system('pause') # 从程序里调用“暂停”命令
