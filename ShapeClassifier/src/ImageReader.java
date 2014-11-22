/*
 * http://www.tutorialspoint.com/java_dip/understand_image_pixels.htm
 * 
 */

import java.awt.Color;
import java.awt.image.BufferedImage;
import java.io.File;

import javax.imageio.ImageIO;
class ImageReader {
	BufferedImage  image;
	private int width;
	private int height;
	private int data[][];
	public ImageReader(String filename){
		try {
			File input = new File(filename);
			image = ImageIO.read(input);
			width = image.getWidth();
			height = image.getHeight();
			data = new int[height][width];
			int count = 0;
			for(int i=0; i<height; i++){
				for(int j=0; j<width; j++){
					count++;
					Color c = new Color(image.getRGB(j, i));
					// System.out.println("S.No: " + count + " Red: " + c.getRed() +
					// " Green: " + c.getGreen() + " Blue: " + c.getBlue());
					data[i][j] = (c.getBlue() + c.getRed() + c.getGreen()) > 700 ? 0:1;
					//System.out.println("S. No: " + count + " Value: " + data[i][j]);
				}
			}
		} catch (Exception e) {}
	}

	public int[][] getData(){
		return data;
	}
	public int getWidth(){
		return width;
	}
	public int getHeight(){
		return height;
	}
	// TODO WRIET NUMBER OF ARGS AS FIST THING
	public static void main(String args[]){
		System.out.println(args.length);
		for(int argslen = 0; argslen < args.length; argslen++){
			ImageReader image = new ImageReader(args[argslen]);
			System.out.println(image.getHeight());
			System.out.println(image.getWidth());
			for(int i = 0; i<image.getHeight(); i++){
				for(int j = 0; j < image.getWidth(); j++){
					System.out.println(image.getData()[i][j]);
				}
			}
		}
	}
}

