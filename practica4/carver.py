#!/usr/bin/python
# -*- coding: utf-8 -*-
#UNAM-CERT
#Manzano Cruz Isaias Abraham

import re
import optparse
import sys
import binascii
import time
import calendar
from binascii import hexlify
from binascii import unhexlify

def addOptions():
    '''
    Funcion que parsea los datos que se tomen de linea de comandos como opciones para ejecutar el programa
    Devuelve un objeto cuyos atributos son las opciones de ejecucion
    '''
    parser = optparse.OptionParser()
    parser.add_option('-d', '--directory', dest='directory', default=None, help='Indica el directorio donde se guardaran los archivos encontrados')
    parser.add_option('-f', '--file', dest='file', default=None, help='Indica el archivo a analizar')
    parser.add_option('-c', '--config', dest='config', default='config.conf', help='Indica el archivo de configuracion')
    opts,args = parser.parse_args()
    return opts


def printError(msg, exit = False):

    '''
    Esta funcion imprime en la salida de error estandar un mensaje
    Recibe:
	msg:	mensaje a imprimir y exit:  exit el cual indica si el el programa termina su ejecucion o no
	exit:	Si es True termina la ejecucion del programa
    '''
    sys.stderr.write('Error:\t%s\n' % msg)
    if exit:
        sys.exit(1)


def check_opts(opts):
    if opts.directory == None and opts.file == None:
        printError('Debes indicar el archivo a analizar y el directorio para guardar los archivos >:v',True)

    if opts.directory == None:
        printError('Debes indicar el directorio para guardar los archivos >:v',True)
    if opts.file == None:
        printError('Debes indicar el archivo a analizar  >:v',True)


def lee_archivo(archivo):
    try:
        return open(archivo, 'rb').read()
    except Exception as e:
        printError(e,True)


def obtener_hex(cadena):
    return hexlify(cadena).upper()


def archivo_binario(original):
    binario = bytes(original)
    binario = (binascii.unhexlify(binario))
    return binario


def escribe_binario(binario,nombre):
    malware = open(nombre,'w+b')
    malware.write(binario)
    malware.close()
    msg = 'Se creo el archivo llamado: "'+nombre.split('/')[1]+'" en el directorio "'+nombre.split('/')[0]+'/"'
    print msg


def lee_config(opts):
    lista=[]
    with open(opts.config) as conf:
        for line in conf:
            if line[0] != '#':
                line = line.replace('\n','')
                lista.append(line)
    return lista


def main():
    opts = addOptions()
    check_opts(opts)
    lista = lee_config(opts)
    if opts.directory[-1] == '/':
        opts.directory = opts.directory[:-1]

    print '\nArchivo de configuracion'
    for x in lista:
        print x
    print '\nArchivo: '+opts.file
    print 'Directorio: '+opts.directory+'/'
    print 'Configuraciòn: '+opts.config
    print '\n'
    arch = lee_archivo(opts.file)
    hexa = obtener_hex(arch)
    c = 0

    for x in lista:
        c += 1
        x.replace('\n','')
        if len(x.split()) == 3:
            ext,tam,inicio = x.split()
            tam = int(tam)
            try:
                if len(hexa.split(inicio)) > 1:
                    print 'Archivos tipo: '+ext+' \noffset: '+str(tam)
                    ind = [m.start() for m in re.finditer(inicio,hexa)]
                    #print ind
                    for i in range(len(ind)):
                        #print ind[i]
                        if i+1 < len(ind) and ind[i+1]-ind[i] < tam:
                            rest = hexa[ind[i]:ind[i+1]]
                            if len(rest)%2 != 0:
                                rest = rest[:-1]
                            binario = archivo_binario(rest)
                            nombre = opts.directory+'/'+str(time.time())+'_'+str(i)+'.'+ext
                            #print nombre
                            escribe_binario(binario,nombre)

                        else:
                            rest = hexa[ind[i]:ind[i]+tam]
                            if len(rest)%2 != 0:
                                rest = rest[:-1]
                            rest.strip()
                            binario = archivo_binario(rest)
                            nombre = opts.directory+'/'+str(time.time())+'_'+str(i)+'.'+ext
                            #print nombre
                            escribe_binario(binario,nombre)

                    print ''
            except Exception as e:
                print e

        else:
            printError('Error en la linea '+str(c)+' ' + x + '\n')

    #original = archivo_original(hexa)
    #binario = archivo_binario(original)
    #escribe_binario(binario,opts.descifra)


if __name__ == '__main__':
    main()
