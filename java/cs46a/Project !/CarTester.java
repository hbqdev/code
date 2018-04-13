/**
   This program tests the Car class.
*/
public class CarTester
{ 
   public static void main(String [] args)
   { 
      Car myHybrid = new Car(50); // 50 miles per gallon       
      myHybrid.addGas(20); 
      myHybrid.drive(50); // consumes 1 gallon      
      myHybrid.drive(50); // and another gallon      
      myHybrid.addGas(10);
      double gasLeft = myHybrid.getGasInTank();       
      System.out.print("Gas left: ");
      System.out.println(gasLeft);
      System.out.println("Expected: 28");
      System.out.print("Miles driven: ");
      System.out.println(myHybrid.getMilesDriven());
      System.out.println("Expected: 100");
   } 
}