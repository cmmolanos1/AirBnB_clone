#!/usr/bin/python3
import cmd
import sys
import shlex
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
import models
import json

classes = {'BaseModel': BaseModel, 'User': User, 'State': State, 'City': City,
           'Amenity': Amenity, 'Place': Place, 'Review': Review}


class HBNBCommand(cmd.Cmd):
    """Console"""
    prompt = "(hbtn) "

    def do_EOF(self, args):
        """ Console exit when EOF\n """
        return (True)

    def do_quit(self, args):
        """ Console quit Builtin\n """
        return (True)

    def emptyline(self):
        """ Does not perform any action """
        return (False)

    def do_create(self, args):
        """
        Creates an object using the BaseModel
        eval the class if it exist or not
        var = eval("BaseModel()") is the same as var = Basemodel()
        """
        if args is None or len(args) == 0:
            print("** class name missing **")
        else:
            if args in classes:
                new = eval(str(args) + "()")
                new.save()
                print(new.id)
            else:
                print("** class doesn't exist **")

    def do_show(self, args):
        """
        Prints the string representation of an instance
        based on the class name and id
        eval the class if it exist or not
        var = eval("BaseModel") is the same as var = Basemodel()
        use of split in order to get tokens or args
        """
        if args is None or len(args) == 0:
            print("** class name missing **")
        else:
            line = args.split()

            if len(line) < 2:
                print("""** instance id missing **""")
            else:
                try:
                    objects = models.storage.all()
                    key = str(line[0]) + "." + str(line[1])
                    if key in objects:
                        print(objects[key])
                    else:
                        print("** no instance found **")
                except:
                    print("** class doesn't exist **")

    def do_destroy(self, args):
        """
        delete the object: the dictionary of dictionaries with storage.all()
        using alias with variable objects, and remove the key specified from
        objects where modifies at the same time self.__objects Cuz is an alias
        and finally update json file with storage.save()
        """
        if args is None or len(args) == 0:
            print("** class name missing **")
        else:
            line = args.split()

            if len(line) < 2:
                print("""** instance id missing **""")
            else:

                try:
                    objects = models.storage.all()
                    key = str(line[0]) + "." + str(line[1])
                    if key in objects:
                        del(objects[key])
                        models.storage.save()
                    else:
                        print("** no instance found **")
                except:
                    print("** class doesn't exist **")

    def do_all(self, args):
        """
        Prints all string representation of all instances based or not
        on the class name
        we have to use str because we have to call the method __str__
        in order to print in the format that we need
        """
        objects = models.storage.all()
        objList = []
        if args is "":
            for key in objects:
                objList.append(str(objects[key]))
            print(objList)
        else:
            try:
                line = args.split()
                eval(line[0])
                for elem in objects:
                    aux = objects[elem].to_dict()
                    if aux['__class__'] == line[0]:
                        objList.append(str(objects[elem]))
                print(objList)
            except:
                print("** class doesn't exist **")

    def do_update(self, args):
        """
        Updates an instance based on the class name and id by adding
        or updating attribute
        """
        line = shlex.split(args)
        if len(line) == 0:
            print("** class name missing **")
        else:
            try:
                eval(str(line[0]))
            except:
                print("** class doesn't exist **")
                return
            if len(line) == 1:
                print("** instance id missing **")
            else:
                objects = models.storage.all()
                key = str(line[0]) + "." + str(line[1])
                if key not in objects:
                    print("** no instance found **")
                else:
                    if len(line) == 2:
                        print("** attribute name missing **")
                    else:
                        if len(line) == 3:
                            print("** value missing **")
                        else:
                            setattr(objects[key], line[2], line[3])
                            models.storage.save()

    def do_count(self, args):
        """Count the number of type of class"""
        print("vamos a contar!!")

    def default(self, args):
        """ Handle the prefix and replace all the symbols by spaces"""
        s = args.replace('.', ' ')
        s = s.replace('(', ' ')
        s = s.replace(')', '')
        # if there is a dictionary give it a & in order to get as a part
        # with the split
        s = s.replace('{', '&{')
        s = s.replace(',', '')
        s = s.split('&')
        # if there is a dictionary we get more than 1 elem in s
        # if not there only will be one elem
        # we made the shlex to the first elem in the split of s because is the
        # first part before the dictionary, and if exist a second elem or more
        # we add the second elem to line
        line = shlex.split(s[0])
        if len(s) > 1:
            line.append(s[1])
        # create a new list empty where we are going to save the partitions
        lista = ['', '', '', '', '']
        for i in range(len(line)):
            if i < 5:
                lista[i] = line[i]
        # create a string as comando that is going to be the
        # input of the functions
        aux = ""
        comando = aux
        for i in range(0, 5):
            if i != 1 and i != 4:
                comando = comando + aux + str(lista[i])
                aux = " "
            if i == 4 and lista[i] != '':
                comando = comando + aux + '\"'
                comando = comando + str(lista[i]) + '\"'
        # get the different functions depending of the line[1] part
        if line[1] == 'all':
            self.do_all(comando)
        elif line[1] == 'count':
            self.do_count(comando)
        elif line[1] == 'show':
            self.do_show(comando)
        elif line[1] == 'destroy':
            self.do_destroy(comando)
        elif line[1] == 'update':
            # when we have update it could be a dictionary or the name and attr
            if lista[3] != '' and line[3][0] == '{' and line[3][-1] == '}':
                # if it is a dictionary we separate it by pairs
                line[3] = line[3].replace('{', ' ')
                line[3] = line[3].replace('}', ' ')
                line[3] = line[3].replace(': ', ':')
                sub = shlex.split(line[3])
                # then each pair we split it in a list, and we create tuples
                # and with these tuples we create a list of tuples in order
                # to create a dictionary with dict function
                new_list = []
                for elem in sub:
                    # we take care of spaces thas why we use & in order to get
                    # both parts
                    elem = elem.replace(':', '&')
                    sub2 = elem.split('&')
                    if len(sub2) < 2:
                        sub2.append('')
                    new_list.append(tuple(sub2))
                dicti = dict(new_list)
                # go through the dictionary and create the comando string
                # to send it into the function for the creation of the key
                # and the attr in the object
                for key in dicti:
                    lista[3] = key
                    lista[4] = dicti[key]
                    aux = ""
                    comando = aux
                    for i in range(0, 5):
                        if i != 1 and i != 4:
                            comando = comando + aux + str(lista[i])
                            aux = " "
                        if i == 4 and lista[i] != '':
                            comando = comando + aux + '\"'
                            comando = comando + str(lista[i]) + '\"'
                    self.do_update(comando)
            else:
                self.do_update(comando)
        else:
            return cmd.Cmd.default(self, args)

if __name__ == '__main__':
    """ Main """
    console = HBNBCommand()
    console.cmdloop()
