import Board

size = int(input("size: "))
a = Board.Board(size=size)
print(a)

row = -1
col = -1

while row or col != -1:
  print("White's Turn:")
  row = int(input("row: "))
  col = int(input("col: "))
  a.playWhite(row= row, col= col)
  print("White Board: \n", a.printWhite(), sep= '')
  print(a)
  
  print("Blacks's Turn:")
  row = int(input("row: "))
  col = int(input("col: "))
  a.playBlack(row= row, col= col)
  print("Black Board: \n", a.printBlack(), sep= '')
  print(a)