#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math

# Primero creamos el mapa

#Leer el mapa de un archivo y guardar sus posiciones en una lista
class Mapa:
	def __init__(self, archivo="map.txt"):
		self.mapa = leerMapa(archivo)
		#guardo el valor de filas y columnas
		self.fil = len(self.mapa)
		self.col = len(self.mapa[0])

#devuelver un mapa a mostrar en pantalla
	def __str__(self):
		mostrar = ""
		for f in range(self.fil):
			for c in range(self.col):
				if self.mapa[f][c] == 0:
					mostrar += "  "
				if self.mapa[f][c] == 1:
					mostrar += "# "
				if self.mapa[f][c] == 2:
					mostrar += "I "
				if self.mapa[f][c] == 3:
					mostrar += "M "
				if self.mapa[f][c] == 4:
					mostrar += ". "
			mostrar += "\n"
		return mostrar

	def camino(self, lista):
		del lista[-1]
		for i in range(len(lista)):
			self.mapa[lista[i][0]][lista[i][1]] = 4	

#Creación de la clase Nodo
class Nodo:
	def __init__(self, posact=[0, 0], padre=None):
		self.posact = posact
		self.padre = padre
		#Estimación de distancia a la meta h(n)
		self.h = distancia(self.posact, posfin)
		
		# Distancia hasta el nodo actual g(n)
		if self.padre == None:
			self.g = 0
		else:
			self.g = self.padre.g + 1
		
		#definición de la función de peso f(n)
		self.f = self.g + self.h 

class Aestrella:
	#1.Crear un grafo G con un único nodo que contiene la descripción del problema.
	def __init__(self,mapa):
		self.mapa = mapa
		
		#Marcar inicio y fin
		self.inicio = Nodo(buscarPosicion(2, mapa)) #Buscar el inicio, asignar 2 al valor inicial en el método
		self.fin = Nodo(buscarPosicion(3, mapa)) #Buscar la meta, asignar 3 a las metas en el método
		
		#Crear una lista de nodos llamada ABIERTA e inicializarla con dicho nodo.
		self.ABIERTA = []
		
		#Llamar a este elemento r y asignarle g(r) = 0
		#2.Crear una lista de nodos llamada CERRADA inicialmente vacía.
		self.CERRADA = []
		self.CERRADA.append(self.inicio)
		
		#3.Hasta que se encuentre una meta o se devuelva fallo realizar las siguientes acciones:
		#3.1 Si ABIERTA está vacía terminar con fallo; en caso contrario, continuar.
		#3.3 Si m es meta, abandonar el proceso iterativo establecido en 3, devolviendo el camino de la solución, que se obtiene recorriendo los punteros de sus antepasados.
		#3.4 En caso contrario, expandir m generando todos sus sucesores.
		self.ABIERTA += self.sucesores(self.inicio)
		
		#Buscar hasta encontrar la meta		
		while self.meta():
			if not self.ABIERTA:
				break
			self.buscar()
		
		if not self.ABIERTA:
			self.camino = -1
		else:
			self.camino = self.camino()

	# El método devuelve una lista con los sucesores que no son obstáculo incluyendo diagonales
	def sucesores(self, nodo):
		sucesores = []
		if self.mapa.mapa[nodo.posact[0]+1][nodo.posact[1]] != 1:
			sucesores.append(Nodo([nodo.posact[0]+1, nodo.posact[1]], nodo))
		if self.mapa.mapa[nodo.posact[0]-1][nodo.posact[1]] != 1:
			sucesores.append(Nodo([nodo.posact[0]-1, nodo.posact[1]], nodo))
		if self.mapa.mapa[nodo.posact[0]][nodo.posact[1]-1] != 1:
			sucesores.append(Nodo([nodo.posact[0], nodo.posact[1]-1], nodo))
		if self.mapa.mapa[nodo.posact[0]][nodo.posact[1]+1] != 1:
			sucesores.append(Nodo([nodo.posact[0], nodo.posact[1]+1], nodo))
		if self.mapa.mapa[nodo.posact[0]+1][nodo.posact[1]+1] != 1:
			sucesores.append(Nodo([nodo.posact[0]+1, nodo.posact[1]+1], nodo))
		if self.mapa.mapa[nodo.posact[0]+1][nodo.posact[1]-1] != 1:
			sucesores.append(Nodo([nodo.posact[0]+1, nodo.posact[1]-1], nodo))
		if self.mapa.mapa[nodo.posact[0]-1][nodo.posact[1]+1] != 1:
			sucesores.append(Nodo([nodo.posact[0]-1, nodo.posact[1]+1], nodo))
		if self.mapa.mapa[nodo.posact[0]-1][nodo.posact[1]-1] != 1:
			sucesores.append(Nodo([nodo.posact[0]-1, nodo.posact[1]-1], nodo))
		return sucesores

	#3.2 Eliminar el nodo de ABIERTA que tenga un valor mínimo de f,
	#llamar a este nodo m e introducirlo en la lista CERRADA.
	def f_min(self):
		a = self.ABIERTA[0]
		m = 0
		for i in range(1,len(self.ABIERTA)):
			if self.ABIERTA[i].f < a.f:
				a = self.ABIERTA[i]
				m = i
		self.CERRADA.append(self.ABIERTA[m])
		del self.ABIERTA[m]


	#Método para comprobar si un nodo está en alguna lista
	def en_lista(self, nodo, lista):
		for i in range(len(lista)):
			if nodo.posact == lista[i].posact:
				return 1
		return 0

	#3.5 Para cada sucesor n' de m:
	#(1) Crear un puntero de n' a m.
	#(2) Calcular g(n') = g(m) + c(m,n')   c(a,b): coste de pasar de a a b (método distancia)
	#(3) Si n' está en ABIERTA, llamar n al nodo encontrado en dicha lista, añadirlo a los sucesores de m y realizar (3.1.).
	#(3.1.) Si g(n') < g(n) entonces redireccionar el puntero de n a m y cambiar el camino de menor coste encontrado a n desde la raíz; g(n) = g(n') y f(n) = g(n') + h(n).

	def ruta(self):
		for i in range(len(self.nodos)):
			if self.en_lista(self.nodos[i], self.CERRADA):
				continue
			elif not self.en_lista(self.nodos[i], self.ABIERTA):
				self.ABIERTA.append(self.nodos[i])
			else:
				if self.select.g+1 < self.nodos[i].g:
					for j in range(len(self.ABIERTA)):
						if self.nodos[i].posact == self.ABIERTA[j].posact:
							del self.ABIERTA[j]
							self.ABIERTA.append(self.nodos[i])
							break

	#Analizamos el último nodo de la lista CERRADA
	def buscar(self):
		self.f_min()
		self.select = self.CERRADA[-1]
		self.nodos = self.sucesores(self.select)
		self.ruta()

	#Comprobamos si la meta está en ABIERTA
	def meta(self):
		for i in range(len(self.ABIERTA)):
			if self.fin.posact == self.ABIERTA[i].posact:
				return 0
		return 1

	#El método devuelve una lista con el camino
	def camino(self):
		for i in range(len(self.ABIERTA)):
			if self.fin.posact == self.ABIERTA[i].posact:
				meta = self.ABIERTA[i]

		camino = []
		while meta.padre != None:
			camino.append(meta.posact)
			meta = meta.padre
		camino.reverse()
		return camino

#--------------------------------------------------------

#devuelve la posición de un nodo en el mapa
def buscarPosicion(n,mapa):
	for a in range(mapa.fil):
		for b in range(mapa.col):
			if mapa.mapa[a][b] == n:
				return [a, b]
	return 0

#Definición de Distancia (Euclídea)
def distancia(a, b):
#	return abs(a[0] - b[0]) + abs(a[1] - b[1]) #Distancia Manhatan.
	return math.sqrt(((a[0] - b[0])**2)+((a[1] - b[1])**2)) #Distancia Euclídea

# Quitar el último caracter de una lista
def quitaultimo(lista):
	for i in range(len(lista)):
		lista[i] = lista[i][:-1]
	return lista

#convierte una cadena en una lista
def listaporcadena(cadena):
	lista = []
	for i in range(len(cadena)):
		if cadena[i] == ".":
			lista.append(0)
		if cadena[i] == "#":
			lista.append(1)
		if cadena[i] == "I":
			lista.append(2)
		if cadena[i] == "M":
			lista.append(3)
	return lista

#Leer el archivo y pasarlo por el método para convertirlo en una lista
def leerMapa(archivo):
	mapa = open(archivo, "r")
	mapa = mapa.readlines()
	mapa = quitaultimo(mapa)
	for i in range(len(mapa)):
		mapa[i] = listaporcadena(mapa[i])
	return mapa

#----------------------------------------------------------------

#Muestro el mapa en pantalla
def main():
	mapa = Mapa()
	globals()["posfin"] = buscarPosicion(3, mapa)
	Sol = Aestrella(mapa)
	mapa.camino(Sol.camino)
	print(mapa)
	return 0

if __name__ == '__main__':
	main()