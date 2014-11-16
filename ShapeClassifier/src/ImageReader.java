/*
 * http://www.tutorialspoint.com/java_dip/understand_image_pixels.htm
 * 
 */

import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.*;
import javax.imageio.ImageIO;
import javax.swing.JFrame;
class ImageReader {
   BufferedImage  image;
   int width;
   int height;
   public ImageReader() {
      try {
         File input = new File("/Users/aakash/Desktop/ap_mugshot.jpg");
         image = ImageIO.read(input);
         width = image.getWidth();
         height = image.getHeight();
         int count = 0;
         for(int i=0; i<height; i++){
            for(int j=0; j<width; j++){
               count++;
               Color c = new Color(image.getRGB(j, i));
               System.out.println("S.No: " + count + " Red: " + c.getRed() +
               " Green: " + c.getGreen() + " Blue: " + c.getBlue());
               }
            }
      } catch (Exception e) {}
   }
   static public void main(String args[]) throws Exception 
   {
	   ImageReader obj = new ImageReader();
   }
}
