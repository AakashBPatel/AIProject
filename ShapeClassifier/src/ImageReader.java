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
   int width;
   int height;
   int data[][];
   public ImageReader(String filename) {
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
               System.out.println("S. No: " + count + " Value: " + data[i][j]);
               }
            }
      } catch (Exception e) {}
   }
   
   public int[][] getData(){
	   return data;
   }
}
