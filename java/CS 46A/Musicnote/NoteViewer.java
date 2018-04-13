import javax.swing.JFrame;

public class NoteViewer
{
   public static void main(String[] args)
   {
      JFrame frame = new JFrame();
      frame.setSize(300, 100);
      frame.setTitle("Musical Note");
      frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
      NoteComponent component = new NoteComponent();
      frame.add(component);
      frame.setVisible(true);
   }
}
