#!/usr/bin/python
# -*- coding: utf-8 -*-
#############################################
######## Manzano Cruz Isaias Abraham ########
#############################################

import argparse
import parted

def opciones():
    '''
    Funcion que parsea las opciones dadas por comandos
    Devuelve: Opciones ordenadas
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('-d','--device', help='Dispositivo o archivo para particionar', default=None)
    parser.add_argument('-l','--lista', help='Lista las particiones de un dispositivo o archivo', default=None)
    return parser.parse_args()


def verifica(args):
    '''
    Funcion que verifica que las opciones minimas para ejecutar el programa esten presentes, en caso contrario, termina el programa
    Recibe: Los argumentos
    Devuelve: None
    '''
    if args.device == None:
        print '\nDebes seleccionar el dispositivo \n'
        exit(1)


def particion_pri(sdb,disk,size,tipo,fin):
    geometry1 = parted.Geometry(start=fin, length=parted.sizeToSectors(size, 'MiB', sdb.sectorSize), device=sdb)
    filesystem1 = parted.FileSystem(type=tipo, geometry=geometry1)
    partition1 = parted.Partition(disk=disk, type=parted.PARTITION_NORMAL, fs=filesystem1, geometry=geometry1)
    disk.addPartition(partition1, constraint=sdb.optimalAlignedConstraint)
    disk.commit()
    return partition1.geometry.end


def main():
    opt = opciones()
    verifica(opt)
    #Inicializando dispositivo
    try:
        print '\nVerificando dispositivo............',
        sdb = parted.getDevice(opt.device)
    except Exception:
        print '[ERROR]'
        exit(1)
    print '[OK]'
    print '\nDispositivo seleccionado: '+opt.device
    c=''
    while c != 'y':
        c = raw_input('\nAl dispositivo '+opt.device+' se le eliminara la tabla de particion actual, quieres continuar? [Y/n] ')
        c = c.lower()
        if c == 'n':
            print '\nSaliendo ...\n'
            exit(1)
        elif c == '' or c == 'y':
            c='y'
            sdb.clobber()
            print ''
            pass
    try:
        disk=parted.newDisk(sdb)
    except Exception:
        pass
    print 'Creando dispositivo msdos\n'
    disk=parted.freshDisk(sdb,'msdos')
    print 'Tipos aceptados'
    for x in parted.fileSystemType.keys():
        print x+' ',
    print ''
    fin = 0
    n = raw_input('\nCuantas particiones van a ser? (maximo 4)> ')
    print ''
    for x in range(int(n)):
        print 'Particion primaria ' + str(x+1) + ':'
        t = raw_input('Tipo> ')
        s = long(raw_input('Tamaño en MiB> '))
        print ''
        fin = particion_pri(sdb,disk,s,t,fin)



main()
