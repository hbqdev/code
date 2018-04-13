import java.awt.BasicStroke;
import java.awt.Dimension;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.Rectangle;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.awt.image.BufferedImage;
import java.awt.print.PageFormat;
import java.awt.print.Printable;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.concurrent.Semaphore;
import javax.imageio.ImageIO;
import javax.print.DocFlavor;
import javax.print.DocPrintJob;
import javax.print.PrintException;
import javax.print.PrintService;
import javax.print.SimpleDoc;
import javax.print.StreamPrintServiceFactory;
import javax.print.attribute.HashPrintRequestAttributeSet;
import javax.print.attribute.PrintRequestAttributeSet;
import javax.swing.JComponent;
import javax.swing.JFileChooser;
import javax.swing.JFrame;
import javax.swing.JMenu;
import javax.swing.JMenuBar;
import javax.swing.JMenuItem;
import javax.swing.KeyStroke;
import org.alice.apis.moveandturn.*;
import org.alice.apis.moveandturn.gallery.environments.grounds.GrassyGround;

public abstract class RobotScene extends Scene
{
    private DirectionalLight sunLight = new DirectionalLight();
    private GrassyGround grassyGround = new GrassyGround();
    private SymmetricPerspectiveCamera camera = new SymmetricPerspectiveCamera();

    public RobotScene()
    {
        performSetUp();
    }

    public SymmetricPerspectiveCamera getCamera()
    {
        return camera;
    }

    public void performSetUp()
    {
        performSceneEditorGeneratedSetUp();
        performCustomPropertySetUp();
    }

    public void draw(Graphics2D g2) {
        for (Composite match : findAllMatches()) {
            if (match instanceof Beeper)
                ((Beeper) match).draw(g2);
            else if (match instanceof Wall)
                ((Wall) match).draw(g2);
            else if (match instanceof Robot)
                ((Robot) match).draw(g2);
        }
    }

    protected void showScene(final int xmin, final int ymin,
            final int xmax, final int ymax)
    {
        final int GRID_SIZE = 50;
        final JFrame frame = new JFrame();
        final JComponent component = new JComponent() {
            public void paintComponent(Graphics g) {
                Graphics2D g2 = (Graphics2D) g;
                g2.scale(GRID_SIZE, GRID_SIZE);
                g2.translate(-xmin + 1, -ymin + 1);
                g2.setStroke(new BasicStroke(1.0F / GRID_SIZE));
                g2.setColor(java.awt.Color.LIGHT_GRAY);
                for (int i = xmin - 1; i <= xmax; i++) {
                    g2.drawLine(i, ymin - 1, i, ymax);
                }
                for (int i = ymin - 1; i <= ymax; i++) {
                    g2.drawLine(xmin - 1, i, xmax, i);
                }


                g2.setColor(java.awt.Color.BLACK);


                draw(g2);
            }
            public Dimension getPreferredSize() {
                return new Dimension((xmax - xmin + 1) * GRID_SIZE,
                        (ymax - ymin + 1) * GRID_SIZE);
            }
        };
        frame.add(component);
        JMenuBar menuBar = new JMenuBar();
        frame.setJMenuBar(menuBar);
        JMenu menu = new JMenu("File");
        menu.setMnemonic('F');
        menuBar.add(menu);
        JMenuItem item = new JMenuItem("Save", 'S');
        menu.add(item);
        item.setAccelerator(KeyStroke.getKeyStroke("ctrl S"));
        item.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent event) {
                JFileChooser chooser = new JFileChooser();
                if (chooser.showOpenDialog(frame) == JFileChooser.APPROVE_OPTION)
                    try {
                        saveImage(component, chooser.getSelectedFile().getPath());
                    } catch (Exception ex) {
                        ex.printStackTrace();
                    }
            }
        });
        final Semaphore sem = new Semaphore(0);
        item = new JMenuItem("Exit", 'X');
        menu.add(item);
        item.setAccelerator(KeyStroke.getKeyStroke("ctrl X"));
        item.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent event) {
                frame.setVisible(false);
                sem.release();
            }
        });
        frame.addWindowListener(new WindowAdapter() {
           public void windowClosing(WindowEvent event) {
               frame.setVisible(false);
                sem.release();
           }
        });

        frame.pack();
        frame.setVisible(true);
        try {
            sem.acquire();
        } catch (InterruptedException ex) {
        }
    }
    
    private static void saveImage(final JComponent comp, String fileName) throws IOException, PrintException {
        if (fileName.endsWith(".ps")) {
            DocFlavor flavor = DocFlavor.SERVICE_FORMATTED.PRINTABLE;
            String mimeType = "application/postscript";
            StreamPrintServiceFactory[] factories = StreamPrintServiceFactory.lookupStreamPrintServiceFactories(flavor, mimeType);

            FileOutputStream out = new FileOutputStream(fileName);
            if (factories.length > 0) {
                PrintService service = factories[0].getPrintService(out);

                SimpleDoc doc = new SimpleDoc(new Printable() {
                    public int print(Graphics g, PageFormat pf, int page) {
                        if (page >= 1) return Printable.NO_SUCH_PAGE;
                        else {
                            System.out.println(comp.getWidth());
                            System.out.println(comp.getHeight());
                            System.out.println(pf.getImageableWidth());
                            System.out.println(pf.getImageableHeight());
                            System.out.println(pf.getWidth());
                            System.out.println(pf.getHeight());

                            double sf1 = pf.getImageableWidth() / (comp.getWidth() + 1);
                            double sf2 = pf.getImageableHeight() / (comp.getHeight() + 1);
                            double s = Math.min(sf1, sf2);
                            Graphics2D g2 = (Graphics2D) g;
                            g2.translate((pf.getWidth() - pf.getImageableWidth()) / 2, (pf.getHeight() - pf.getImageableHeight()) / 2);
                            g2.scale(s, s);

                            comp.paint(g);
                            return Printable.PAGE_EXISTS;
                        }
                    }
                }, flavor, null);
                DocPrintJob job = service.createPrintJob();
                PrintRequestAttributeSet attributes = new HashPrintRequestAttributeSet();
                job.print(doc, attributes);
            }
        } else {
            Rectangle rect = comp.getBounds();
            BufferedImage image = new BufferedImage(rect.width, rect.height, BufferedImage.TYPE_INT_RGB);
            Graphics g = image.getGraphics();
            comp.paint(g);
            String extension = fileName.substring(fileName.lastIndexOf('.') + 1);
            ImageIO.write(image, extension, new File(fileName));
            g.dispose();
        }
    }

    public abstract void performCustomPropertySetUp();

    /*
     * x = left to right
     * y = bottom to top
     * z = front to back
     * Quaternions x y z w
     * Unit quaternion (0 0 0 1)
     * Rotation about x with angle a (sin(a/2), 0, 0, cos(a/2))
     * Rotation about y with angle a (0, sin(a/2), 0, cos(a/2))
     * Rotation about z with angle a (0, 0, sin(a/2), cos(a/2))
     */
    protected void performSceneEditorGeneratedSetUp() {
        this.setName("scene");
        this.setAtmosphereColor(new Color(0.5, 0.5, 1.0));
        this.sunLight.setName("sunLight");
        this.sunLight.setLocalPointOfView(new PointOfView(new Quaternion(-0.7071067811865475, 0.0, 0.0, 0.7071067811865476), new Position(0.0, 0.0, 0.0)));
        this.addComponent(this.sunLight);
        this.grassyGround.setName("grassyGround");
        this.grassyGround.setLocalPointOfView(new PointOfView(new Quaternion(0.0, 0.0, 0.0, 1.0), new Position(0.0, 0.0, -0.0)));
        this.addComponent(this.grassyGround);
        this.camera.setName("camera");
        double yCameraAngle = Math.toRadians(10.0);
        double xCameraAngle = Math.toRadians(-20.0);
        double sx = Math.sin(xCameraAngle / 2);
        double cx = Math.cos(xCameraAngle / 2);
        double sy = Math.sin(yCameraAngle / 2);
        double cy = Math.cos(yCameraAngle / 2);

        this.camera.setLocalPointOfView(new PointOfView(
                new Quaternion(sx*cy, cx*sy, sx*sy, cx*cy),
                new Position(8, 4, 16.0)));
        this.addComponent(this.camera);
    }

    public abstract void run();
}
