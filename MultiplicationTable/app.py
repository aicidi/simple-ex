printt = lambda x: print(x, end='')

def draw_bar():
    printt('|')

def end_line():
    print()    

def start_line():
    draw_bar()

def gugu(x, i):
    printt(' {} X {} = {:2} '.format(x, i, x * i)) 
    
def gugu_print(gu_arr, num):
    for i in range(1, num):
        start_line()
        
        for j in gu_arr:
            gugu(j, i)
            draw_bar()
            
        end_line()

def draw_gugu_table(start, end, num, table_size):
    ttk = list(range(start, end))
    tt = range(start, end, table_size)
    
    for idx in range(len(tt)):
        tkx = ttk[idx * table_size : (idx + 1) * table_size]
        
        gugu_print(tkx, num)
        end_line()

def main():
    start = int(input('start gu: '))
    end = int(input('end gu: ')) + 1
    num = int(input('count gu: ')) + 1
    table_size = int(input('table size: '))
    
    draw_gugu_table(start, end, num, table_size)

main()
