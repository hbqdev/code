import javax.swing.JFrame;

public class BullsEyeViewer
{
   public static void main(String[] args)
   {
      JFrame frame = new JFrame();

      frame.setSize(300, 400);
      frame.setTitle("Bulls eye");
      frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

     BullsEyeComponent component = new BullsEyeComponent();
      frame.add(component);

      frame.setVisible(true);
   }
}
