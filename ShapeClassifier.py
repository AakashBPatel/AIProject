import neural
import shlex, subprocess

SIZE = 15*15

def read_image(filepath):
	print("Reading image: " + filepath)
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
	print("Done.")
	return temp

def build_net1():
	network = [];
	input_layer = [];
	for i in range(SIZE):
		input_layer += [(neural.u(), neural.u())]
	#print(input_layer)
	hidden_layer = []
	for i in range((SIZE+5)//2+1):
		t = ()
		for j in range(SIZE+1):
			t += (neural.u(),)
		hidden_layer += [t]
	output_layer = []
	for i in range(5):
		print("Creating output neuron " + str(i))
		t = ()
		for j in range((SIZE+5)//2+1):
			t += (neural.u(),)
		output_layer += [t]
		print("Done.")
	network += [input_layer]
	network += [hidden_layer]
	network += [output_layer]
	return network

def build_net():
	network = []
	input_layer = []
	for i in range(3*(SIZE+5)//4):
		#print("Creating input neuron " + str(i))
		t = ()
		for j in range(SIZE+1):
			t += (neural.u(),)
		input_layer += [t]
	#print(input_layer)
	hidden_layer1 = []
	for i in range((SIZE+5)//2):
		#print("Creating output neuron " + str(i))
		t = ()
		for j in range(3*(SIZE+5)//4+1):
			t += (neural.u(),)
		hidden_layer1 += [t]
		print("Done.")
	hidden_layer2 = []
	for i in range((SIZE+5)//4):
		#print("Creating output neuron " + str(i))
		t = ()
		for j in range((SIZE+5)//2+1):
			t += (neural.u(),)
		hidden_layer2 += [t]
		print("Done.")
	output_layer = []
	for i in range(5):
		print("Creating output neuron " + str(i))
		t = ()
		for j in range((SIZE+5)//4+1):
			t += (neural.u(),)
		output_layer += [t]
		print("Done.")
	return [input_layer,hidden_layer1,hidden_layer2,output_layer]

# 1,0,0,0,0 is circle
# train_net(image_data, [[1,0,0,0,0],[0,1,0,0,0]])
def gen_training_data(image_array, input_array):
	print("Generating training data set")
	training_set = []
	
	for image in range(len(image_array)):
		out_dat = input_array[image]
		in_dat = image_array[image]
		in_dat += [out_dat]
		training_set += [in_dat]
	print("Done.")
	return training_set

def classify(path, net):
	image_data = [read_image(path)]
	output = neural.classify_new(net, image_data)
	summ = 0
	shape = 0
	maxx = 0
	for i in range(len(output)):
		summ += output[i]
		if(output[i]>maxx):
			maxx=output[i]
			shape=i
	prop = maxx/summ
	prop = (prop*100)/100
	if(shape==0):
		print("Shape is a Square with %s certainty" % (prop))
	elif(shape==1):
		print("Shape is a Plus with %s certainty" % (prop))
	elif(shape==2):
		print("Shape is a Triangle with %s certainty" % (prop))
	elif(shape==3):
		print("Shape is a Circle with %s certainty" % (prop))

	#output_layer = [neural.u(), neural.u(), neural.u(), neural.u(), neural.u()]
	#network

# Make training array and network

image_data = [read_image("/Users/aakash/Downloads/shapeyz/ss.png"),read_image("/Users/aakash/Downloads/shapeyz/sp.png"),read_image("/Users/aakash/Downloads/shapeyz/st.png"),read_image("/Users/aakash/Downloads/shapeyz/sc.png"),read_image("/Users/aakash/Downloads/shapeyz/sh.png")]
#image_data = [read_image("/Users/aakash/Downloads/shapeyz/ss.png")]
#training_data = gen_training_data(image_data, [[1,0,0,0,0]])
training_data = gen_training_data(image_data, [[1,0,0,0,0], [0,1,0,0,0],[0,0,1,0,0],[0,0,0,1,0],[0,0,0,0,1]])
temp = build_net()
net = neural.buildNet(temp[0], temp[1], temp[2], temp[3])
classified = neural.classify(net, training_data, 0.2,verbose=True)
#classify("/Users/aakash/Downloads/smallnoise.png", net)





