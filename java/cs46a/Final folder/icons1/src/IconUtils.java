
import java.awt.Component;
import java.awt.Graphics;
import java.awt.Image;
import java.awt.Toolkit;
import javax.swing.Icon;
import javax.swing.ImageIcon;
import javax.swing.JComponent;
import javax.swing.JFrame;

public class IconUtils
{
   /**
      Paints the icons, starting with x = 0 and lining them up horizontally with no gaps between them.
      @param icons an array of objects that belong to classes implementing the Icon interface
      @comp the component on which the icons are drawn. (Simply pass it along to the paintIcon method.)
   */
   public static void paintIconsHorizontally(Icon[] icons, Component comp, Graphics g)
   {

   }

   // This method makes a frame with a component that calls your method
   // with an array of three objects that belong to classes implementing
   // the Icon interface. You need not look inside the method.
   public static void main(String[] args)
   {
      final Icon[] myIcons = new Icon[3];
      Image img = Toolkit.getDefaultToolkit().getImage(
         IconUtils.class.getResource("eiffel-tower.gif"));
      myIcons[0] = new MarsIcon(50);
      myIcons[1] = new ImageIcon(img);
      myIcons[2] = new CarIcon(200);

      JFrame frame = new JFrame();
      JComponent comp = new JComponent()
      {
         public void paintComponent(Graphics g)
         {
            paintIconsHorizontally(myIcons, this, g);
         }
      };
      frame.add(comp);
      frame.setSize(500, 300);
      frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
      frame.setVisible(true);
   }
}