#!/usr/bin/python3
"""
Command interpreter for Holberton AirBnB project
"""
import cmd
from models import base_model, user, storage, CNC, DNC
import os

BaseModel = base_model.BaseModel
User = user.User
FS = storage


class HBNBCommand(cmd.Cmd):
    """Command inerpreter class"""
    prompt = '(hbnb) '
    ERR = [
        '** class name missing **',
        "** class doesn't exist **",
        '** instance id missing **',
        '** no instance found **',
        '** attribute name missing **',
        '** value missing **',
        ]

    def preloop(self):
        """handles intro to command interpreter"""
        print(".----------------------------.")
        print("|    Welcome to hbnb CLI!    |")
        print("|   for help, input 'help'   |")
        print("|   for quit, input 'quit'   |")
        print(".----------------------------.")

    def postloop(self):
        """handles exit to command interpreter"""
        print(".----------------------------.")
        print("|  Well, that sure was fun!  |")
        print(".----------------------------.")

    def default(self, line):
        """default response for unknown commands"""
        pass

    def emptyline(self):
        """Called when an empty line is entered in response to the prompt."""
        pass

    def __class_err(self, arg):
        """private: checks for missing class or unknown class"""
        error = 0
        if len(arg) == 0:
            print(HBNBCommand.ERR[0])
            error = 1
        else:
            if arg[0] not in CNC:
                print(HBNBCommand.ERR[1])
                error = 1
        return error

    def __id_err(self, arg):
        """private checks for missing ID or unknown ID"""
        error = 0
        if (len(arg) < 2):
            error += 1
            print(HBNBCommand.ERR[2])
        if not error:
            fs_o = FS.all()
            for k, v in fs_o.items():
                temp_id = k.split('.')[1]
                if temp_id == arg[1] and arg[0] in k:
                    return error
            error += 1
            print(HBNBCommand.ERR[3])
        return error

    def do_airbnb(self, arg):
        """airbnb: airbnb
        SYNOPSIS: Command changes prompt string"""
        print("                      __ ___                        ")
        print("    _     _  _ _||\ |/  \ | _  _  _|_|_     _  _ _| ")
        print("|_||_)\)/(_|| (_|| \|\__/ || )(_)| |_| )\)/(_|| (_| ")
        print("   |                                                ")
        if HBNBCommand.prompt == '(hbnb) ':
            HBNBCommand.prompt = " /_ /_ _  /_\n/ //_// //_/ "
        else:
            HBNBCommand.prompt = '(hbnb) '
        arg = arg.split()
        error = self.__class_err(arg)

    def do_quit(self, line):
        """quit: quit
        USAGE: Command to quit the program
        """
        return True

    def do_EOF(self, line):
        """function to handle EOF"""
        print()
        return True

    def _parse_args(self, arg):
        """
        breaks up arguments class attribute arguments
        makes key value pair dict by delimitng at =
        """

        arg.pop(0)  # deletes first element of array of args

        # returns new dict with key value pairs from args
        new_dict = dict(s.split('=') for s in arg)
        for key, value in new_dict.items():
            str_value = value.strip('"').replace('_', ' ')
            flag = 1  # flag for checking negative int or float

            if '.' in str_value:  # checks if str_value is a float
                temp = str_value.split('.')
                if '-' in temp[0]:  # if negative inside string strips
                    temp[0] = temp[0].strip('-')
                    flag = 2
                # check if digit
                if temp[0].isdigit() is True and temp[1].isdigit() is True:
                    str_value = float(str_value)
                    if flag == 2:
                        str_value = -abs(str_value)
                    new_dict[key] = str_value
                    continue
            elif '-' in str_value:
                str_value = str_value.strip('-')
                flag = 2
            if str_value.isdigit() is True:   # checks if str_value is int
                str_value = int(str_value)
                if flag == 2:
                    str_value = -abs(str_value)
            new_dict[key] = str_value
        return new_dict

    def do_create(self, arg):
        """create: create [ARG]
        ARG = Class Name
        SYNOPSIS: Creates a new instance of the Class from given input ARG
        EXAMPLE: create City
                 City.create()
        """
        arg_list = arg.split()
        error = self.__class_err(arg_list)
        if not error:
            ''' instantiates object called at arg[0]'''
            ''' below this line code handles arguments after arg[0]
            arguments update dictionary with new key-pair values
            '''
            if os.getenv('HBNB_TYPE_STORAGE', 'fs') == 'db':
                for k, v in DNC.items():
                    if k == arg_list[0]:
                        my_obj = v()
                new_dict = self._parse_args(arg_list)
                # updates dictionary with new values pairs
                my_obj.__dict__.update(new_dict)
                my_obj.save()
                BaseModel(**my_obj.__dict__)
                print(my_obj.id)
            else:
                for k, v in CNC.items():
                    if k == arg_list[0]:
                        my_obj = v()
                new_dict = self._parse_args(arg_list)
                my_obj.__dict__.update(new_dict)
                my_obj.save()
                BaseModel(**my_obj.__dict__)
                print(my_obj.id)

    def do_show(self, arg):
        """show: show [ARG] [ARG1]
        ARG = Class
        ARG1 = ID #
        SYNOPSIS: Prints object of given ID from given Class
        EXAMPLE: show City 1234-abcd-5678-efgh
                 City.show(1234-abcd-5678-efgh)
        """
        arg = arg.split()
        error = self.__class_err(arg)
        if not error:
            error += self.__id_err(arg)
        if not error:
            fs_o = FS.all()
            for k, v in fs_o.items():
                if arg[1] in k and arg[0] in k:
                    print(v)

    def do_all(self, arg):
        """all: all [ARG]
        ARG = Class
        SYNOPSIS: prints all objects of given class
        EXAMPLE: all City
                 City.all()
        """
        arg = arg.split()
        error = 0
        if arg:
            error = self.__class_err(arg)
        if not error:
            print('[', end='')
            fs_o = FS.all()
            l = 0
            if arg:
                for v in fs_o.values():
                    if type(v).__name__ == CNC[arg[0]].__name__:
                        l += 1
                c = 0
                for v in fs_o.values():
                    if type(v).__name__ == CNC[arg[0]].__name__:
                        c += 1
                        print(v, end=(', ' if c < l else ''))
            else:
                l = len(fs_o)
                c = 0
                for v in fs_o.values():
                    print(v, end=(', ' if c < l else ''))
            print(']')

    def do_destroy(self, arg):
        """destroy: destroy [ARG] [ARG1]
        ARG = Class
        ARG1 = ID #
        SYNOPSIS: destroys object of given ID from given Class
        EXAMPLE: destroy City 1234-abcd-5678-efgh
                 City.destroy(1234-abcd-5678-efgh)
        """
        arg = arg.split()
        error = self.__class_err(arg)
        if not error:
            error += self.__id_err(arg)
        if not error:
            fs_o = FS.all()
            for k in fs_o.keys():
                if arg[1] in k and arg[0] in k:
                    del fs_o[k]
                    FS.save()

    def __rreplace(self, s, l):
        """replaces characters from input list with input string"""
        for c in l:
            s = s.replace(c, '')
        return s

    def __check_dict(self, arg):
        """checks if the arguments input has a dictionary"""
        if '{' and '}' in arg:
            l = arg.split('{')[1]
            l = l.split(', ')
            l = list(s.split(':') for s in l)
            d = {}
            for subl in l:
                k = subl[0].strip('"\' {}')
                v = subl[1].strip('"\' {}')
                d[k] = v
            return d
        else:
            return None

    def __handle_update_err(self, arg):
        """checks for all errors in update"""
        d = self.__check_dict(arg)
        arg = self.__rreplace(arg, [',', '"'])
        arg = arg.split()
        error = self.__class_err(arg)
        if not error:
            error += self.__id_err(arg)
        if not error:
            valid_id = 0
            fs_o = FS.all()
            for k in fs_o.keys():
                if arg[1] in k and arg[0] in k:
                    key = k
            if len(arg) < 3:
                print(HBNBCommand.ERR[4])
            elif len(arg) < 4:
                print(HBNBCommand.ERR[5])
            else:
                return [1, arg, d, fs_o, key]
        return [0]

    def do_update(self, arg):
        """update: update [ARG] [ARG1] [ARG2] [ARG3]
        ARG = Class
        ARG1 = ID #
        ARG2 = attribute name
        ARG3 = value of new attribute
        SYNOPSIS: updates or adds a new attribute and value of given Class
        EXAMPLE: update City 1234-abcd-5678-efgh name Chicago
                 City.update(1234-abcd-5678-efgh, name, Chicago)
        """
        arg_inv = self.__handle_update_err(arg)
        if arg_inv[0]:
            arg = arg_inv[1]
            d = arg_inv[2]
            fs_o = arg_inv[3]
            key = arg_inv[4]
            if not d:
                avalue = arg[3].strip('"')
                if avalue.isdigit():
                    avalue = int(avalue)
                fs_o[key].bm_update(arg[2], avalue)
            else:
                for k, v in d.items():
                    if v.isdigit():
                        v = int(v)
                    fs_o[key].bm_update(k, v)

    def do_BaseModel(self, arg):
        """class method with .function() syntax
        Usage: BaseModel.<command>(<id>)"""
        self.__parse_exec('BaseModel', arg)

    def do_Amenity(self, arg):
        """class method with .function() syntax
        Usage: Amenity.<command>(<id>)"""
        self.__parse_exec('Amenity', arg)

    def do_City(self, arg):
        """class method with .function() syntax
        Usage: City.<command>(<id>)"""
        self.__parse_exec('City', arg)

    def do_Place(self, arg):
        """class method with .function() syntax
        Usage: Place.<command>(<id>)"""
        self.__parse_exec('Place', arg)

    def do_Review(self, arg):
        """class method with .function() syntax
        Usage: Review.<command>(<id>)"""
        self.__parse_exec('Review', arg)

    def do_State(self, arg):
        """class method with .function() syntax
        Usage: State.<command>(<id>)"""
        self.__parse_exec('State', arg)

    def do_User(self, arg):
        """class method with .function() syntax
        Usage: User.<command>(<id>)"""
        self.__parse_exec('User', arg)

    def __count(self, arg):
        """counts the number objects in File Storage"""
        args = arg.split()
        fs_o = FS.all()
        count = 0
        for k in fs_o.keys():
            if args[0] in k:
                count += 1
        print(count)

    def __parse_exec(self, c, arg):
        """parses the input from .function() syntax, calls appropriate function
        """
        CMD_MATCH = {
            '.all': self.do_all,
            '.count': self.__count,
            '.show': self.do_show,
            '.destroy': self.do_destroy,
            '.update': self.do_update,
            '.create': self.do_create,
        }
        if '(' and ')' in arg:
            check = arg.split('(')
            new_arg = "{} {}".format(c, check[1][:-1])
            for k, v in CMD_MATCH.items():
                if k == check[0]:
                    if ((',' or '"' in new_arg) and k != '.update'):
                        new_arg = self.__rreplace(new_arg, ['"', ','])
                    v(new_arg)
                    return
        self.default(arg)

if __name__ == '__main__':
    """MAIN function"""
    HBNBCommand().cmdloop()
