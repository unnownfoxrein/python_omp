def factory(n):
    list_to_return = []

    for i in range(n):
        list_to_return.append(lambda: i)

    return list_to_return

if __name__ == "__main__":
    for func in factory(5):
        print(func())
