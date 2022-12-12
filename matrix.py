import numpy as np
import math
import curses
from torch import initial_seed 

# l = [[1,2,3],[2,3,4],[5,6,7]]
# M = np.array(l)
# inv = np.linalg.inv(M)
# # print("MATRIX \n",M)
# # print("INVERSE \n",inv)
# # print("TEST  :  (M times its inv) \n",np.dot(M,inv))
# m = np.array([[1,2,3],[2,3,4],[1,2,1]]);print(m,"\n")
# n = np.array([[1,2,1]]).T;print(n,"\n")
# print(m/n)
def menu(title, classes, color='white'):
  # define the curses wrapper
  def character(stdscr,):
    attributes = {}
    # stuff i copied from the internet that i'll put in the right format later
    icol = {
      1:'red',
      2:'green',
      3:'yellow',
      4:'blue',
      5:'magenta',
      6:'cyan',
      7:'white'
    }
    # put the stuff in the right format
    col = {v: k for k, v in icol.items()}

    # declare the background color

    bc = curses.COLOR_BLACK

    # make the 'normal' format
    curses.init_pair(1, 7, bc)
    attributes['normal'] = curses.color_pair(1)


    # make the 'highlighted' format
    curses.init_pair(2, col[color], bc)
    attributes['highlighted'] = curses.color_pair(2)


    # handle the menu
    c = 0
    option = 0
    while c != 10:

        stdscr.erase() # clear the screen (you can erase this if you want)

        # add the title
        stdscr.addstr(f"{title}\n", curses.color_pair(1))

        # add the options
        for i in range(len(classes)):
            # handle the colors
            if i == option:
                attr = attributes['highlighted']
            else:
                attr = attributes['normal']
            
            # actually add the options

            stdscr.addstr(f'> ', attr)
            stdscr.addstr(f'{classes[i]}' + '\n', attr)
        c = stdscr.getch()

        # handle the arrow keys
        if c == curses.KEY_UP and option > 0:
            option -= 1
        elif c == curses.KEY_DOWN and option < len(classes) - 1:
            option += 1
    return option
  return curses.wrapper(character)



#////////////////  JACOBI METHORD ///////////////////////

def Lets_run():
    global n
    n = menu("CHOOSE A METHORD : ",["1. JACOBI","2. GOSS SEIN"],'blue')
    if n==0:
        jacobi_run()
    elif n==1:
        GossSein_run()

    

class Jacobin():
    def __init__(self,matrix1,var_matrix,delta,d):
        self.matrix1 = matrix1
        self.var_matrix = var_matrix
        self.delta = delta
        self.d = d
    def cal(self):
        T = self.matrix1*self.var_matrix #; print("T:\n",T)
        L =[T[i,i] for i in range(0,3)]#; print("L :\n",L)
        T = np.array(T).T/np.array(L)
        delta = self.delta/np.array(L) #; print("DELTA\n",delta)
        S=[]
        for i in range(3):
            S.append([np.array(T).T[i,j] for j in range(3) if j!=i])
        S = np.array(S)
        #print("S:\n",S)
        l = S[:,0]+S[:,1]
        #print("l:\n",l)
        self.new_vals = delta-l#;print(self.new_vals)
        #return new_vals  

    def cal2(self):
        x=0
        self.output = []
        for i in range(len(self.var_matrix)):
            # print(self.var_matrix[i])
            # print("INITIAL: \n",self.var_matrix)
            r = self.matrix1[x,:]*np.array(self.var_matrix[i])#; print(r)
            rhs = self.delta[x]/r[x];# print(rhs)
            l = np.array(r)/r[x] #print(l)
            S =[np.array(l)[i]for i in range(len(l)) if x!=i ]
            f = rhs - (S[0]+S[1]) #; print(f)
            self.output.append(f)
            #print(self.d)
            L = list(self.d.keys())
            self.d[L[x]] = f
            #print(self.d)
            self.var_matrix = np.array([[1,self.d["y"],self.d["z"]],[self.d["x"],1,self.d["z"]],[self.d["x"],self.d["y"],1]])
            #print(self.var_matrix)
            x+=1
        return self.output


    def update(self):
            x=0
            for i in self.d:
                if n == 0:
                    self.d[i]= self.new_vals[x]
                else:
                    self.d[i]= self.output[x]
                x+=1
            #print(self.d)
            return self.d
        



def jacobi_run():
    matrix_main = np.array([eval(input(f"ENTER COEFFICIENT FOR EQ {i+1} : ")) for i in range(3)])
    delta = np.array(eval(input("Enter the RHS of the equations as a list : ")))
    d={}
    for i in ["x","y","z"]:d[f"{i}"]= 0
    initial_m = np.array([[1,d["y"],d["z"]],[d["x"],1,d["z"]],[d["x"],d["y"],1]])
    for i in range (int(input("ENTER THE NUMBER OF ITERATIONS : "))):
        #print("d ////// = \n ",d)
        D1=d.copy()
        s1=Jacobin(matrix_main,initial_m,delta,d)
        s1.cal()
        d=s1.update()
        initial_m = np.array([[1,d["y"],d["z"]],[d["x"],1,d["z"]],[d["x"],d["y"],1]])#;print(initial_m)
        #print(np.array(list(d.values())),"\n",np.array(list(D1.values())),"\n")
        error  =  np.absolute(np.array(list(d.values())) - np.array(list(D1.values())))

        print("THE ERROR IS : \n",error)

    print("\nFINAL OUTPUT \n",np.array(list(d.values())))

def GossSein_run():
    matrix_main = np.array([eval(input(f"ENTER COEFFICIENT FOR EQ {i+1} : ")) for i in range(3)])
    delta = np.array(eval(input("Enter the RHS of the equations as a list : ")))
    d={}
    for i in ["x","y","z"]:d[f"{i}"]= 0
    initial_m = np.array([[1,d["y"],d["z"]],[d["x"],1,d["z"]],[d["x"],d["y"],1]])
    D1 = list(d.values())
    for i in range (int(input("ENTER THE NUMBER OF ITERATIONS : "))):
        s1 = Jacobin(matrix_main,initial_m,delta,d)
        L = s1.cal2()
        d = s1.update()
       # print(d)
        initial_m = np.array([[1,d["y"],d["z"]],[d["x"],1,d["z"]],[d["x"],d["y"],1]])
        error = np.absolute(np.array(L) - np.array(D1))
        D1 = L
        print("THE ERROR IS : \n",error)
    print("\nFINAL OUTPUT \n",np.array(L))





if __name__=='__main__':
    Lets_run()







