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

def coords_to_vertex(x,y):
    letters = [chr(a) for a in range(ord('A'),ord('U'))]
    if x < 9:
    	return letters[x-1]+str(y)
    if x >= 9:
	return letters[x]+str(y)
    
def coords_from_vertex(vertex):
    if ord(vertex[0]) < 74:
    	x = ord(vertex[0])-ord('A')+2
    else:
	x = ord(vertex[0])-ord('A')+1
    y = int(vertex[1:])
    return (x,y) 
