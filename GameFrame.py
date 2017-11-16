from Tkinter import *
import ttk
import tkFont
from PIL import ImageTk
import winsound
import time
import random
import MySQLdb
from time import gmtime, strftime


# Main Frame which asks user to start a New Game or Load Game
class MyFirstGUI:

    def __init__(self, master):

        self.head = tkFont.Font(family='Comic Sans MS', size=20, weight=tkFont.BOLD)        #Font for heading
        self.cont = tkFont.Font(family='Calibri', size=18, weight=tkFont.BOLD)              #Font for Content
        self.game = tkFont.Font(family='Comic Sans MS', size=12, weight=tkFont.BOLD)        #Font for Game Frame
        self.loadFont = tkFont.Font(family='Calibri', size=12, weight=tkFont.BOLD)          # Font for Game Frame
        self.Lev1 = [0,0,0,0,0,0,0] #[apple,apple,smiley,smiley,watch,watch]                #Tracker for Level 1
        self.OneLastActive=-1                                                               #Tracker for last unmatched image
        self.OneDone = [0,0,0,0,0,0] #[apple,apple,smiley,smiley,watch,watch]               #Tracker for Level 1 completion

        self.qtb = ImageTk.PhotoImage(file='images/quitb.png')
        self.qtr = ImageTk.PhotoImage(file='images/quitr.png')
        self.apple = ImageTk.PhotoImage(file='images/apple.png')
        self.smiley = ImageTk.PhotoImage(file='images/smiley.png')
        self.watch = ImageTk.PhotoImage(file='images/watch.png')
        self.question = ImageTk.PhotoImage(file='images/question.png')
        self.done = ImageTk.PhotoImage(file='images/done.png')
        self.imageArr = [self.apple,self.apple,self.smiley,self.smiley,self.watch,self.watch,self.question,self.done]
        self.load = False
        self.root = master
        self.randomBt = []
        self.master = master
        master.title("Memory Tiles")
        master.geometry("500x300")

        self.label = Label(master, text="Welcome To Memory Tile Game",font=self.head,fg ='blue',borderwidth = 2,relief='solid',padx=4,pady=4)
        self.label.pack(pady=8)

        #New Game Option Button
        self.new_button = Button(master, text="Start New Game", bg='white',command=self.create_Level1,font=self.cont,fg='red', borderwidth=5,relief='solid')
        self.new_button.pack(pady=8)
        self.new_button.bind("<Enter>", lambda event, h= self.new_button:h.configure(bg='black',fg='white'))
        self.new_button.bind("<Leave>", lambda event, h=self.new_button: h.configure(bg='white', fg='red'))


        #Load Game Option Button
        self.load_button = Button(master, text="Load Game",bg='white', font=self.cont,command=self.LoadGame,fg='red',borderwidth=5,relief='solid')
        self.load_button.pack(pady=8)
        self.load_button.bind("<Enter>", lambda event, h=self.load_button: h.configure(bg='black', fg='white'))
        self.load_button.bind("<Leave>", lambda event, h=self.load_button: h.configure(bg='white', fg='red'))

        #Close Game Option Button
        self.close_button = Button(master, font=self.cont,image=self.qtb, command=master.quit,fg='red')
        self.close_button.pack(pady=8)
        self.close_button.bind("<Enter>", lambda event, h=self.close_button: h.configure(image=self.qtr))
        self.close_button.bind("<Leave>", lambda event, h=self.close_button: h.configure(image=self.qtb))

    #Creates First Level
    def create_Level1(self):
        #Set The Level Descriptors
        self.Lev1 = [0, 0, 0, 0, 0, 0, 0]  # [apple,apple,smiley,smiley,watch,watch]
        self.OneLastActive = -1
        if self.load == False:
            self.OneDone = [0, 0, 0, 0, 0, 0]  # [apple,apple,smiley,smiley,watch,watch]

        #New Frame
        top = Toplevel()
        top.title("Level One")
        top.geometry("500x650")
        label = Label(top, text="Try To Memorise The Tiles\n It will disappear after 5 seconds", font=self.game, fg='blue', borderwidth=2,relief='solid', padx=4, pady=4)
        label.grid(row=0,sticky=W+E,columnspan=3)

        #Button Definitions
            #Apple Button
        ap1 = Button(top,bg='white',image=self.apple,fg='red',borderwidth=5,relief='solid',)
        ap2 = Button(top, bg='white',image=self.apple, fg='red', borderwidth=5, relief='solid')

            #Smiley Button
        sm1 = Button(top, bg='white',image=self.smiley, fg='red', borderwidth=5, relief='solid')
        sm2 = Button(top, bg='white',image=self.smiley, fg='red', borderwidth=5, relief='solid')

            #Watch Button
        wt1 = Button(top,bg='white',image=self.watch,fg='red',borderwidth=5,relief='solid')
        wt2 = Button(top, bg='white',image=self.watch, fg='red', borderwidth=5, relief='solid')

        # Layout
            #Randomise images

        btnArray = [ap1, ap2, sm1, sm2, wt1, wt2]

        if self.load == False :
            self.randomBt = range(len(btnArray))
            random.shuffle(self.randomBt)
        else :
            self.load = False

            #Place the buttons in the grid
        for i in range(len(self.randomBt)):
            btnArray[self.randomBt[i]].grid(row=int(i/3)+1,column=i%3,padx=5,pady=5)


        #Some extra task
        self.temp = btnArray
        self.tempLabl = label

        #Next Level Button
        next_button = Button(top, text="Next Level", state=DISABLED, bg='white', command=top.destroy, font=self.cont,
                             fg='green', borderwidth=5, relief='solid')

        #Event Handling
        ap1.bind("<Button-1>",lambda event, obj=ap1:self.OneHandle(0, btnArray,sucLabel,next_button))
        ap2.bind("<Button-1>", lambda event, obj=ap2:self.OneHandle(1, btnArray,sucLabel,next_button))

        sm1.bind("<Button-1>", lambda event, obj=sm1:self.OneHandle(2, btnArray,sucLabel,next_button))
        sm2.bind("<Button-1>", lambda event, obj=sm2:self.OneHandle(3, btnArray,sucLabel,next_button))

        wt1.bind("<Button-1>", lambda event, obj=wt1:self.OneHandle(4, btnArray,sucLabel,next_button))
        wt2.bind("<Button-1>", lambda event, obj=wt2:self.OneHandle(5, btnArray,sucLabel,next_button))


        #Success and Exit
        sucLabel = Label(top, text="Keep Trying :)", font=self.game, fg='blue', borderwidth=2,relief='solid', padx=4, pady=4)
        sucLabel.grid(row=4,sticky=W+E,columnspan=3)
        exit_button = Button(top, text="Exit", bg='white', command=top.destroy, font=self.cont,fg='red', borderwidth=5, relief='solid')
        save_button = Button(top, text="Save Game", bg='white', command=self.saveGame, font=self.cont,
                             fg='green', borderwidth=5, relief='solid')
        next_button.grid(row=5,sticky=W+E,columnspan=3,pady=5)
        save_button.grid(row=6, sticky=W + E, columnspan=3, pady=5)
        exit_button.grid(row=7,sticky=W+E,columnspan=3,pady=5)

        root.after(5000, self.setImage)

    #Function to Set image
    def setImage(self):
        print(self.OneDone)
        for i in range(len(self.temp)):
            if self.OneDone[i] == 1:
                self.temp[i].configure(image=self.done)
            else:
                self.temp[i].configure(image=self.question)
        self.tempLabl.configure(text='Level One')

    #Save Game Functionality
    def saveGame(self):
        dtime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        db = MySQLdb.connect("localhost", "root", "", "game")
        cursor = db.cursor()
        sql = "SELECT MAX(id) FROM snapshot;"
        cursor.execute(sql)
        row = cursor.fetchone()
        id1 = int(row[0]) + 1
        id =  "'" + str(id1) + "'"
        done = "'" + ''.join(str(e) for e in self.OneDone)+"'"
        config = "'"+''.join(str(e) for e in self.randomBt)+"'"
        dtime = "'" + dtime + "'"
        level = "'1'"
        sql = "INSERT INTO snapshot VALUES ("+id+", "+level+", "+dtime+", "+done+", "+config+");"
        print(sql)
        cursor.execute(sql)
        db.commit()



    #Event Handler for Level One
    def OneHandle(self,num,btnArray,sucLabel,next):
        if(num%2==1):
            other=num-1
        else:
            other=num+1

        #Other is the button with same image as num
        print("Button Clicked ")
        print("Num : "+str(num))
        print("Other : "+str(other))

        #Check If Presed Button is Already Matched
        if(self.OneDone[num]==1 and self.OneDone[other]==1):
            return

        #Set the Current Cliked Button as Marked
        self.Lev1[num]=1;

        #Check if no other button is previously clicked
        if(self.OneLastActive == -1):
            self.OneLastActive=num
            #Set Actual Image
            btnArray[num].configure(image=self.imageArr[num])
        else:
            if(self.OneLastActive == other):
                self.OneDone[num] = self.OneDone[other]=1
                self.OneLastActive=-1
                # Set Tick Image to Both
                btnArray[num].configure(image=self.imageArr[7])
                btnArray[other].configure(image=self.imageArr[7])
                winsound.PlaySound("sounds/success.wav",winsound.SND_FILENAME)
                #The above code refers to event when user's succed to pair the tiles

            else:
                self.Lev1[num]=0
                self.Lev1[self.OneLastActive]=0
                btnArray[self.OneLastActive].configure(image=self.imageArr[6])
                self.OneLastActive = -1
                #Set Question Mark To Both

                btnArray[num].configure(image=self.imageArr[6])
                btnArray[other].configure(image=self.imageArr[6])
                winsound.PlaySound("sounds/wrong.wav",winsound.SND_FILENAME)
                # The above code refers to event when user fails to pair the tiles

            #Here check if Level One is Completed or not
            checker = True
            for i in range(len(self.OneDone)):
                if(self.OneDone[i]!=1):
                    checker=False
            if(checker):
                sucLabel.configure(fg='green')
                sucLabel.configure(text='Congratulations !! You Cleared this Level ')
                next.configure(state=NORMAL)

    #handleSelect
    def handleSelect(self,list1):
        print("Selection Made");
        index = int(list1.curselection()[0])
        value = list1.get(index)
        words = value.split();
        id = int(words[2])
        print("Selected - > ")
        print(id)
        db = MySQLdb.connect("localhost", "root", "", "game")
        cursor = db.cursor()
        sql = "SELECT * FROM snapshot WHERE id='"+str(id)+"';"
        try:
            cursor.execute(sql)
            results = cursor.fetchone()
            done = results[3]
            conf = results[4]
            print(done)
            print(conf)
            done1 = list(done);
            conf1 = list(conf);
            for i in range(len(done1)):
                print("Doing ")
                self.OneDone[i] = int(done1[i])
                self.randomBt[i]= int(conf1[i])
            print(self.OneDone)
            self.load = True
        except Exception, e:
            print('Failed to Load Game: ' + str(e))


    #Load Game Functionalit
    def LoadGame(self):
        print("Loading ..... ")
        db = MySQLdb.connect("localhost", "root", "", "game")
        print("Connected")

        # prepare a cursor object using cursor() method
        cursor = db.cursor()

        sql = "SELECT * FROM snapshot;"
        try:
            # Execute the SQL command
            cursor.execute(sql)
            # Fetch all the rows in a list of lists.
            results = cursor.fetchall()
            #Create a Frmae and listbox
            top = Toplevel()
            top.title("Load Game")
            top.geometry("500x550")
            label = Label(top, text="Select Game To Load", font=self.game,
                          fg='blue', borderwidth=2, relief='solid', padx=4, pady=4)
            label.pack(padx=5,pady=5)

            gameList = Listbox(top,font=self.loadFont,width=50)
            for row in results:
                onerow = ""
                game_id = row[0]
                level = row[1]
                date = row[2]
                # Now print fetched result
                onerow = "Id -> " + str(game_id) + " || " + "Level -> "+str(level) + " || " + "Date -> "+str(date)
                print(onerow)
                gameList.insert(END, onerow)
            self.OneDone = [0,0,0,0,0,0]
            self.randomBt = [0,0,0,0,0,0]
            gameList.bind("<<ListboxSelect>>",lambda event, obj=gameList:self.handleSelect(gameList))
            gameList.pack(padx=5, pady=5)
            load_button = Button(top, text="Load", bg='white', command=self.create_Level1, font=self.cont, fg='red',
                                 borderwidth=5, relief='solid')
            load_button.pack(padx=5,pady=5)
        except Exception, e:
                print('Failed to upload to ftp: '+ str(e))


        # disconnect from server
        db.close()


root = Tk()
my_gui = MyFirstGUI(root)
root.mainloop()