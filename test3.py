

list = ["a", "b", 1, 2.0]
list.append(True)
list.insert(4, False)
del(list[5])

print(list, len(list), list[4], sep="\n")

list2 = ["fehh", "non", "jashdk"]

list2.extend(list)

print(list2 + ['a'])