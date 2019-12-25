import urllib.request

def get_input(day,year):
    url = "https://adventofcode.com/%4i/day/%i/input" %(year,day)
    opener = urllib.request.build_opener()
    opener.addheaders.append(('Cookie', 'session=53616c7465645f5f4652ae8b0dbce244ab28bb254b5f20b632a1058d5963f5d7cdf713b27a9fe5adc7ba293417bac760'))
    f = opener.open(url)
    input = str(f.read()).split("\\n")
    input[0] = input[0][2:]
    return input[:-1]
