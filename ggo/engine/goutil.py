def coords_to_vertex(x,y):
    letters = [chr(a) for a in range(ord('A'),ord('U'))]
    return letters[x]+str(y)
def vertex_to_coords(vertex):
    x = ord(vertex[0])-ord('A')+1
    y = int(vertex[1:])
    return (x,y)
