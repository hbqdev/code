import java.util.ArrayList;
import javax.swing.JFrame;
import java.util.Random;


/**
 * GameEngine runs the Asteroids game using all available classes.
 * 
 * @author Zane Melcho
 * @version 0.0.1
 */
public class GameEngine
{
    public static void main(String[] args)
    {
        JFrame frame = new JFrame();

        final int FRAME_WIDTH = 1280;
        final int FRAME_HEIGHT = 768;

        frame.setSize(FRAME_WIDTH, FRAME_HEIGHT);
        frame.setResizable(false);
        frame.setTitle("Asteroids");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        
        Random r = new Random();
        boolean playAgain = true;
        
        while(playAgain)
        {
            // Initial Variables
//ZShip            Ship firefly = new Ship(FRAME_WIDTH / 2, FRAME_HEIGHT / 2, 90, FRAME_WIDTH, FRAME_HEIGHT);
            Ship firefly = new Ship(FRAME_WIDTH / 2, FRAME_HEIGHT / 2, 270, .05, 4.5, FRAME_WIDTH, FRAME_HEIGHT);
            ArrayList<Bullet> bulletList = new ArrayList<Bullet>();
            ArrayList<Asteroid> asteroidList = new ArrayList<Asteroid>();
            ArrayList<Drawable> drawableList = new ArrayList<Drawable>();
            ArrayList<ScoreKeeper> scoreList = new ArrayList<ScoreKeeper>();
            ScoreKeeper currentScore = new ScoreKeeper(10);
            CollisionDetector ruth = new CollisionDetector();
            int level = 0;
                        
            // Sets up the Components to be drawn
            AsteroidsComponent asteroidsComponent = new AsteroidsComponent(drawableList);
            asteroidsComponent.setDoubleBuffered(true);
            asteroidsComponent.addKeyListener(new KeyCatcher());
            frame.add(asteroidsComponent);
            asteroidsComponent.setFocusable(true);
            frame.setVisible(true);
            
            Background bg = new Background();
            
            
            SoundEffect.init();
            //SoundEffect.TITLE.play();
            //SoundEffect.volume = SoundEffect.Volume.MUTE;
            
            //Beginning of game after Title Screen
            boolean gameOver = false;
            //SoundEffect.TITLE.stop();


            while(!gameOver)
            {
                SoundEffect.THEME.loop();
                // If all asteroids are destroyed start next level with more asteroids
                if (asteroidList.size() == 0)
                {
                    level++;
                    for (int k = 0; k < STARTING_ASTEROIDS + level; k++)
                    {
                        int asteroidX = r.nextInt(frame.getWidth() / 3);
                        if (r.nextInt(2) == 0)
                            asteroidX = asteroidX + 2 *( frame.getWidth() / 3); // Ensures the middle section has no asteroids
                        
                        int asteroidY = r.nextInt(frame.getHeight() - 20);
                        
                        int asteroidAngle = r.nextInt(360);
                        
                        asteroidList.add(new Asteroid(asteroidX, asteroidY, asteroidAngle, LARGE, frame.getWidth(), frame.getHeight()));
                    }  
                }
                
                // **********************************
                // **** Check for Key Presses  ***
                // **********************************
                if (KeyCatcher.spacePressed()) //Space bar
                {
                    // Check to see if the number of bullets fired is less than the max 
                    // Check to see if the time between shots is sufficient 
                    // If both are true a bullet is fired.
                    if (bulletList.size() < BULLET_MAX && Bullet.getTimeSinceLastBullet() >= BULLET_DELAY)
                    {
//ZShip                        bulletList.add(new Bullet(firefly.getX(), firefly.getY(),firefly.getSpeed(), -firefly.getAngle(), FRAME_WIDTH, FRAME_HEIGHT));    
                        bulletList.add(new Bullet(firefly.getX(), firefly.getY(), firefly.getMiddleX(), firefly.getMiddleY(), firefly.getVelocity(), firefly.getAngleOfDirection(), FRAME_WIDTH, FRAME_HEIGHT));    

                        SoundEffect.PHASER.play();
                    }
                    
                } 
               
                 if (KeyCatcher.upPressed()) // Up
                 {
                     firefly.thrust();
                     SoundEffect.THRUST.play();
                 }
                else
                SoundEffect.THRUST.stop();

                if (KeyCatcher.leftPressed()) //Left
                {
                    firefly.rotateShip(LEFT);
                }
                 
                if (KeyCatcher.rightPressed()) //Right
                {
                    firefly.rotateShip(RIGHT);
                }
                 
                if (KeyCatcher.downPressed()) //Down
                    firefly.hyperSpace();
                
                //Test to verify what happens when all asteroids are destroyed    
                /*
                if (asteroidList.size() > 0)
                    asteroidList.remove(0);
                */
               
                // **************************
                // **** Move all objects ****
                // **************************
                firefly.move();
                
                for (Asteroid asteroid : asteroidList)
                    asteroid.move();
                
                for (Bullet bullet : bulletList)
                    bullet.move();
                
                // ****** Fix this for wrap Around ********
                // If the bullet travels past a certain distance the bullet is removed from the arrayList
                for (int i = 0; i < bulletList.size(); i++)
                {      
                   if (bulletList.get(i).distanceTraveled() > BULLET_DISTANCE)
                    bulletList.remove(i);
                }
                
//************************************************************                
// **********    Check for Collisions   ***********************
//************************************************************
                //Checks for Bullets colliding with Asteroids
                for(int i = 0; i < bulletList.size(); i++)
                {
                     for(int k = 0; k < asteroidList.size(); k++)
                     {
                         // Checks if bullet has hit a asteroid
                         if (ruth.checkCollision(asteroidList.get(k).getBoundary(), bulletList.get(i).getBoundary()))
                         {
                             currentScore.addScore(asteroidList.get(k).getPoints());
                             asteroidList.get(k).getAngle();
                             
                             //Adds two new MEDIUM asteroids if asteroid shot was LARGE
                             if(asteroidList.get(k).getSize() == 3)
                             {
                                 int newAngle = r.nextInt(15) + 6;
                                 for (int j = 0; j < 2; j++)
                                    {
                                        asteroidList.add(new Asteroid(asteroidList.get(k).getX() + 10, asteroidList.get(k).getY() + 10, asteroidList.get(k).getAngle() + newAngle, MEDIUM, frame.getWidth(), frame.getHeight()));
                                        newAngle = newAngle * -1;
                                    }
                             }
                             //Adds two new SMALL asteroids if asteroid shot was LARGE
                             else if(asteroidList.get(k).getSize() == 2)
                             {
                                 int newAngle = r.nextInt(15) + 6;
                                 for (int j = 0; j < 2; j++)
                                    {
                                        asteroidList.add(new Asteroid(asteroidList.get(k).getX() + 15, asteroidList.get(k).getY() + 15, asteroidList.get(k).getAngle() + newAngle, SMALL, frame.getWidth(), frame.getHeight()));
                                        newAngle = newAngle * -1;
                                    }
                             }
                             SoundEffect.EXPLODE.play();
                             asteroidList.remove(k);
                            
                             bulletList.remove(i);
                             if (i > 0 && bulletList.size() > 1)
                                 i--;
                             k = asteroidList.size();
                         }      
                     }
                 }
//**************************************************************************************************                
                 
                
                // Updates
                Bullet.incrementBulletDelayTime();

                //Clear and  Copy all Drawable objects to the drawableList
                int listSize = drawableList.size();
                for (int i = 0; i < listSize; i++)
                    drawableList.remove(0);
                
                drawableList.add(bg);
                
                for (Asteroid asteroid : asteroidList)
                    drawableList.add(asteroid);
                    
                for (Bullet bullet : bulletList)
                    drawableList.add(bullet);
                
                

                drawableList.add(firefly);
                    
                asteroidsComponent.paintImmediately(asteroidsComponent.getX(), asteroidsComponent.getY(), asteroidsComponent.getWidth(), asteroidsComponent.getHeight());

                Pause.pause(10);
                
                
            }
            
        }
        
    }
    
    // Constant Variables
    public static final int RIGHT = 2;
    public static final int LEFT = -2;
    public static final int LARGE = 3;
    public static final int MEDIUM = 2;
    public static final int SMALL = 1;
    public static final int STARTING_ASTEROIDS = 3;
    public static final int BULLET_DISTANCE = 400;
    public static final int BULLET_MAX = 7;
    public static final int BULLET_DELAY = 25;
    public static final int BLACK = 1;
    public static final int RED = 2;
    public static final int GREEN= 3;
}
