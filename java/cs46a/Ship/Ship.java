import java.awt.geom.*;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.Rectangle;
import java.util.Random;
import java.awt.Image;
import javax.imageio.ImageIO;
import java.io.File;
import java.io.IOException;



public class Ship
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
 */
public Ship (double x, double y, int lives, double Acceleration, double maxSpeed, double fWidth, double fHeight)
{
            xcor = x;
            ycor = y;
            middlex = bound.getWidth()/2;
            middley = bound.getHeight()/2;
            acce =  Acceleration;
            topSpeed = maxSpeed;
            currentLives = lives;
            framex = fWidth;
            framey = fHeight;
            
      try 
      {
         image = ImageIO.read(new File("spaceship.png"));
        }
      catch (IOException ex)
      { 
         System.out.println("Can't read image.");
        } 
   }
        

/**
 * Rotate the Ship by an angle
 * @Para theta the angle that the Ship rorates
 */
public void rotate (double theta)
{
           angle = theta;
           angle +=(Math.PI)/12;
           xf = middlex;
           yf= ycor;
        }

/**
 * Return the X-Coordinate of the head of the Ship
  */
public double getFrontx()
{
            return xf;
        }

/**
 * Return the Y-Coordinate of the head of the Ship
  */
public double getFronty()
{
            return yf;
        }   

/**
 * Computes the angle of the Ship, the Velocity of the Ship
 */
public void thurs()
{
        angle1 = Math.atan((xf-middlex)/(yf-middley));
        double distant = ((xf-middlex)*(xf-middlex) + ((yf-middley)*(yf-middley)));
        xVelocity = distant*Math.cos(Math.toRadians(angle))*acce;
        yVelocity = distant*Math.sin(Math.toRadians(angle))*acce;
        Velocity = Math.sqrt(xVelocity*xVelocity + yVelocity*yVelocity);
            if (Velocity > topSpeed)
           {
               Velocity = topSpeed;
               xVelocity = Velocity*Math.cos(angle1);
               yVelocity = Velocity*Math.sin(angle1);
        }
    }

/**
 * Move the ship
 */
public void move()
{
    xf += xVelocity;
    yf +=yVelocity;
            }

/**
 * Return the velocity of the Ship
 */

public double ShipVelocity()
{
        return Velocity;
}

/**
 * Draws the boundary box
 * Draws the image
 */
public void draw(Graphics2D g2)
{
            g2.drawImage(image, (int)xcor,(int)ycor, null);
            Rectangle2D.Double ship = new Rectangle2D.Double (xcor,ycor, 10,10);
            g2.draw(ship);
            
             }
             


/**
 * Return the x-Coordinate of the Ship
 */
public double getX()
{
            return middlex;
}

/**
 * Return the y-Coordinate of the Ship
 */
public double getY()
{
            return middley;
}

/**
 * Returns the current lives of the Ship
 */
public int getLives()
{
            return currentLives;
}


Random hyper = new Random();

/**
 * Moves the Ship to Random location
  */
 public void hyperSpace()
{
            double width = framex - 0 - 10;
            double height = framey -0 -10;
            xcor = hyper.nextInt((int) width);
            ycor = hyper.nextInt((int) height);
}



private double xcor;
private double ycor;
private double middlex;
private double middley;
private double framex;
private double framey;
private double x2;
private double y2;
private double acce;
private double angle;
private double angle1;
private double xVelocity;
private double yVelocity;
private double Velocity;
private int currentLives;
private double topSpeed;
private double xf;
private double yf;
private Image image;
private Rectangle2D.Double bound;
}
