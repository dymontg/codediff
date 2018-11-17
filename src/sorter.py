def sort(array):
    less = []
    equal = []
    greater = []

    if len(array) > 1:
        pivot = array[0][2]
        for x in array:
            if x[2] < pivot:
                less.append(x)
            if x[2] == pivot:
                equal.append(x)
            if x[2] > pivot:
                greater.append(x)
        return sort(less)+equal+sort(greater)

    else:
        return array