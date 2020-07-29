import asyncio

async def find_divisible(inrange, div_by):
    print(f"Finding nums in range {inrange} divisible by {div_by}")
    located = list()
    for i in range(inrange):
        if i % div_by == 0:
            located.append(i)
    print(f"Done w/ nums in range {inrange} divisible by {div_by} ")
    return located

async def main():
    divs1 = find_divisible(508000000, 34113)
    divs2 = find_divisible(500, 3)
    divs3 = find_divisible(334343, 3)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    main()
