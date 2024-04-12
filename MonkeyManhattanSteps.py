import decimal


#Creates a list which appends more list but in order to represent the coordinate of each block
# and adds all the possible coordinates into the list.
def getallloc(row, col):
    list1 = []
    for r in range(row):
        for c in range(col):
            i = [r, c]
            list1.append(i)

    return list1

class LastLoc:
  def __init__(self, row, col):
    self.row = row
    self.col = col
    self.distrib = dict()

  #initially distributes the equal amount of percentage of based on number of rows times number of cols
  #Then it's stored in a dictionary with the key being the coordinate as a tuple (r,c)
  def get_distrib(self):
    for r in range(self.row):
        for c in range(self.col):
            v = 1/(self.row*self.col)
            self.distrib[(r,c)] = v
            if debug == "y":
                print("Last location: (" + str(r) +
                      ", " + str(c) + "), prob: " + str(v))

  #returns probability of last location
  def get_prob(self, loc):
      return self.distrib[loc]   

class CurrLoc:
  def __init__(self, row, col):
    self.row = row
    self.col = col
    self.distrib = dict()
    
  #The first two for loops are for the coordinates of the last location 
  def get_distrib(self):
    for r in range(self.row):
        for c in range(self.col):
            list1 = []
            if debug == "y":
                print("Last location: (" + str(r) +
                      ", " + str(c) + ")")
            loc = (r,c)
            loclist = onemanhattan(self.row, self.col, loc)
            #Then we check for all the locations one step away from the last location
            #if it's one step away from the last location then it's possible as a current location
            #and we divide the percentage based on how many possible one step locations there are
            #Each current location is added to a list along with it's probability
            #For example: [[0,0], 0.5] is what is being appended
            for p in loclist:
                val = 1/len(loclist)
                if debug == "y":
                    print(" Current location: (" + str(p[0]) +
                      ", " + str(p[1]) + "), prob: " + str(val))
                list1.append([p, val])
            self.distrib[loc] = list1
            
  def get_prob(self, loc, lastloc):
      list1 = self.distrib[lastloc]
      for x in list1:
          #We have to convert the x from list into a tuple because all locations are tuples. 
          p = x[0]    
          newtup = (p[0], p[1])
          #Check if the location has a probability or not
          if loc == newtup:
              return x[1]
          
      return 0

class Sound:
  def __init__(self, row, col):
    self.row = row
    self.col = col
    self.distrib = dict()
    

  def get_distrib(self):
    if debug == "y":
        print("Sound Distribution")
    for r in range(self.row):
        for c in range(self.col):
            list1 = []
            if debug == "y":
                print("Current Location (" + str(r) +
                      ", " + str(c) + ")")
            curr = (r,c)
            onelist = onemanhattan(self.row, self.col, curr)
            twolist = twomanhattan(self.row, self.col, curr)
            totallist = onelist + twolist
            list1.append([curr, 0.6])
            if debug == "y":
                print(" Sound reported at: (" + str(curr[0]) +
                      ", " + str(curr[1]) + "), prob: " + str(0.6))
            for p in totallist:
                if p in onelist:
                    val = 0.3/len(onelist)
                else:
                    val = 0.1/len(twolist)
                if debug == "y":
                    print(" Sound reported at: (" + str(p[0]) +
                      ", " + str(p[1]) + "), prob: " + str(val))
                list1.append([p, val])
            self.distrib[curr] = list1
            

  def get_prob(self, loc, soundloc):
      list1 = self.distrib[loc]
      for x in list1:
          p = x[0]
          newtup = (p[0], p[1])
          if soundloc == newtup:
              return x[1]
          
      return 0 
      
      
      

class MotionSensor:
  def __init__(self, row, col):
    self.row = row
    self.col = col
    self.distrib = dict()
    self.distrib1 = dict()

  def M1distrib(self):
    if debug == "y":
        print("Motion sensor #1 (top left) distribution")  
    for r in range(self.row):
        for c in range(self.col):
            loc  = [r,c]
            #if the location is in the topleft list we check how far it is from 0, 0 and multiply it by 0.1
            if loc in self.topleft():
                count = loc[0] + loc[1]
                count = 0.9 - count * 0.1
            else:
                count = 0.05
            self.distrib[(r,c)] = count 
            falseprob = 1- count
            if debug == "y":
                print("Current location: (" + str(r) + "," + str(c) + "), true prob: "+ str(count) + ", false prob: " + str(falseprob))
                
                
                

            
  def M2distrib(self):
    if debug == "y":
        print("Motion sensor #2 (bottom right) distribution")
    for r in range(self.row):
        for c in range(self.col):
            loc = [r,c]
            #if the location is in the bottomright list we check how far it is from m-1, n-1 and multiply it by 0.1
            if loc in self.bottomright():
                count = (self.row-1)-loc[0] + ((self.col-1) - loc[1])
                count = 0.9 - count * 0.1
            else:
                count = 0.05
            self.distrib1[(r,c)] = count 
            falseprob = 1- count
            if debug == "y":
                print("Current location: (" + str(r) + "," + str(c) + "), true prob: "+ str(count) + ", false prob: " + str(falseprob))

   #topleft checks all horizontal and vertical possibilities from 0,0 and adds it to a list 
  def topleft(self):
    list1 = []
    for r in range(self.row):
        list1.append([r, 0])
    for c in range(self.col):
        list1.append([0, c])
    return list1

  #topleft checks all horizontal and vertical possibilities from m-1, n-1 and adds it to a list 
  def bottomright(self):
    list1 = []
    for r in range(self.row):
        list1.append([r, self.col-1])
    for c in range(self.col):
        list1.append([self.row-1, c])
    return list1

  def get_probM1(self, loc):
      return self.distrib[loc]
    
  def get_probM2(self, loc):
      return self.distrib1[loc]
                
            




def onemanhattan(row, col, loc):
    list1 = []
    if (loc[0]+1) < row:
        v = loc[0] +1
        t = loc[1]
        p = [v, t]
        list1.append(p)
    if (loc[1]+1) < col:
        v = loc[1] +1
        t = loc[0]
        p = [t, v]
        list1.append(p)
    if (loc[0]-1) >= 0:
        v = loc[0] -1
        t = loc[1]
        p = [v, t]
        list1.append(p)
    if (loc[1]-1) >= 0:
        v = loc[1]-1
        t = loc[0]
        p = [t, v]
        list1.append(p)
    return list1

def twomanhattan(row, col, loc):
    list1 = []
    if (loc[0]+2) < row:
        list1.append([loc[0] +2, loc[1]])
    if (loc[1]+2) < col:
        list1.append([loc[0], loc[1] +2])
    if (loc[0]-2) >= 0:
        list1.append([loc[0] -2, loc[1]])
    if (loc[1]-2) >= 0:
        list1.append([loc[0], loc[1]-2])
    if (loc[0]-1) >= 0 and (loc[1] - 1) >= 0:
        list1.append([loc[0] - 1 , loc[1]-1])
    if (loc[0]+1) < row and (loc[1] - 1) >= 0:
        list1.append([loc[0] + 1 , loc[1]-1])
    if (loc[0]-1) >= 0 and (loc[1] + 1) < col:
        list1.append([loc[0] - 1 , loc[1]+1])
    if (loc[0]+1) < row and (loc[1] + 1) < col:
        list1.append([loc[0] + 1 , loc[1]+1])
            
    return list1

def normalization(problist):
    total = 0
    for p in problist:
        total += p
    for x in range(len(problist)):
        problist[x] = problist[x]/total


def main():
    global debug
    filename = input('Enter a filename: ')
    debug = input("Do you want to see the debug (y/n)? ")
    row = 0
    col = 0
    board = None
    board1 = None
    motion = None
    sound = None
    iteration  = 0
    with open(filename, 'r') as file:
        for line in file:
            line = line.rstrip()
            L = line.split(' ')
            if len(L) == 2: 
                row = int(L[0])
                col = int(L[1])
                #these get all the inital distributions from each class 
                board = LastLoc(row, col)
                board.get_distrib()
                print()
                board1 = CurrLoc(row, col)
                board1.get_distrib()
                print()
                motion = MotionSensor(row, col)
                motion.M1distrib()
                print()
                motion.M2distrib()
                print()
                sound = Sound(row, col)
                sound.get_distrib()
                print()
                
                x = 0
                print("Initial distribution of monkey's last location:")
                for r in range(row):
                    printstatement = ""
                    for c in range(col):
                        printstatement += f"    {board.distrib[r,c]:.9f} "
                        x+= 1
                    print(printstatement)
                print()
                
            else:
                    
                motion1 = "False"
                motion2 = "False"
                if(L[0] == "1"):
                    motion1 = "True"
                if(L[1] == "1"):
                    motion2 = "True"
                print("Observation: Motion1: " + motion1 + ", Motion2: " + motion2 + ", Sound location: ("+ L[2] +", " + L[3] +")")
                print("Monkey's predicted current location at time step: " + str(iteration))
                iteration += 1
                
                problist = []
                totalprob = 0
                for loc in getallloc(row, col):
                  if debug == "y":
                      print("Calculating total prob for current location (" + str(loc[0]) + ", " + str(loc[1]) + ")")
                  for lastloc in getallloc(row, col):
                      last = (lastloc[0], lastloc[1])
                      curr = (loc[0], loc[1])
                      lastprob = board.get_prob(last)
                      currprob = board1.get_prob(curr, last)
                      M1Prob = motion.get_probM1(curr)
                      M2Prob = motion.get_probM2(curr)
                      
                      if(L[0] == "0"):
                          M1Prob = 1- M1Prob
                      if(L[1] == "0"):
                          M2Prob = 1- M2Prob

                      soundloc = (int(L[2]), int(L[3]))
                      soundprob = sound.get_prob(curr, soundloc)
                      prob = lastprob * currprob  * M1Prob * M2Prob *soundprob
                      totalprob = totalprob + prob
                      if debug == "y":
                          print("   Probs being multiplied for last location (" + str(lastloc[0]) + ", " + str(lastloc[1]) + ")" + str(lastprob) + " " +  str(currprob) +" "+
                                str(M1Prob) + " " + str(M2Prob) + " " + str(soundprob))
                  problist.append(totalprob)
                  totalprob = 0

                print()
                print("Before Normalization:")
                printstatement = ""
                x = 0
                for r in range(row):
                    printstatement = ""
                    for c in range(col):
                        printstatement += f"    {problist[x]:.9f} "
                        x+= 1
                    print(printstatement)
                    
                    

                normalization(problist)

                print()
                print("After Normalization:")
                x = 0
                for r in range(row):
                    printstatement = ""
                    for c in range(col):
                        printstatement += f"    {problist[x]:.9f} "
                        x+= 1
                    print(printstatement)
                print()
                
                y = 0 
                for loc in getallloc(row, col):
                      newloc = (loc[0],loc[1])
                      board.distrib[newloc] = problist[y]
                      y += 1
            
            
            
                      

            
              
main()
    
    
        
