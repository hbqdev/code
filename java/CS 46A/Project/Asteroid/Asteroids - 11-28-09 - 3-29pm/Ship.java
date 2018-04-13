import java.awt.geom.*;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.Rectangle;
import java.util.Random;
import java.awt.Image;
import javax.imageio.ImageIO;
import java.io.File;
import java.io.IOException;



public class Ship implements Drawable
{
/**
 * Construct a class Ship 
 * @Para x X-coordinate of the ship
 * @Para y Y-Coordinate of the ship
 * @Para lives number of lives of the ship
 * @Para Acceleration the acceleration of the ship
 * @Para maxSpeed the maximum travel speed of the ship
 * @Para fWidth the width of the frame
 * @Para Height the height of the frame
 * @author Tin Tran
 * @Version  1.0
 */
public Ship (double x, double y,double anangle, double Acceleration, double maxSpeed, double fWidth, double fHeight)
{
            xcor = x;
            ycor = y;
            angle = anangle;
            acce =  Acceleration;
            topSpeed = maxSpeed;
            //currentLives = lives;
            framex = fWidth;
            framey = fHeight;
            
          
           
      try 
      {
         image = ImageIO.read(new File("hornet.png"));
        }
      catch (IOException ex)
      { 
         System.out.println("Can't read image.");
        } 
       
         try 
      {
         image2 = ImageIO.read(new File("hornet_thrust.png"));
        }
      catch (IOException ex)
      { 
         System.out.println("Can't read image.");
        } 
        
      ship = new Rectangle2D.Double(xcor+0.25*image.getWidth(null),ycor, image.getWidth(null)-0.5*image.getWidth(null),image.getHeight(null));  
        
   }
        

/**
 * Computes the angle of the Ship, the Velocity of the Ship
 */

/**
 * Rotate the Ship by an angle
 * @Para theta the angle that the Ship rorates
 */
public void rotateShip(double theta)
{
           angle += theta;
                     
        }

        
public void thrust()
{
        xVelocity += Math.cos(Math.toRadians(angle))*acce;
        yVelocity += Math.sin(Math.toRadians(angle))*acce;
        Velocity = getVelocity();
        
        angle1 = Math.toDegrees(Math.atan(yVelocity / xVelocity)); 
        if(xVelocity < 0) 
        angle1 += 180; 
        if(xVelocity > 0 && yVelocity < 0) 
            angle1 += 360;
            if (getVelocity()>topSpeed)
           {
               xVelocity = topSpeed*Math.cos(Math.toRadians(angle1));
               yVelocity = topSpeed*Math.sin(Math.toRadians(angle1));
               
        }
     isThrust = true;
    }

/**
 * Move the ship
 */
public void move()
{

        if (xcor >= framex)
        {
            xcor = -image.getWidth(null);   
        }
        else if (xcor <= -image.getWidth(null))
        {
            xcor = framex;
        }
        // Controls wrap around in the y-axis
        if (ycor >= framey)
        {
            ycor = -image.getWidth(null);   
        }
        else if (ycor <= -image.getWidth(null))
        {
            ycor = framey;
        }
    
     xcor += xVelocity;
    ycor +=yVelocity;
    
    
    
    xfront = xcor + image.getWidth(null)/2;
    yfront = ycor;
    
    middlex = xcor + image.getWidth(null) / 2;
    middley = ycor + image.getHeight(null) / 2;
    }

/**
 * Return the velocity of the Ship
 */

public double getVelocity()
{
        return Math.sqrt(xVelocity*xVelocity + yVelocity*yVelocity);
}

public void stopThrust()
{
    isThrust = false;
}

/**
 * Draws the boundary box
 * Draws the image
 */
public void draw(Graphics2D g2)
{
            ship = new Rectangle2D.Double (xcor+0.25*image.getWidth(null),ycor + image.getHeight(null) * .1, image.getWidth(null) * 0.475,image.getHeight(null) * .8);
            //g2.draw(ship);         
            
            
            AffineTransform identity = new AffineTransform();
            AffineTransform trans = new AffineTransform();       
            
            identity.translate(xcor,ycor);
            trans.setTransform(identity);
            trans.rotate(Math.toRadians(angle+90), image.getWidth(null) / 2, image.getHeight(null) / 2);

            if (isThrust)
            {
             g2.drawImage(image2, trans, null);
            }
       else 
          {
          g2.drawImage(image,trans,null);
        }
}
             

/**
 * Return the x-Coordinate of the Ship
 */
public double getX()
{
            return xcor;
          }

/**
 * Return the y-Coordinate of the Ship
 */
public double getY()
{
            return ycor;
}

/**
 * Returns the current lives of the Ship
 */

/**
 * returns the x-coordinate of the head of the ship
 */
public double getXFront()
{
return xfront;
}

/**
 * returns the y-coordinate of the head of the ship
 */
public double getYFront()
{
return yfront;
}

public double getMiddleX()
{
    return middlex;
}
public double getMiddleY()
{
    return middley;
}

Random hyper = new Random();

/**
 * Moves the Ship to Random location
  */
 public void hyperSpace()
{
            double width = framex - image.getWidth(null);
            double height = framey - image.getHeight(null);
            xcor = hyper.nextDouble() * width;
            ycor = hyper.nextDouble() * height;
            xVelocity =0;
            yVelocity =0;
}
/**
 * gets the current speed of the ship
 */
public double getSpeed()
{
    return Velocity;
}

/**
 * return the angle the ship is facing
 */
public double getAngleOfMotion() 
{
    return angle1;
}

/**
 * return the angle the ship is traveling
 */
public double getAngleOfDirection()
{
return angle;
}

public Rectangle2D.Double getBoundary()
{
    return ship;
}

private double xcor;
private double ycor;
private double middlex;
private double middley;
private double framex;
private double framey;
private double acce;
private double angle;
private double angle1;
private double xVelocity;
private double yVelocity;
private double xfront;
private double yfront;
private double Velocity;
private double topSpeed;
private Image image;
private Image image2;
private Rectangle2D.Double ship;
private boolean isThrust;
}
