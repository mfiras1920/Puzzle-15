from copy import deepcopy
import numpy as np
import time

class Puzzle15:
    
    rows = 4
    columns = 4
    arrOfKurang = []

    nodeHeight = 0
    cost = 0
    arrOfRute = []

    def __init__(self, arrPuzzle):
        self.arrPuzzle = arrPuzzle
        for i in range(self.rows):
            for j in range(self.columns):
                if(self.arrPuzzle[i][j] == 16):
                    self.emptyCell = i*10 + j

    def __eq__(self, other):
        return (self.arrPuzzle == other.arrPuzzle)

    def addRute(self, rute):
        self.arrOfRute.append(rute)

    def resetRute(self):
        self.arrOfRute.clear()

    def getHeight(self):
        return self.nodeHeight

    def setHeight(self, height):
        self.nodeHeight += height

    def getCost(self):
        return self.cost

    def setCost(self, cost):
        self.cost = cost

    def getEmptyCell(self):
        return self.emptyCell

    def getEmptyRow(self):
        return (self.emptyCell // 10)

    def getEmptyColumn(self):
        return (self.emptyCell % 10)

    def printPuzzle(self):
        for i in range (self.rows):
            for j in range (self.columns):
                if (self.arrPuzzle[i][j] != 16):
                    if(self.arrPuzzle[i][j] < 10):
                        print(" " + str(self.arrPuzzle[i][j]), end=" ")
                    else:
                        print(self.arrPuzzle[i][j], end=" ")
                else:
                    print("  ", end=" ")
            print()
        print()

    def moveUp(self):
        if(self.getEmptyRow() != 0):
            temp = self.arrPuzzle[ self.getEmptyRow() ][ self.getEmptyColumn() ]
            self.arrPuzzle[ self.getEmptyRow() ][ self.getEmptyColumn() ] = self.arrPuzzle[ (self.getEmptyRow()) - 1 ][ self.getEmptyColumn() ]
            self.arrPuzzle[ (self.getEmptyRow()) - 1 ][ self.getEmptyColumn() ] = temp
            self.emptyCell -= 10

    def moveDown(self):
        if(self.getEmptyRow() != 3):
            temp = self.arrPuzzle[ self.getEmptyRow() ][ self.getEmptyColumn() ]
            self.arrPuzzle[ self.getEmptyRow() ][ self.getEmptyColumn() ] = self.arrPuzzle[ (self.getEmptyRow()) + 1 ][ self.getEmptyColumn() ]
            self.arrPuzzle[ (self.getEmptyRow()) + 1 ][ self.getEmptyColumn() ] = temp
            self.emptyCell += 10

    def moveLeft(self):
        if(self.getEmptyColumn() != 0):
            temp = self.arrPuzzle[ self.getEmptyRow() ][ self.getEmptyColumn() ]
            self.arrPuzzle[ self.getEmptyRow() ][ self.getEmptyColumn() ] = self.arrPuzzle[ self.getEmptyRow() ][ self.getEmptyColumn() - 1 ]
            self.arrPuzzle[ self.getEmptyRow() ][ self.getEmptyColumn() - 1 ] = temp
            self.emptyCell -= 1

    def moveRight(self):
        if(self.getEmptyColumn() != 3):
            temp = self.arrPuzzle[ self.getEmptyRow() ][ self.getEmptyColumn() ]
            self.arrPuzzle[ self.getEmptyRow() ][ self.getEmptyColumn() ] = self.arrPuzzle[ self.getEmptyRow() ][ self.getEmptyColumn() + 1 ]
            self.arrPuzzle[ self.getEmptyRow() ][ self.getEmptyColumn() + 1 ] = temp
            self.emptyCell += 1

    def kurang(self):
        temp = np.array(self.arrPuzzle)
        temp = temp.flatten()
        for i in range(0, 16):
            count = 0
            for j in range(i+1, 16):
                if(temp[i] > temp[j]):
                    count += 1
            self.arrOfKurang.insert(i, count)
    
    def sumOfKurang(self):
        sum = 0
        for i in range(16):
            sum += self.arrOfKurang[i]
        return sum

    def printArrOfKurang(self):
        self.kurang()
        temp = np.array(self.arrPuzzle)
        temp = temp.flatten()
        for i in range(0,16):
            print(str(temp[i]) + " , kurang(" + str(temp[i]) + "): " + str(self.arrOfKurang[i]))
        print()

    def KurangX(self):
        X = (self.getEmptyRow() + self.getEmptyColumn()) % 2
        sumX = self.sumOfKurang() + X
        return sumX

def cost(P, Goal):
    count = 0
    for i in range(4):
        for j in range(4):
            if (P.arrPuzzle[i][j] != Goal.arrPuzzle[i][j]):
                count += 1
    return (P.nodeHeight + count)
    
def insertPrio(Q, P):
    for i in range(len(Q)):
        if(Q[i].getCost() > P.getCost()):
            Q.insert(i, P)
            return
    Q.append(P)


def isEqual(P, Q):
    for i in range(len(Q)):
        if (P == Q[i]):
            return True
    return False

NULL = 16
Goal = Puzzle15([[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,NULL]])

fileFound = False
while not(fileFound):
    try:
        file = input("Masukkan nama file: ")
        ins = open( file, "r" )
        data = []
        for line in ins:
            number_strings = line.split()
            numbers = [int(n) for n in number_strings]
            data.append(numbers)
        ins.close()
        fileFound = True
    except FileNotFoundError:
        print("File tidak ditemukan!")
        print()

Puzzle = Puzzle15(data)
# Puzzle = Puzzle15([[1,2,3,4],[5,6,7,8],[9,NULL,10,11],[13,14,15,12]])
# Puzzle = Puzzle15([[1,2,3,4],[5,6,NULL,12],[9,10,8,7],[13,14,11,15]])
# Puzzle = Puzzle15([[1,2,3,NULL],[5,6,7,15],[9,10,8,4],[13,14,12,11]])

print("Posisi awal:")
Puzzle.printPuzzle()

print("Kurang(i) untuk setiap ubin:")
Puzzle.printArrOfKurang()

print("Kurang(i) + X = " + str(Puzzle.KurangX()))
print()

if ((Puzzle.KurangX() % 2) == 1):
    print("Karena Kurang(i) + X adalah ganjil, maka persoalan tidak dapat diselesaikan")

else:
    startTime = time.time() # Waktu mulai

    allQueue = []       # Total simpul yang dibangkitkan
    Queue = []
    i = 1

    Queue.append(Puzzle)
    allQueue.append(Puzzle)

    while(Queue[0] != Goal):
        current = Queue.pop(0)

        up = deepcopy(current)
        up.arrOfRute = deepcopy(current.arrOfRute)
        up.moveUp()
        if(not(isEqual(up, allQueue))):          # Mengecek apakah simpul sudah pernah dibangkitkan
            up.setHeight(i)
            up.setCost(cost(up, Goal))
            up.addRute('up')
            insertPrio(Queue, up)
            insertPrio(allQueue, up)

        down = deepcopy(current)
        down.arrOfRute = deepcopy(current.arrOfRute)
        down.moveDown()
        if(not(isEqual(down, allQueue))):       # Mengecek apakah simpul sudah pernah dibangkitkan
            down.setHeight(i)
            down.setCost(cost(down, Goal))
            down.addRute('down')
            insertPrio(Queue, down)
            insertPrio(allQueue, down)

        left = deepcopy(current)
        left.arrOfRute = deepcopy(current.arrOfRute)
        left.moveLeft()
        if(not(isEqual(left, allQueue))):       # Mengecek apakah simpul sudah pernah dibangkitkan
            left.setHeight(i)
            left.setCost(cost(left, Goal))
            left.addRute('left')
            insertPrio(Queue, left)
            insertPrio(allQueue, left)

        right = deepcopy(current)
        right.arrOfRute = deepcopy(current.arrOfRute)
        right.moveRight()
        if(not(isEqual(right, allQueue))):      # Mengecek apakah simpul sudah pernah dibangkitkan
            right.setHeight(i)
            right.setCost(cost(right, Goal))
            right.addRute('right')
            insertPrio(Queue, right)
            insertPrio(allQueue, right)

    endTime = time.time() # Waktu akhir

    executionTime = (endTime-startTime)*1000000.00

    langkah = 1
    print("Langkah penyelesaian persoalan:")
    for j in Queue[0].arrOfRute:
        print("Langkah " + str(langkah) + ":")
        if(j == "up"):
            Puzzle.moveUp()
            Puzzle.printPuzzle()
        elif(j == "down"):
            Puzzle.moveDown()
            Puzzle.printPuzzle()
        elif(j == "left"):
            Puzzle.moveLeft()
            Puzzle.printPuzzle()
        elif(j == "right"):
            Puzzle.moveRight()
            Puzzle.printPuzzle()
        langkah += 1

    print("Banyak simpul yang dibangkitkan: " + str(len(allQueue)))
    print("Waktu eksekusi program: " + str(round((executionTime),4)) + " mikrosekon")