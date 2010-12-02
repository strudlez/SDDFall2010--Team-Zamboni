# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor Boston, MA 02110-1301,  USA

#Goutil consists of two methods we use in multiple classes that converte between numeric coordinates(I.E. (1,10)) to a vertex on a Go board (I.E. (A10))
def coords_to_vertex(x,y): #Converts number coordinates to a letter and number(Board Vertex)
    letters = [chr(a) for a in range(ord('A'),ord('U'))] #Creates an Array of letters from A to T
    assert x < 20, 'messed up column entry'
    if x < 9: #These if statements are here to remove the I column, as Go boards skip I in the naming of columns
    	return letters[x-1]+str(y)
    if x >= 9:
	return letters[x]+str(y) #Returns the letter of the colum and the number of the row
    
def coords_from_vertex(vertex): #Determines numberic coordinates given a board vertex
    if ord(vertex[0]) < 74: #if the unicode value of the column is less than 74
    	x = ord(vertex[0])-ord('A')+2 #Set our x column to the unicode value of the letter, minus the unicode value of A, then increment it by 2
    else: #Otherwise, Get the unicode value of the letter minus the unicode value of A, incremented by 1 as we have skipped the letter I
	x = ord(vertex[0])-ord('A')+1
    y = int(vertex[1:])
    return (x,y) #Return the numeric coordinates
