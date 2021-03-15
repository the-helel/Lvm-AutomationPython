import os
import subprocess as sp

## create Menu for our program
def menu():
    sp.run("clear", shell=True)
    print("""\n
        1. Help [Steps for creating LVM ]
        2. Check how many storages is attached"
        3. Create Physical Volume (PV)
        4. Get Physical Volume details
        5. Create Volume Group (VG)
        6. Add Physical Volume(PV) to exisiting Volume Group(VG)
        6. Get Volume Group details
        7. Create Logical Volume(LV)
        8. Format the Logical Volume(LV)
        9. Get Logical Volume details
        10. Mount Logical Volume
        0. Exit
        """)
    while True:
       try:
          choice = int(input("Enter your choice:"))
          break
       except ValueError:
           print("No Valid Interger!, Please try again...")
    return choice

# what are the steps required to setup LVM
def get_steps():
    print("""
        1. Select the physical storage devices for LVM
        2. Create the Volume Group from Physical Volumes
        3. Create Logical Volumes from Volume Group
    """)

#get list of physical devices
def get_physical_storages():
   sp.run("clear", shell=True)
   sp.run("fdisk -l", shell=True)


def create_physical_volume():
    sp.run("clear", shell=True)
    device_name = input("Enter Physical storage name from you want to create physical volume [eg: /dev/sdb] :" )
    sp.run("sudo pvcreate {}".format(device_name), shell=True)
    sp.run("sudo pvdisplay {}".format(device_name), shell=True)

def get_all_pvs():
    sp.run("clear", shell=True)
    choice =  int(input(" Enter 1. pvscan 2. pvdisplay [all]"))
    if choice == 1:
        sp.run("sudo pvscan",shell=True)
    elif choice == 2:
        sp.run("sudo pvdisplay", shell=True)

def create_volume_group():
    sp.run("clear", shell=True)
    vg_name = input("Enter Volume Group name :")
    pv_name = input("Enter Physical Volume name :")
    sp.run("sudo vgcreate {} {}".format(vg_name, pv_name), shell=True)
    sp.run("sudo vgdisplay {}".format(vg_name), shell=True)
    choice = input("Do you want to add another Physical Volume to this Volume Group? [y/N]")
    if choice.lower() == 'y':
          extend_volume_group(vg_name)

def extend_volume_group( vg_name= ""):
    sp.run("clear", shell=True)

    if vg_name == "":
        vg_name = input("Enter Volume Group name : ")

    pv_name = input("Enter Physical volume Group :")
    sp.run("sudo vgextend {} {}".format(vg_name, pv_name), shell=True)
    sp.run("sudo vgdisplay {}".format(vg_name), shell=True)


def get_vg_details():
    sp.run("clear", shell=True)
    vg_name = input("Enter Volume Group name :")
    sp.run("sudo vgdisplay {}".format(vg_name), shell=True)


def create_logical_volume():
     sp.run("clear", shell=True)
     lv_name = input("Enter New Logical Volume name :")
     vg_name = input("Enter Volume Group Name(VG) :")
     size    = input("Enter the size of Logical Volume(LV) :")
     sp.run("sudo lvcreate --size {} --name {} {}".format(size, lv_name, vg_name), shell=True)
     sp.run("sudo lvdisplay {}/{}".format(vg_name, lv_name), shell=True)
     choice = input("Do you want to format this logical volume now? [y/N]")
     if choice.lower() == 'y':
        format_logical_volume("{}/{}".format(vg_name, lv_name))


def format_logical_volume(lv_name=""):
     sp.run("clear", shell=True)
     lv_name = input("Enter the Logical Volume name (eg: vg_name/lv_name) :")
     file_system =  input("Enter the file system (ext2, ext3, ext4, minix, xfs, cramfs) :")
     sp.run("sudo mkfs.{} /dev/{}".format(file_system, lv_name), shell=True)

def get_logical_volue():
    sp.run("clear", shell=True)
    lv_name = input("Enter Logical Volume Name (eg: vg_name/lv_name) : ")
    sp.run("sudo lvdisplay /dev/{}".format(lv_name), shell=True)


def mount_logical_volume():
    sp.run("clear", shell=True)
    lv_name = input("Enter the Logical Volume name (eg: vg_name/lv_name) :")
    mount_path = input("Enter absolute path of directory for mounting :")
    sp.run("mkdir -p {}".format(mount_path), shell=True)
    sp.run("sudo mount /dev/{} {}".format(lv_name, mount_path), shell=True)
    sp.run("sudo lsblk /dev/{}".format(lv_name), shell=True)


if __name__ == "__main__":
    print("Welcome To Python script for LVM")
    choice = menu()
    #create shell
    while (choice != 0 ):
        if choice == 1:
               get_steps()
        elif choice == 2:
               get_physical_storages()
        elif choice == 3:
               create_physical_volume()
        elif choice == 4:
               get_all_pvs()
        elif choice == 5:
               create_volume_group()
        elif choice == 6:
               extend_volume_group()
        elif choice == 7:
               create_logical_volume()
        elif choice == 8:
               format_logical_volume()
        elif choice == 9:
               get_logical_volue()
        elif choice == 10:
               mount_logical_volume()
        else:
             print("Wrong Choice !!")

        input("\n\nPress Enter to continue...:\t")
        choice =  menu()
