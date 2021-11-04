def read_simple_csv(filename):
    with open(f'E2/DB/{filename}.csv', 'r') as file:
        lines = file.readlines()
        list_ = []
        for a in lines:
            a = a[:-1]
            if a.isnumeric():
                a = int(a)
            list_.append(a)
        return list_


def read_dict_csv_int(filename):
    with open(f'E2/DB/{filename}.csv', 'r') as file:
        lines = file.readlines()
        dict_ = {}
        lines = lines[1:]
        for a in lines:
            a = a[:-1]
            a = a.split(',')
            dict_[a[0], a[1]] = int(a[2])
        return dict_


def read_dict_csv_float(filename):
    with open(f'E2/DB/{filename}.csv', 'r') as file:
        lines = file.readlines()
        dict_ = {}
        lines = lines[1:]
        for a in lines:
            a = a[:-1]
            a = a.split(',')
            dict_[a[0]] = float(a[1])
        return dict_
