import neural
import shlex, subprocess

def read_image(filepath):
	cmd = 'java -Dfile.encoding=UTF-8 -classpath "/Users/aakash/Sync/Artificial Intelligence/AIProject/ShapeClassifier/bin" ImageReader ' + filepath
	#print(cmd)
	args = shlex.split(cmd)
	output,error = subprocess.Popen(args,stdout = subprocess.PIPE, stderr= subprocess.PIPE).communicate()
	#print(output)
	raw = output.splitlines()

	height = eval(raw[1])
	width = eval(raw[2])
	#print(height)
	#print(width)
	temp = []
	for x in range(height*width):
		temp.append(eval(raw[x+3]))
	return temp

# Make training array and network