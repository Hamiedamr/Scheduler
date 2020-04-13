class process:
    def __init__(self, pid, at, bt):
        self.pid=pid
        self.arrival=at
        self.burst=bt
chart = []

def SJF(plist, n, preemp):
    global chart
    queue=[]
    time=0   
    ap=0    #arrival process
    rp=0    #ready process
    done=0  #done processss
    
    if not preemp:
        while(done<n):
            for i in range(ap,n):
                if time>=plist[i].arrival:    
                    queue.append(plist[i])
                    ap+=1    
                    rp+=1    
            if rp<1:
                time+=1
                chart.append(0)
                continue
                
            queue.sort(key=lambda x: (x.burst, x.arrival))
                
            if queue[0].burst>0:
                for g in range (queue[0].burst):
                    chart.append(queue[0].pid)
                time+=queue[0].burst
                queue[0].burst=99999999
                done+=1
                rp-=1
         
    else: 
        while(done<n):
            for i in range (ap,n):
                if time>=plist[i].arrival:    
                    queue.append(plist[i])
                    ap+=1
                    rp+=1 
            if rp<1:
                time+=1
                chart.append(0)
                continue
                
            queue.sort(key=lambda x:(x.burst,x.arrival))
                
            if queue[0].burst>0:
                chart.append(queue[0].pid)
                time+=1
                queue[0].burst-=1
                if queue[0].burst<1:
                    queue[0].burst=99999999
                    done+=1
                    rp-=1
plist=[]
plist.append(process(1,1,2))
plist.append(process(1,4,4))
plist.append(process(3,4,7))
plist.append(process(7,5,4))

SJF(plist,len(plist),1)
print(chart)
