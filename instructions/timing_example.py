import resource


def gettime():
    rs = resource.getrusage(resource.RUSAGE_SELF)
    return rs[0] + rs[1]

t0 = gettime()
print(t0)

for i in range(100000):
    j = i * i * i

t1 = gettime()
print(t1)
print(t1 - t0)

j = 1
for i in range(100000):
    j = i * i * i * i * i

t2 = gettime()
print(t2)
print(t2 - t1)

j = 1
for i in range(100000):
    j = i ** 10

t3 = gettime()
print(t3)
print(t3 - t2)

j = 1
for i in range(100000):
    j = i ** 100

t4 = gettime()
print(t3)
print(t4 - t3)

# nothing

t5 = gettime()
print(t5)
print(t5 - t4)

print(t5 - t0)
