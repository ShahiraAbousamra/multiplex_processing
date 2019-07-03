import os
with open('patches.txt') as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
content = [x.strip('\n') for x in content] 
print(content)

for line in content:
  print(line)
  os.system('python registration_for_user '+line)
	