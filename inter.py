s = "Hello world !!"
result = ":".join("{:02x}".format(ord(c)) for c in s)
print(result)