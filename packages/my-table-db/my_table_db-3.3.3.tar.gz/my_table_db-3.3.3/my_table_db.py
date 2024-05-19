__all__ = ['my_table_db']
def my_table_db(name_arg1=None, arg1=None, name_arg2=None, arg2=None, name_arg3=None, arg3=None, arg4=None,
            name_arg4=None, name_arg5=None, arg5=None, name_arg6=None, arg6=None, name_arg7=None, arg7=None):
    if (name_arg1 and name_arg2 and name_arg3 and name_arg4 and name_arg5 and name_arg6 and name_arg7) is not None:
        return (
            f'{name_arg1}:{str(arg1):10}{'|':9}{name_arg2}:{str(arg2):10}{'|':9}{name_arg3}:{str(arg3):10}{'|':9}{arg4}:{str(name_arg4):10}{'|':9}{arg5}:{str(name_arg5):10}{'|':9}{arg6}:{str(name_arg6):10}{'|':9}{arg7}:{str(name_arg7):10}')
    elif (name_arg1 and name_arg2 and name_arg3 and name_arg4 and name_arg5 and name_arg6) is not None:
        return (
            f'{name_arg1}:{str(arg1):10}{'|':9}{name_arg2}:{str(arg2):10}{'|':9}{name_arg3}:{str(arg3):10}{'|':9}{arg4}:{str(name_arg4):10}{'|':9}{arg5}:{str(name_arg5):10}{'|':9}{arg6}:{str(name_arg6):10}')
    elif (name_arg1 and name_arg2 and name_arg3 and name_arg4 and name_arg5) is not None:
        return (
            f'{name_arg1}:{str(arg1):10}{'|':9}{name_arg2}:{str(arg2):10}{'|':9}{name_arg3}:{str(arg3):10}{'|':9}{arg4}:{str(name_arg4):10}{'|':9}{arg5}:{str(name_arg5):10}')
    elif (name_arg1 and name_arg2 and name_arg3 and name_arg4) is not None:
        return (
            f'{name_arg1}:{str(arg1):10}{'|':9}{name_arg2}:{str(arg2):10}{'|':9}{name_arg3}:{str(arg3):10}{'|':9}{arg4}:{str(name_arg4):10}')
    elif (name_arg1 and name_arg2 and name_arg3) is not None:
        return (
            f'{name_arg1}:{str(arg1):10}{'|':9}{name_arg2}:{str(arg2):10}{'|':9}{name_arg3}:{str(arg3)}')
    elif (name_arg1 and name_arg2) is not None:
        return (
            f'{name_arg1}:{str(arg1):10}{'|':9}{name_arg2}:{str(arg2):10}')
    elif name_arg1 is not None:
        return (
            f'{name_arg1}:{str(arg1):10}')
