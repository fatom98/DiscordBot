def find_divisible(inrange, div_by):
    print(f"Finding nums in range {inrange} divisible by {div_by}")
    located = list()
    for i in range(inrange):
        if i % div_by == 0:
            located.append(i)
    print(f"Done w/ nums in range {inrange} divisible by {div_by} ")
    return located

def main():
    divs1 = find_divisible(508000, 34113)
    divs1 = find_divisible(500, 3)
    divs1 = find_divisible(334343, 3)

if __name__ == '__main__':
    main()
