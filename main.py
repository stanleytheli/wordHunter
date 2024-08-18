#inclusive
minLength = 4
maxLength = 9

#settings for printing out to console
wordsPerRow = 5
spaceBetween = 14

#TODO Generalize to be able to handle 5x5 grids

#path to get files
PATH = "C:/Users/stanl/OneDrive/Desktop/python programs/wordHunter/"

#clear file
lengthFilteredWords = open(PATH + "lengthFilteredWords.txt", "w")
lengthFilteredWords.write("")
lengthFilteredWords.close()

#filters out words that are too short or too long
words = open(PATH + "words.txt", "r")
lengthFilteredWords = open(PATH + "lengthFilteredWords.txt", "a")

for word in words:
  if len(word) >= minLength+1 and len(word) <= maxLength+1: # the +1's are because \n is considered a character
    lengthFilteredWords.write(word)
    
words.close()
lengthFilteredWords.close()

#
#  0   1   2   3
#  4   5   6   7
#  8   9  10  11
# 12  13  14  15
#

# we could write some code to calculate the neighbors grid, but there are quite literally more edge cases than not for a 4x4 grid, so I find it easier to just do this manually...
neighbors = [
  [1, 4, 5], #0
  [0, 2, 4, 5, 6], #1
  [1, 3, 5, 6, 7], #2
  [2, 6, 7], #3

  [0, 1, 5, 8, 9], #4
  [0, 1, 2, 4, 6, 8, 9, 10], #5
  [1, 2, 3, 5, 7, 9, 10, 11], #6
  [2, 3, 6, 10, 11], #7

  [4, 5, 9, 12, 13], #8
  [4, 5, 6, 8, 10, 12, 13, 14], #9
  [5, 6, 7, 9, 11, 13, 14, 15], #10
  [6, 7, 10, 14, 15], #11

  [8, 9, 13], #12
  [8, 9, 10, 12, 14], #13
  [9, 10, 11, 13, 15], #14
  [10, 11, 14] #15
]

#get input
#input format: 16 letters like "WNELSMFLIENSXRTY"
letters = []
for letter in input(">>"):
  letters.append(letter.upper())

containsLetter = {
  "A": 0,
  "B": 0,
  "C": 0,
  "D": 0,
  "E": 0,
  "F": 0,
  "G": 0,
  "H": 0,
  "I": 0,
  "J": 0,
  "K": 0,
  "L": 0,
  "M": 0,
  "N": 0,
  "O": 0,
  "P": 0,
  "Q": 0,
  "R": 0,
  "S": 0,
  "T": 0,
  "U": 0,
  "V": 0,
  "W": 0,
  "X": 0,
  "Y": 0,
  "Z": 0,
}

#creates letter matrix
for letter in letters:
    containsLetter[letter] = containsLetter[letter] + 1

#clears file
letterFilteredWords = open(PATH + "letterFilteredWords.txt", "w")
letterFilteredWords.write("")
letterFilteredWords.close()

#filters out words that require letters impossible to obtain with given board
lengthFilteredWords = open(PATH + "lengthFilteredWords.txt", "r")
letterFilteredWords = open(PATH + "letterFilteredWords.txt", "a")

for word in lengthFilteredWords:
  add = True
  letterMatrix = containsLetter.copy()
  
  for letter in word:
    if letter != "\n":
      letterMatrix[letter] = letterMatrix[letter] - 1
      if letterMatrix[letter] == -1:
        add = False
        break
  
  if add:
    letterFilteredWords.write(word)

lengthFilteredWords.close()
letterFilteredWords.close()

#now let's find which words have a valid path

#recursive function to evaluate whether valid path is possible
def isPossible(currentIndex, ifOccupied, remainingString):
  occupiedList = ifOccupied.copy()
  occupiedList[currentIndex] = len(remainingString)+1
  
  if len(remainingString) == 1:
    for neighbor in neighbors[currentIndex]:
      if letters[neighbor] == remainingString[0] and ifOccupied[neighbor] == 0:
        occupiedList[neighbor] = 1
        return [True, occupiedList]
        
  else:
    for neighbor in neighbors[currentIndex]:
      if letters[neighbor] == remainingString[0] and ifOccupied[neighbor] == 0:
        condition = isPossible(neighbor, occupiedList, remainingString[1:])
        if condition[0]:
          return condition

  return [False]

#clears file
possibleWords = []

letterFilteredWords = open(PATH + "letterFilteredWords.txt", "r")

for word in letterFilteredWords:
  word = word[:-1] #removes the \n
  #keeps track of which spaces already taken
  occupied = [0] * 16 
  for i in range(16):
    if word[0] == letters[i]:
      newOccupied = occupied.copy()
      newOccupied[i] = len(word)+1
      condition = isPossible(i, newOccupied, word[1:])
      
      if condition[0]:
        r = condition[1]
        for i in range(len(r)):
          if (r[i] != 0):
            r[i] = str(len(word) - r[i] + 1)
          else:
            r[i] = "/"
        possibleWords.append([word, r[0] + r[1] + r[2] + r[3], r[4] + r[5] + r[6] + r[7], r[8] + r[9] + r[10] + r[11], r[12] + r[13] + r[14] + r[15]])

letterFilteredWords.close()

#sorts by most points first
possibleWords.sort(key=lambda s: 10-len(s[0]))

#removes duplicates
newList = []
for i in range(len(possibleWords)):
  contains = False
  plural = False
  for j in range(len(newList)):
    if possibleWords[i][0] == newList[j][0]:
      contains = True
    #if possibleWords[i][0] == newList[j][0][:-1]:
    #  contains = True
    #  newList[j][0] = newList[j][0] + "+"
    
  if not contains:
    newList.append(possibleWords[i])
possibleWords = newList.copy()

#displaying
def spacePrint(list, space):
  for item in list:
    print(item,end="")
    for i in range(space - len(item)):
      print(" ",end="")
  print("")

for i in range(int(len(possibleWords)/wordsPerRow)):
  print(str(i+1) + ".")
  for j in range(wordsPerRow):
    printList = []
    for k in range(wordsPerRow):
      printList.append(possibleWords[wordsPerRow*i+k][j])
    spacePrint(printList, spaceBetween)
  print("")
