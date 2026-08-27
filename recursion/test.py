def show_steps_gcd(a, b, ctr=0):
    ctr += 1
    print("-"*20, "Level", ctr)
    print("new variable at", id(a))
    if b == 0:
       print("return a", a)
       return a
    else:
        print(f'{a} = {a // b} * ({b}) + {a % b}')
        print("calling show...")
        result=show_steps_gcd(b, a % b, ctr)
        print("return from", ctr, result, "=", id(result))
        return result
test = show_steps_gcd(234, 66)
print(test)