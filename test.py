ss = """I figured it out
I figured it out from black and white
Seconds and hours
Maybe they had to take some time"""

words = ss.split()
d = {}
for w in ss.split():
    d[w] = d.get(w,0) + 1
print (d)
d.setdefault(0)

a = 5
b = 2
c = 5//2
print(c)