

from numpy import Inf
from tabulate import tabulate


tick=0
num_frames=4
total_hit_attempt=0 #total hit attempt
number_of_hits=0 #number of hits
pages_already_used=0

class Frame:
    def __init__(self,frameid) -> None:
        self.frameid=frameid#this actually a frame not page 
        self.fix_writes=0
        self.fix_reads=0
        self.dirty=False
        self.is_frame_in_use=False #check if transactions previously happened on the page
        self.pageid=0

    def flush(self):#when buffer full, flush to get space for new page to come into frame
        self.frameid=frameid#this actually a frame not page 
        self.fix_writes=0
        self.fix_reads=0
        self.dirty=False
        self.is_frame_in_use=False #transactions previously happened on the page
        self.pageid=0    
 
 

def createPages():
    frames=[]
    for i in range(num_frames):
        frames.append(Frame(i))

    return frames

def lru(pages):
    #buffer_pool=32
    #number of pages currently in buffer
    #buffer_state=
    #print("here")
    #print(frame_command)
    #for p in frame_commands:
    #p=int(frame_commands[1])
    #if int(p not in pages):
    #    if (len(pages)==num_frames):
    #        pages.remove(pages[0])
    #        pages.append(p)
    #    else:
    #        pages.append(p)
            

    #else:
    #    pages.remove(p)
    #    pages.append(p)
    t=0
    

def lfu(frames,pageid_):
    pages_total_fix_count=float('-inf')
    lfu_frameid=0
    for f in range(frames):
        temp=frames[f].fix_writes+frames[f].fix_reads
        if pages_total_fix_count<temp:
            pages_total_fix_count=temp
            lfu_frameid=f
    
    
    frames[f].flush()#reintialize frame
    frames[f].pageid=pageid_#set frame to new page
    return frames


def mfu(pages):
    #
    t=1


def fifo(pages):
    t=1


def checkIfBufferFull(pages):
    for t in range(len(pages)):
        if pages[t].is_frame_in_use:
            continue
        else:
            return False    
    return True
#returns the index of the page searched for in the pages array
def findPageIndex(frames,searchid):#return None if not found
    for t in range(page_num):
        if frames[t].pageid==searchid:
            return t
    return None  #        

def maketable(head, data):
    num_rows=len(data)
    print("-----------------------------------------------------------------------------")
    print ("|",head[0],"|",head[1],"|",head[2],"|",head[3],"|",head[4],"|",head[5],"|")
    print("-----------------------------------------------------------------------------")
    for i in range(num_rows):
        u=data[i]
        print("|",u[0],"     |",u[1],"    |",u[2],"                |",u[3],"               |",u[4],"    |",u[5],"       |")
    
    print("-----------------------------------------------------------------------------")



def getOutstandingR_W(frames):
    number=[0,0]#position 0 is read, position 1 is writes
    for frame in frames:
        number[0]=number[0]+frame.fix_reads
        number[1]=number[1]+frame.fix_writes

    return number    

if __name__=='__main__':
    frames=createPages()
    #for y in range(num_pages):
    #    print (pages[y].pageid)
    file_obj=open("buffer_info.txt","r")
    commands=file_obj.readlines()
    initial_params=commands[0].strip().split(",")
    buffer_num=int(initial_params[1])
    page_num=int(initial_params[2])
    replacement_method=int(initial_params[3])

    #head=["Frame#","Page#","Fix Count(Writes)", "Fix Count(Reads)","Dirty","Hit Rate%"]
    #data=[["0","3","5","7","Y","70"],["8","3","5","7","Y","97"],
    #["4","9","9","9","Y","96"],["0","4","4","4","N","99"]]
    data=[]
    #maketable(head,data)
    
    head=["Frame#","Page#","Fix Count(Writes)", "Fix Count(Reads)","Dirty","Hit Rate%"]
    data.append(head)
    #loop over commans in text file
    frameid_increment=0
    for t in range(1,len(commands)):
        frame_command=commands[t].strip().split(",")
        page_id=int(frame_command[1])

        if checkIfBufferFull(frames):#check if buffer is full first
        
            if replacement_method==1:
                    #for t in range(1,len(commands)):
                    #frame_command=commands[t].strip().split(",")
                    lru(frames)
                    print(frames)
            elif replacement_method==2:
                #for t in range(1,len(commands)):
                    #frame_command=commands[t].strip().split(",")
                    frames=lfu(frames,page_id)
                
            elif replacement_method==3:
                #for t in range(1,len(commands)):
                    #frame_command=commands[t].strip().split(",")
                    mfu(frames)
                
            else:
                #for t in range(1,len(commands)):
                    frame_command=commands[t].strip().split(",")
                    fifo(frames)



        frameid=findPageIndex(frames,page_id)#find frameid of page in buffer
        if frameid==None:#existing frame with that id is not found
            total_hit_attempt+=1
            frameid_increment+=1
            current_frame=frames[frameid_increment]
            #continue#skip to next loop iteration -----no if frame not found create it
        else:
            total_hit_attempt+=1
            number_of_hits+=1
            current_frame=frames[frameid]


        
        
        hit_rate=100*number_of_hits/total_hit_attempt        

        
        current_frame.frame_in_use=True
        current_frame.pageid=page_id
    
        if current_frame.dirty:#check if page dirty before it is written to
            tick+=10
        else:
            tick+=1


        if frame_command[0]=="fix" and frame_command[2]=="write":
            current_frame.fix_writes+=1
        elif frame_command[0]=="unfix" and frame_command[2]=="write": 
            current_frame.fix_writes-=1  
        elif frame_command[0]=="fix" and frame_command[2]=="read": 
            current_frame.fix_reads+=1  
        elif frame_command[0]=="unfix" and frame_command[2]=="read": 
            current_frame.fix_reads-=1  

        #wont all pages written to become dirty if they are written to again
        if current_frame.fix_writes>0:
            current_frame.dirty=True

        current_data=[str(current_frame.frameid),str(current_frame.pageid),str(current_frame.fix_writes),str(current_frame.fix_reads),str(current_frame.dirty),str(float("{:.2f}".format(hit_rate)))]
        data.append(current_data)
        
        
        print(tabulate(data,headers='firstrow'))
        print("")
        print("")
        print("")




    r_w_num=getOutstandingR_W(frames)
    data3=[["Statistic","Values"]]
    data3.append(["Number of references",str(len(commands)-1)])
    data3.append(["Outstanding Writes",str(r_w_num[1])])
    data3.append(["Outstanding Reads",str(r_w_num[0])])
    data3.append(["Total Ticks Consumed", str(tick)])
    data3.append(["Hit Rate", str(hit_rate)])


    print(tabulate(data3,headers='firstrow'))
        #print("you")
        #maketable(head,data)        
    #data=[["0","3","5","7","Y","70"],["8","3","5","7","Y","97"],
    #    ["4","9","9","9","Y","96"],["0","4","4","4","N","99"]]
        #check if page buffer full
        
