import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
 /**
  An action listener that prints a message.
 */
public class ClickListener implements ActionListener
 {
    public void actionPerformed(ActionEvent event)
   {
        count++;
        System.out.println("I was clicked " + count + " times" );
    }
    private int count;
}
