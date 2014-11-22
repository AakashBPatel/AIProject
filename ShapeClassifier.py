import neural

image_data = [];

images = eval(input())
for image in range(images):
	height = eval(input());
	width = eval(input());
	temp = []
	for x in range(height*width):
		temp.append(eval(input()))
	image_data.append(temp)

# Make training array and network