import sys
sys.path.append('../board')

from Board import Board

size = int(input("size: "))
a = Board(size=size)
print(a)

row = -1
col = -1

while row or col != -1:
  print("White's Turn:")
  row = int(input("row: "))
  col = int(input("col: "))
  a.set_white((row, col))
  print("White Board: \n", a.whiteBoard, sep= '')
  print(a)
  
  print("Blacks's Turn:")
  row = int(input("row: "))
  col = int(input("col: "))
  a.set_black((row, col))
  print("Black Board: \n", a.blackBoard, sep= '')
  print(a)