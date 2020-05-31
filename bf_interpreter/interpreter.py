class BfPtr:
  def __init__(self):
    self.ptr = 0
    self.buffer = [0]
  
  def inc(self):
    self.ptr += 1
    
    if len(self.buffer) == self.ptr:
      self.buffer.append(0)

  def dec(self):
    self.ptr -= 1

  def p_inc(self):
    if self.deref() == 255:
      self.buffer[self.ptr] = 0
    else:  
      self.buffer[self.ptr] += 1
      
  def p_dec(self):
    if self.deref() == 0:
      self.buffer[self.ptr] = 255
    else:  
      self.buffer[self.ptr] -= 1
    
  def print(self):
    print(chr(self.deref()), end='')
    
  def input(self):
    self.buffer[self.ptr] = ord(input('\ninput: '))
  
  def deref(self):
    return self.buffer[self.ptr]  
  
  
ptr = BfPtr()

ch_map = {
  '>': ptr.inc,
  '<': ptr.dec,
  '+': ptr.p_inc,
  '-': ptr.p_dec,
  '.': ptr.print,
  ',': ptr.input
}
ch_arr = ch_map.keys()

ss = """
-,+[                         Read first character and start outer character reading loop
    -[                       Skip forward if character is 0
        >>++++[>++++++++<-]  Set up divisor (32) for division loop
                               (MEMORY LAYOUT: dividend copy remainder divisor quotient zero zero)
        <+<-[                Set up dividend (x minus 1) and enter division loop
            >+>+>-[>>>]      Increase copy and remainder / reduce divisor / Normal case: skip forward
            <[[>+<-]>>+>]    Special case: move remainder back to divisor and increase quotient
            <<<<<-           Decrement dividend
        ]                    End division loop
    ]>>>[-]+                 End skip loop; zero former divisor and reuse space for a flag
    >--[-[<->+++[-]]]<[         Zero that flag unless quotient was 2 or 3; zero quotient; check flag
        ++++++++++++<[       If flag then set up divisor (13) for second division loop
                               (MEMORY LAYOUT: zero copy dividend divisor remainder quotient zero zero)
            >-[>+>>]         Reduce divisor; Normal case: increase remainder
            >[+[<+>-]>+>>]   Special case: increase remainder / move it back to divisor / increase quotient
            <<<<<-           Decrease dividend
        ]                    End division loop
        >>[<+>-]             Add remainder back to divisor to get a useful 13
        >[                   Skip forward if quotient was 0
            -[               Decrement quotient and skip forward if quotient was 1
                -<<[-]>>     Zero quotient and divisor if quotient was 2
            ]<<[<<->>-]>>    Zero divisor and subtract 13 from copy if quotient was 1
        ]<<[<<+>>-]          Zero divisor and add 13 to copy if quotient was 0
    ]                        End outer skip loop (jump to here if ((character minus 1)/32) was not 2 or 3)
    <[-]                     Clear remainder from first division if second division was skipped
    <.[-]                    Output ROT13ed character from copy and clear it
    <-,+                     Read next character
]                            End charact
"""

def parse(ss):
  bra_idx_arr = [{'idx': 0, 'flag': True}]
  idx = 0
  
  while idx < len(ss):
    s = ss[idx]
    
    if s == '[':
      temp = {'idx': idx, 'flag': True}
      
      if ptr.deref() == 0:
        temp['flag'] = False
        
      bra_idx_arr.append(temp)
      
    elif s == ']':
      if ptr.deref() == 0:
        del bra_idx_arr[-1]
      else:
        idx = bra_idx_arr[-1]['idx']
    
    if (bra_idx_arr[-1]['flag'] 
        and s in ch_arr):
      ch_map[s]()
      
    idx += 1

print('BF code', ss)  
print('Output')
parse(ss)

