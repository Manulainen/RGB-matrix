#! /usr/bin/python3
"""
CORE para la puta matriz RGB de 8x8 de los fucking chinos
dados 27 putos colores indexados (AMSTRAD) se pueden hacer varias cosas:
-pintar un puto pixel
-pintar una puta columna
-pintar un puto sprite
-hacer aparecer un puto sprite por cualquier lado de la puta matriz


TODO:
    -definicion de colores en otro fichero aparte
    -definicion de los simbolos en otro fichero aparte

    +rowsDown van de [0-7]
    rowsUp van de [1-8]
    STOSTAMAL!! MUYMAL!

    +Unificar estas dos putas funciones    showSymbol2    drawSwymbol2

    +Ya estan las funciones limpias de up down left y right show
    -optimizar el pintado, esto es un follon que no va a sabe ni donde sa metio
    -mejorar los parametros, molaria que 't' no fuera el numero de iteraciones pero el tiempo
     que estara visible tras las animaciones

    +renombrar los nombres de las funciones

    --probar el core2 experimental, que no hace iteraciones por columna sino por matrices,
      esto parece obvio, y resolveria el problema del parpadeo para correcciones de rojo mayores a 4
      pero no esta tan claro que la correccion de rojo se pueda aplicar eficazmente, un movidote vaya
      aqui iria guay la atenuacion

    +aceleracion deberia ser jodidamente parametrizable
      

"""

import RPi.GPIO as GPIO
import time
import readchar

__author__ = 'Manolo'
__version__ = '0.3'

SDI   = 10 # MOSI
RCLK  = 8  # CE
SRCLK = 11 # CLK

Up =True
Down = False

#Fichero aparte?
c01 = 0b000000000000
c02 = 0b001001000000
c03 = 0b001001001001
c04 = 0b010010000000
c05 = 0b011011000000
c06 = 0b011011001001
c07 = 0b010010010010
c08 = 0b011011010010
c09 = 0b011011011011
c10 = 0b100000000000
c11 = 0b101001000000
c12 = 0b101001001001
c13 = 0b110010000000
c14 = 0b111011000000
c15 = 0b111011001001
c16 = 0b110010010010
c17 = 0b111011010010
c18 = 0b111011011011
c19 = 0b100000100000
c20 = 0b101001100000
c21 = 0b101001101001
c22 = 0b110010100000
c23 = 0b111011100000
c24 = 0b111011101001
c25 = 0b110010110010
c26 = 0b111011110010
c27 = 0b111011111011

#Esto en un fchero aparte
#C_RAYO
#C_NUBE
#C_SOL
#C_NIEVE
#C_GOTA
#C_SOL_CUBIERTO
#C_LUNA
#:)
#C_SMILEY_1
#x(          
#C_SMILEY_2
#:'(          
#C_SMILEY_3
#:D          
#C_SMILEY_4
#:S         
#C_SMILEY_5
#:@          
#C_SMILEY_6
#^^     
#C_SMILEY_7
#:P
#C_SMILEY_8
#:(
#C_SMILEY_9
#8)
#C_SMILEY_10
#C_FANTASMA
#C_SKULL
#C_FIRE
#C_LAPIZ
#C_THINK
#C_CLOCK
#C_ZZ
#C_NOTA1
#C_NOTA2
#C_INTERRO
#C_EXCLA
#C_CORAZON
#C_CORAZON_ROTO
#C_OIKEIN
#C_VAARIN

C_RAYO=[
        [c01, c01, c01, c01, c22, c01, c01, c01],
        [c01, c01, c22, c25, c25, c01, c01, c01],
        [c22, c25, c25, c25, c25, c01, c01, c01],
        [c25, c25, c22, c01, c25, c01, c25, c22],
        [c25, c22, c01, c01, c25, c25, c22, c01],
        [c22, c01, c01, c01, c25, c22, c01, c01],
        [c01, c01, c01, c01, c22, c01, c01, c01],
        [c01, c01, c01, c01, c01, c01, c01, c01]]

C_NUBE=[
        [c01, c01, c01, c14, c01, c06, c01, c01],
        [c01, c01, c01, c14, c01, c01, c01, c06],
        [c01, c14, c14, c14, c01, c01, c01, c01],
        [c14, c14, c14, c14, c01, c06, c01, c01],
        [c14, c14, c14, c14, c01, c01, c01, c06],
        [c14, c14, c14, c14, c01, c01, c01, c01],
        [c01, c14, c14, c14, c01, c06, c01, c01],
        [c01, c01, c01, c14, c01, c01, c01, c06]]

C_SOL=[
        [c22, c22, c01, c22, c22, c01, c22, c22],
        [c22, c01, c25, c25, c25, c25, c01, c22],
        [c01, c25, c25, c25, c25, c25, c25, c01],
        [c22, c25, c25, c25, c25, c25, c25, c22],
        [c22, c25, c25, c25, c25, c25, c25, c22],
        [c01, c25, c25, c25, c25, c25, c25, c01],
        [c22, c01, c25, c25, c25, c25, c01, c22],
        [c22, c22, c01, c22, c22, c01, c22, c22]]

C_NIEVE=[
        [c01, c01, c01, c01, c27, c01, c01, c01],
        [c01, c01, c01, c27, c27, c27, c01, c01],
        [c01, c27, c01, c01, c27, c01, c01, c01],
        [c27, c27, c27, c27, c27, c01, c27, c01],
        [c01, c27, c01, c27, c27, c27, c27, c27],
        [c01, c01, c01, c27, c01, c01, c27, c01],
        [c01, c01, c27, c27, c27, c01, c01, c01],
        [c01, c01, c01, c27, c01, c01, c01, c01]]

C_GOTA=[
        [c01, c01, c01, c01, c06, c06, c06, c01],
        [c01, c01, c01, c27, c27, c06, c27, c06],
        [c01, c01, c27, c27, c06, c06, c06, c06],
        [c06, c06, c06, c06, c06, c06, c06, c06],
        [c01, c01, c06, c06, c06, c06, c06, c06],
        [c01, c01, c01, c06, c06, c06, c06, c06],
        [c01, c01, c01, c01, c06, c06, c06, c01],
        [c01, c01, c01, c01, c01, c01, c01, c01]]

C_SOL_CUBIERTO=[
        [c01, c01, c01, c22, c22, c22, c01, c15],
        [c01, c01, c22, c25, c25, c25, c22, c15],
        [c01, c22, c25, c25, c25, c25, c15, c14],
        [c01, c22, c25, c25, c15, c15, c14, c14],
        [c01, c22, c25, c15, c14, c14, c14, c14],
        [c01, c01, c22, c15, c14, c14, c14, c14],
        [c01, c01, c01, c15, c14, c14, c14, c14],
        [c01, c01, c01, c01, c15, c14, c14, c14]]

C_LUNA=[
        [c01, c01, c14, c27, c27, c14, c01, c01],
        [c01, c14, c27, c27, c27, c27, c14, c01],
        [c14, c27, c27, c27, c27, c27, c27, c14],
        [c27, c14, c01, c01, c01, c14, c27, c14],
        [c27, c01, c01, c01, c01, c01, c27, c14],
        [c27, c01, c01, c01, c01, c01, c27, c14],
        [c01, c14, c01, c01, c01, c01, c14, c01],
        [c01, c01, c01, c01, c01, c14, c01, c01]]


#SMILEYS
#:)
C_SMILEY_1=[
        [c01, c01, c25, c25, c25, c25, c01, c01],
        [c01, c25, c01, c01, c25, c01, c25, c01],
        [c25, c25, c25, c25, c25, c25, c01, c25],
        [c25, c25, c25, c25, c25, c25, c01, c25],
        [c25, c25, c25, c25, c25, c25, c01, c25],
        [c25, c25, c25, c25, c25, c25, c01, c25],
        [c01, c25, c01, c01, c25, c01, c25, c01],
        [c01, c01, c25, c25, c25, c25, c01, c01]]
#x(          
C_SMILEY_2=[
        [c01, c01, c25, c25, c25, c25, c01, c01],
        [c01, c25, c01, c25, c25, c25, c25, c01],
        [c25, c25, c25, c01, c25, c25, c01, c25],
        [c25, c25, c25, c25, c25, c01, c25, c25],
        [c25, c25, c25, c25, c25, c01, c25, c25],
        [c25, c25, c25, c01, c25, c25, c01, c25],
        [c01, c25, c01, c25, c25, c25, c25, c01],
        [c01, c01, c25, c25, c25, c25, c01, c01]]         
#:'(          
C_SMILEY_3=[
        [c01, c01, c25, c25, c25, c25, c01, c01],
        [c01, c25, c01, c06, c06, c25, c25, c01],
        [c25, c25, c01, c25, c25, c25, c25, c25],
        [c25, c25, c25, c25, c25, c01, c01, c25],
        [c25, c25, c25, c25, c25, c01, c01, c25],
        [c25, c25, c01, c25, c25, c25, c25, c25],
        [c01, c25, c01, c06, c06, c25, c25, c01],
        [c01, c01, c25, c25, c25, c25, c01, c01]]
#:D          
C_SMILEY_4=[
        [c01, c01, c25, c01, c25, c25, c01, c01],
        [c01, c25, c01, c25, c25, c01, c25, c01],
        [c25, c25, c25, c01, c25, c01, c01, c25],
        [c25, c25, c25, c25, c25, c01, c01, c25],
        [c25, c25, c25, c25, c25, c01, c01, c25],
        [c25, c25, c25, c01, c25, c01, c01, c25],
        [c01, c25, c01, c25, c25, c01, c25, c01],
        [c01, c01, c25, c01, c25, c25, c01, c01]]
#:S          
C_SMILEY_5=[
        [c01, c01, c25, c25, c25, c25, c01, c01],
        [c01, c25, c01, c01, c25, c25, c25, c01],
        [c25, c25, c25, c25, c25, c25, c01, c25],
        [c25, c25, c25, c25, c25, c25, c01, c25],
        [c25, c25, c25, c25, c25, c01, c25, c25],
        [c25, c25, c25, c25, c25, c01, c25, c25],
        [c01, c25, c01, c01, c25, c25, c25, c01],
        [c01, c01, c25, c25, c25, c25, c01, c01]]
#:@          
C_SMILEY_6=[
        [c01, c01, c19, c19, c19, c19, c01, c01],
        [c01, c19, c01, c19, c19, c19, c19, c01],
        [c19, c19, c19, c01, c19, c01, c01, c19],
        [c19, c19, c19, c19, c19, c01, c01, c19],
        [c19, c19, c19, c19, c19, c01, c01, c19],
        [c19, c19, c19, c01, c19, c01, c01, c19],
        [c01, c19, c01, c19, c19, c19, c19, c01],
        [c01, c01, c19, c19, c19, c19, c01, c01]]
#^^     
C_SMILEY_7=[
        [c01, c01, c25, c25, c24, c24, c01, c01],
        [c01, c25, c01, c01, c24, c24, c25, c01],
        [c25, c25, c25, c25, c25, c25, c25, c25],
        [c25, c25, c25, c25, c25, c25, c01, c25],
        [c25, c25, c25, c25, c25, c25, c01, c25],
        [c25, c25, c25, c25, c25, c25, c25, c25],
        [c01, c25, c01, c01, c24, c24, c25, c01],
        [c01, c01, c25, c25, c24, c24, c01, c01]]
#:P
C_SMILEY_8=[
        [c01, c01, c25, c25, c25, c25, c01, c01],
        [c01, c25, c01, c25, c25, c01, c25, c01],
        [c25, c25, c01, c25, c25, c01, c25, c25],
        [c25, c25, c25, c25, c25, c01, c25, c25],
        [c25, c25, c25, c25, c25, c01, c19, c19],
        [c25, c25, c01, c25, c25, c01, c19, c19],
        [c01, c25, c01, c25, c25, c01, c25, c01],
        [c01, c01, c25, c25, c25, c25, c01, c01]]
#:(
C_SMILEY_9=[
        [c01, c01, c25, c25, c25, c25, c01, c01],
        [c01, c25, c01, c01, c25, c25, c25, c01],
        [c25, c25, c25, c25, c25, c25, c01, c25],
        [c25, c25, c25, c25, c25, c01, c25, c25],
        [c25, c25, c25, c25, c25, c01, c25, c25],
        [c25, c25, c25, c25, c25, c25, c01, c25],
        [c01, c25, c01, c01, c25, c25, c25, c01],
        [c01, c01, c25, c25, c25, c25, c01, c01]]
#8)
C_SMILEY_10=[
        [c01, c01, c27, c01, c01, c25, c01, c01],
        [c01, c25, c01, c01, c01, c25, c25, c01],
        [c25, c25, c01, c01, c01, c25, c01, c25],
        [c25, c25, c01, c25, c25, c25, c01, c25],
        [c25, c25, c01, c25, c25, c25, c01, c25],
        [c25, c25, c27, c01, c01, c25, c01, c25],
        [c01, c25, c01, c01, c01, c25, c25, c01],
        [c01, c01, c01, c01, c01, c25, c01, c01]]

#FANTASMA
C_FANTASMA=[
        [c01, c14, c27, c27, c27, c27, c27, c27],
        [c14, c27, c01, c01, c27, c27, c27, c27],
        [c27, c27, c27, c27, c27, c01, c27, c01],
        [c27, c27, c27, c27, c27, c01, c27, c27],
        [c27, c27, c27, c27, c27, c01, c27, c27],
        [c27, c27, c27, c27, c27, c01, c27, c01],
        [c14, c27, c01, c01, c27, c27, c27, c27],
        [c01, c14, c27, c27, c27, c27, c27, c27]]
#SKULL
C_SKULL=[
        [c01, c14, c27, c15, c15, c27, c01, c01],
        [c14, c27, c27, c01, c01, c27, c27, c27],
        [c27, c27, c27, c01, c15, c27, c27, c01],
        [c27, c27, c27, c27, c14, c01, c27, c27],
        [c27, c27, c27, c27, c14, c01, c27, c27],
        [c27, c27, c27, c01, c15, c27, c27, c01],
        [c14, c27, c27, c01, c01, c27, c27, c27],
        [c01, c14, c27, c15, c15, c27, c01, c01]]
#FIRE
C_FIRE=[
        [c01, c01, c01, c01, c19, c19, c19, c01],
        [c01, c01, c01, c19, c22, c22, c22, c19],
        [c01, c01, c19, c19, c19, c25, c25, c22],
        [c19, c19, c22, c22, c25, c27, c27, c25],
        [c01, c01, c01, c19, c22, c27, c27, c25],
        [c01, c01, c19, c22, c22, c25, c25, c22],
        [c01, c01, c01, c19, c19, c22, c22, c19],
        [c01, c01, c01, c01, c19, c19, c19, c01]]
#LAPIZ  #ES UN TRUNIACO
C_LAPIZ=[
        [c01, c01, c01, c01, c01, c01, c15, c15],
        [c01, c01, c01, c01, c23, c23, c23, c15],
        [c01, c01, c01, c25, c22, c23, c23, c01],
        [c01, c01, c25, c25, c25, c13, c22, c01],
        [c01, c14, c25, c25, c22, c22, c01, c01],
        [c23, c24, c14, c22, c22, c01, c01, c01],
        [c24, c24, c24, c15, c01, c01, c01, c01],
        [c01, c24, c24, c01, c01, c01, c01, c01]]
#THINK
C_THINK=[
        [c01, c27, c27, c27, c27, c01, c01, c01],
        [c27, c27, c27, c01, c27, c27, c01, c01],
        [c27, c27, c27, c27, c27, c27, c01, c01],
        [c27, c27, c27, c01, c27, c27, c01, c01],
        [c27, c27, c27, c27, c27, c27, c27, c27],
        [c27, c27, c27, c01, c27, c27, c27, c01],
        [c27, c27, c27, c27, c27, c27, c01, c01],
        [c01, c27, c27, c27, c27, c01, c01, c01]]
#CLOCK
C_CLOCK=[
        [c01, c01, c14, c14, c14, c14, c01, c01],
        [c01, c14, c27, c27, c27, c27, c14, c01],
        [c14, c27, c27, c27, c27, c27, c27, c14],
        [c14, c01, c01, c01, c01, c27, c27, c14],
        [c14, c27, c27, c27, c01, c27, c27, c14],
        [c14, c27, c27, c01, c27, c27, c27, c14],
        [c01, c14, c27, c27, c27, c27, c14, c01],
        [c01, c01, c14, c14, c14, c14, c01, c01]]
#PINTAZZ
C_ZZ=[
        [c06, c02, c01, c01, c06, c02, c01, c01],
        [c06, c02, c01, c06, c06, c02, c01, c01],
        [c06, c02, c06, c02, c06, c02, c01, c06],
        [c06, c06, c02, c01, c06, c02, c01, c01],
        [c06, c02, c01, c01, c02, c02, c06, c02],
        [c02, c01, c01, c06, c01, c06, c06, c02],
        [c01, c01, c01, c06, c06, c02, c06, c02],
        [c01, c01, c01, c06, c02, c01, c06, c02]]
#NOTA1
C_NOTA1=[
        [c01, c01, c01, c01, c01, c01, c15, c15],
        [c01, c01, c01, c01, c01, c15, c15, c15],
        [c01, c01, c01, c01, c01, c15, c15, c15],
        [c01, c01, c01, c01, c01, c15, c15, c15],
        [c15, c15, c15, c15, c15, c15, c15, c01],
        [c15, c15, c01, c01, c01, c01, c01, c01],
        [c15, c15, c01, c01, c01, c01, c01, c01],
        [c15, c15, c01, c01, c01, c01, c01, c01]]
#NOTA2
C_NOTA2=[
        [c01, c01, c01, c01, c01, c01, c15, c15],
        [c01, c01, c01, c01, c01, c01, c15, c15],
        [c01, c15, c15, c15, c15, c15, c15, c01],
        [c01, c15, c15, c01, c01, c01, c01, c01],
        [c01, c15, c15, c01, c01, c01, c01, c01],
        [c15, c15, c01, c01, c01, c15, c15, c01],
        [c15, c15, c01, c01, c01, c15, c15, c01],
        [c15, c15, c15, c15, c15, c15, c01, c01]]
#?
C_INTERRO=[
        [c01, c27, c27, c01, c01, c01, c01, c01],
        [c27, c27, c27, c01, c01, c01, c01, c01],
        [c27, c27, c01, c01, c01, c01, c01, c01],
        [c27, c27, c01, c01, c27, c27, c01, c27],
        [c27, c27, c01, c01, c27, c27, c01, c27],
        [c27, c27, c01, c01, c27, c01, c01, c01],
        [c27, c27, c27, c27, c27, c01, c01, c01],
        [c01, c27, c27, c27, c01, c01, c01, c01]]
#!
C_EXCLA=[
        [c01, c01, c01, c01, c01, c01, c01, c01],
        [c01, c01, c01, c01, c01, c01, c01, c01],
        [c01, c27, c27, c27, c01, c01, c01, c01],
        [c27, c27, c27, c27, c27, c27, c01, c27],
        [c27, c27, c27, c27, c27, c27, c01, c27],
        [c01, c27, c27, c27, c01, c01, c01, c01],
        [c01, c01, c01, c01, c01, c01, c01, c01],
        [c01, c01, c01, c01, c01, c01, c01, c01]]
# <3
C_CORAZON=[
        [c01, c01, c27, c27, c24, c01, c01, c01],
        [c01, c19, c27, c19, c19, c24, c01, c01],
        [c01, c19, c19, c19, c19, c19, c19, c01],
        [c01, c01, c19, c19, c19, c19, c19, c19],
        [c01, c01, c19, c19, c19, c19, c19, c19],
        [c01, c19, c19, c19, c19, c19, c19, c01],
        [c01, c19, c19, c19, c19, c19, c01, c01],
        [c01, c01, c19, c19, c19, c01, c01, c01]]
# ~<3
C_CORAZON_ROTO=[
        [c01, c01, c27, c24, c19, c01, c01, c01],
        [c01, c19, c19, c19, c19, c19, c01, c01],
        [c01, c19, c01, c19, c19, c19, c19, c01],
        [c01, c01, c01, c19, c01, c19, c01, c01],
        [c01, c01, c19, c01, c19, c01, c19, c19],
        [c01, c19, c19, c19, c19, c19, c19, c01],
        [c01, c19, c19, c19, c19, c19, c01, c01],
        [c01, c01, c19, c19, c19, c01, c01, c01]]
# OK
C_OIKEIN=[
        [c01, c01, c01, c01, c07, c08, c01, c01],
        [c01, c01, c01, c01, c07, c07, c08, c01],
        [c01, c01, c01, c01, c01, c08, c07, c07],
        [c01, c01, c01, c01, c01, c07, c07, c08],
        [c01, c01, c01, c01, c07, c07, c08, c01],
        [c01, c01, c08, c07, c08, c01, c01, c01],
        [c08, c07, c07, c08, c01, c01, c01, c01],
        [c07, c07, c08, c01, c01, c01, c01, c01]]
# KO
C_VAARIN=[
        [c01, c19, c01, c01, c01, c01, c01, c19],
        [c01, c19, c20, c01, c01, c01, c19, c01],
        [c01, c01, c19, c20, c20, c19, c01, c01],
        [c01, c01, c01, c19, c19, c20, c01, c01],
        [c01, c01, c19, c19, c19, c20, c01, c01],
        [c01, c19, c19, c20, c01, c19, c01, c01],
        [c19, c19, c19, c01, c01, c01, c19, c01],
        [c20, c19, c20, c01, c01, c01, c01, c20]]


def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(SDI,   GPIO.OUT)
    GPIO.setup(RCLK,  GPIO.OUT)
    GPIO.setup(SRCLK, GPIO.OUT)
    
    GPIO.setup(SDI,   GPIO.LOW)
    GPIO.setup(RCLK,  GPIO.LOW)
    GPIO.setup(SRCLK, GPIO.LOW)

def matrixPinIn(bit):
    GPIO.output(SDI, bit)
    GPIO.output(SRCLK, GPIO.HIGH)
    GPIO.output(SRCLK, GPIO.LOW) 

def matrixPinOut():
    GPIO.output(RCLK, GPIO.HIGH)
    GPIO.output(RCLK, GPIO.LOW)

def matrixClean():
    a = 0b000000001111111111111111
    for i in range(32):
        bit = a & 0x01
        a >>=1
        matrixPinIn(bit)
    matrixPinOut()

def columnIn(cols, red, green, blue):
        b= (cols<<24) | ((~green&0xff)<<16) | ((~blue&0xff)<<8) | (~red&0xff)
    
        for i in range(32):
                bit = b & 0x01
                b >>=1
                matrixPinIn(bit)
        matrixPinOut()

def showPixel(col,fil,colIndex):
    c = 0x1 << (col -1)
    t = list()
    #4 pintados de 3
    for i in range(12):
        bit = colIndex & 0x01
        colIndex>>=1
        t.append(bit << (8 - fil))
        
    columnIn(c, t[11], t[10], t[9])
    columnIn(c, t[8], t[7], t[6])
    columnIn(c, t[5], t[4], t[3])
    columnIn(c,t[2], t[1], t[0])



def showColumn(r, col, listElems, ord=Up, rows=8):
    """
    Status: TERMINADO
    
    Pinta en la columna col , el contenido de listElems
    para animaciones de aparecer o desaparecer, ord y rows
    Cada drawColumna puede llamar a pintaColumna entre 4 y 8 veces,
    dependiendo de la correccion de rojo.

    redCorr : int
       [1-3] Correccion de rojo, 1 poco rojo, 3 mucho rojo
    col : int
       [1-8]      Indice de la columna a pintar
    listElems : list
       Lista de los 8 colores que componen la columna
    ord : Up, Down
       [Up, Down] Up, rows empieza a contar por el inicio de listElems
                  Down, rows  empieza a contar por el final de listElems 
    rows : int
       [1-8]= numero de filas a pintar, 8 pinta la columna entera, 
    """

    #UP empieza a pintar la primera fila por abajo,
    #row = 1 => primer elemento de la lista en la ultima fila
    #row = 2 => 1er y 2ndo elemento de la lista en la penultima y ultima fila
    #row = 8 => lista completa en su orden
    if ord == Up:                 
        listElems=listElems[:rows]
        lenTargs = len(listElems)
        if lenTargs != 8:
            for i in range(8- lenTargs):
                listElems.insert(0,c01)
                
    #DOWN empieza a pintar la ultima fila por arriba,
    #row = 1 => ultimo elemento de la lista en la primera fila
    #row = 2 => ultimo y penultimo elemento de la lista en la segunda y primera fila
    #row = 8 => lista completa en su orden
    else:                           
        listElems=listElems[(8-rows):]
        lenTargs = len(listElems)
        if lenTargs != 8:
            for i in range(8- lenTargs):
                listElems.append(c01)
    
    c = 0x1 << (col -1)

    color = listElems[0]
    t = list()
    
    #4 pintados de 3
    #COLOR1
    for i in range(12):
        bit = color & 0x01
        color>>=1
        t.append(bit)

    #Resto de colores
    for j in range(7):
       color = listElems[j+1]
       for i in range(12):
           bit = color & 0x01
           color>>=1
           t[i] = (t[i]<<1) + bit

    for i in range(r):        
        columnIn(c, t[11], t[10], t[9])
    columnIn(c, t[8], t[7], t[6])
    for i in range(r): 
        columnIn(c, t[5], t[4], t[3])
    columnIn(c,t[2], t[1], t[0])



#SHOW
################################################################
def showSymbol(r,t, symbol, ord=Up, rows=8):
    """
    Status: TERMINADO
    
    Pinta durante t iteracions el simbolo symbol en la matriz
    r: int
    [1-3] Correccion de rojo
    t: int
    [1-n] Numero de iteraciones
    symbol : symbol
    simbolo a pintar, busca la lista disponible, serebro de atun
    ord: Up Down
    rows: int
    [1-8] numero de filas a pintar de la matriz (util en animaciones)
    """
    for i in range(t):
        for columna in range(8):
            showColumn(r, columna+1, symbol[columna], ord, rows)



#RIGHT   
################################################################
def rightSymbol(r,t, symbol, aceleracionI=90, aceleracionF=90):
    """
    Status: TERMINADO
    
    Muestra un simbolo haciendolo aparecer hacia la derecha
    permanece un rato y desaparece por la izquierda
    r : int
       correccion de rojo para el simbolo [1-3]
    t :int
       tiempo que permanecera visible antes de apagarse
    symbol : symbol
       simbolo a pintar
    aceleracionI : int
       mas aceleracionI, menos tarda la animacion Inicial
    aceleracionF: int
       mas aceleracionF, menos tarda la animacion Final
    
    """
    for times in range(1,8+1):
        for i in range(t//aceleracionI):
            for columna in range(1, times+1):
                showColumn(r,columna, symbol[columna + 7 - times])
              
    showSymbol(r,t, symbol)

    for times in reversed(range(1,8+1)):
        for i in range(t//aceleracionF):
            for columna in range(1, times+1):
                showColumn(r, columna, symbol[columna + 7 - times])


#LEFT
################################################################
def leftSymbol(r,t, symbol, aceleracionI=90, aceleracionF=90):
    """
    Status: TERMINADO
    
    Muestra un simbolo haciendolo aparecer hacia la izquierda
    permanece un rato y desaparece por la derecha
    r : int
       correccion de rojo para el simbolo [1-3]
    t :int
       tiempo que permanecera visible antes de apagarse
    symbol : symbol
       simbolo a pintar
    aceleracionI : int
       mas aceleracionI, menos tarda la animacion Inicial
    aceleracionF: int
       mas aceleracionF, menos tarda la animacion Final
    
    """
    
    for times in range(1,8+1):
        for i in range(t//aceleracionI):
            for columna in range(1, times+1):
                showColumn(r,9-columna, symbol[times-columna])
       
    showSymbol(r,t, symbol)

    for times in reversed(range(1,8+1)):
        for i in range(t//aceleracionF):
            for columna in range(1, times+1):
                  showColumn(r, 9-columna,symbol[times-columna])



#DOWN
################################################################
def downSymbol(r,t, symbol,aceleracionI=90, aceleracionF=90):
    """
    Status: TERMINADO
    
    Muestra un simbolo haciendolo aparecer hacia abajo
    permanece un rato y desaparece por arriba
    r : int
       correccion de rojo para el simbolo [1-3]
    t :int
       tiempo que permanecera visible antes de apagarse
    symbol : symbol
       simbolo a pintar
    aceleracionI : int
       mas aceleracionI, menos tarda la animacion Inicial
    aceleracionF: int
       mas aceleracionF, menos tarda la animacion Final
    """
    
    for rows in range(1,8+1):
         showSymbol(r, t//aceleracionI, symbol, Down, rows)
        
    showSymbol(r,t, symbol)

    for rows in reversed(range(1,8+1)):
         showSymbol(r, t//aceleracionF, symbol, Down, rows)


#UP
################################################################
def upSymbol(r,t, symbol, aceleracionI=90, aceleracionF=90):
    """
    Status: TERMINADO
    
    Muestra un simbolo haciendolo aparecer hacia arriba
    permanece un rato y desaparece por abajo
    r : int
       correccion de rojo para el simbolo [1-3]
    t :int
       tiempo que permanecera visible antes de apagarse
    symbol : symbol
       simbolo a pintar
    aceleracionI : int
       mas aceleracionI, menos tarda la animacion Inicial
    aceleracionF: int
       mas aceleracionF, menos tarda la animacion Final
    """

    for rows in range(1,8+1):
        showSymbol(r,t//aceleracionI, symbol, Up, rows)

    showSymbol(r,t, symbol)


    for rows in reversed(range(1,8+1)):
        showSymbol(r,t//aceleracionF, symbol, Up, rows)
     
setup()
try:
        #upSymbol(3,90,C_RAYO)
        #upSymbol(1,90,C_NUBE)
        #upSymbol(3,90,C_SOL)
        #upSymbol(2,90,C_NIEVE)
        #upSymbol(1,90,C_GOTA)
        #upSymbol(3,90,C_SOL_CUBIERTO)
        #upSymbol(2,90,C_LUNA)
        #         
        #upSymbol(3,90,C_SMILEY_1)
        #upSymbol(3,93,C_SMILEY_2)
        #upSymbol(3,93,C_SMILEY_3)
        #upSymbol(3,93,C_SMILEY_4)
        #upSymbol(3,93,C_SMILEY_5)
        #upSymbol(3,93,C_SMILEY_6)
        #upSymbol(3,93,C_SMILEY_7)
        #upSymbol(3,93,C_SMILEY_8)
        #upSymbol(3,93,C_SMILEY_9)
        #upSymbol(3,93,C_SMILEY_10)
        #         
        #upSymbol(2,93,C_FANTASMA)
        #upSymbol(3,93,C_SKULL)
        #upSymbol(3,93,C_FIRE)
        #upSymbol(2,100,C_LAPIZ)
        #upSymbol(2,100,C_THINK)
        #upSymbol(2,100,C_CLOCK)
        #upSymbol(2,100,C_ZZ)
        #upSymbol(1,100,C_NOTA1)
        #upSymbol(1,100,C_NOTA2)
        #upSymbol(2,100,C_INTERRO)
        #upSymbol(2,100,C_EXCLA)
        #upSymbol(3,100,C_CORAZON)
        #upSymbol(3,100,C_CORAZON_ROTO)
        #upSymbol(1,100,C_OIKEIN)
        #upSymbol(1,100,C_VAARIN)


        showSymbol(1,100,C_GOTA)
        upSymbol(3,100,C_LUNA)
        downSymbol(3,100,C_ZZ)
        leftSymbol(3,100,C_ZZ)
        rightSymbol(3,100,C_SMILEY_10)

  

        matrixClean()
except KeyboardInterrupt:
    matrixClean()
