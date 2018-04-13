public class MyScene extends RobotScene 
{
    private Robot carol;

    // This method sets up the maze. Don't look inside.
    public void performCustomPropertySetUp()
    {
        carol = new Robot(2, 0);
        addComponent(carol);

        for (int i = 0; i < 10; i++)
        {
            addComponent(new Wall(i, 0, Wall.X_DIRECTION));
            if (i != 5)
                addComponent(new Wall(i, 10, Wall.X_DIRECTION));
            if (i < 7)
                addComponent(new Wall(i, 5, Wall.X_DIRECTION));
        }
        for (int i = 0; i < 10; i++)
        {
            addComponent(new Wall(0, i, Wall.Y_DIRECTION));
            addComponent(new Wall(10, i, Wall.Y_DIRECTION));
            if (i > 2 && i < 9)
                addComponent(new Wall(7, i, Wall.Y_DIRECTION));
        }

        addComponent(new Beeper(5, 10));
        carol.turnLeft();
    }

    public void run()
    {
        while (!carol.isOverBeeper())
            step();
    }

    public void step()
    {
      if (!carol.isOverBeeper())
      {
          if (carol.rightHasWall())
          {
              if (!carol.frontHasWall())
              {
              carol.moveForward();
               if (!carol.rightHasWall()
               {
                   if(!carol.isOverBeeper()
                   {
                       carol.turnRight();
                       carol.moveForward();
                       if (!carol.isOverBeeper()
                       {
                           carol.turnRight();
                           carol.moveForward();
                       }
                   }
               }
              }
              else
              {
                  carol.turnleft();
              }
          }
          
                       }
                   }
               }
              }
          }
      }

        carol.moveForward();
    }
}
