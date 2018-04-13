
import org.alice.apis.moveandturn.Program;

public class MyProgram extends Program
{
    private RobotScene scene;

    public MyProgram() 
    {
        scene = new MyScene();
    }

    protected void initialize()
    {
        setScene(scene);
    }

    protected void run()
    {
        scene.run();
    }

    public static void main(String[] args)
    {
        MyProgram myProgram = new MyProgram();
        myProgram.showInJFrame(args, true);
    }
}
