from time import sleep


def progress(num=0, den=100, width=30):
    percent = num / den * 100
    left = width * num // den
    right = width - left
    print('\r[', '#' * left, ' ' * right, ']',
          f' {percent: .0f}%', sep='', end='', flush=True)

n = 1000
for i in range(n+1):
    progress(i, n)
    sleep(i/n)