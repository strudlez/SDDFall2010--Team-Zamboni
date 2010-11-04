def coords_to_vertex(x,y):
    letters = [chr(a) for a in range(ord('A'),ord('U'))]
    if x < 8:
    	return letters[x]+str(y)
    if x >= 8:
	return letters[(x+1)]+str(y)
def vertex_to_coords(vertex):
    if ord(vertex[0]) < 74:
    	x = ord(vertex[0])-ord('A')+1
    else:
	x = ord(vertex[0])-ord('A')
    y = int(vertex[1:])
    return (x,y)
