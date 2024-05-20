def out(text, color: int=38, *args, output=True) -> str:
    combine = f"\033[{color}m{text}"
    for i in range(int(len(args)/2)):
        combine += f"\033[{args[i*2+1]}m{args[i*2]}"
    combine += "\033[0m"
    
    if output:
        print(combine)
    return combine


def inp(text, color: int=38, *args) -> any:
    return input(out(text, color, *args, output=False))
    

def options(reach: int=100) -> None:
    for i in range(range):
        out(i, i)
