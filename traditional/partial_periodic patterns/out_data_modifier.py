import sys
def modify_op(file):
    outfile= file
    lines=[]
    with open(outfile, 'r') as r:
        for line in r:
            val=line.split('(', 1)[1].split(')')[0]
            z=val.split('[', 1)[1].split(']')
            pattern=z[0]+z[1]
            pattern = pattern.replace(",", "")
            lines.append(pattern)
#             r.write('%s \n'%str(pattern))
    r.close()
    with open(outfile, 'w') as f:
        for x in lines:
            f.write('%s \n'%str(x).replace("'",""))
    f.close()