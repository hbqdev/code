/**
 * Created by HBQ on 10/29/2016.
 */
import java.util.*;

public class calbmi {

    public static double calbmi(double weight, double height) {
        return weight/height;
    }


    public static void main (String[]args) {
        double weight = 90;
        double height = 1.8;

        double bmi = calbmi(weight, height);
        System.out.println(bmi);
    }

}
