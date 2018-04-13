/** 
    A car can drive and consume fuel. 
*/ 
public class Car 
{ 
   /** 
      Constructs a car with a given fuel efficiency. 
      @param anEfficiency the fuel efficiency of the car 
   */ 
   public Car(double anEfficiency) 
   {
      efficiency = anEfficiency;
   }

   /** Adds gas to the tank. 
       @param amount the amount of fuel to add 
   */ 
   public void addGas(double amount) 
   { 
       gas+=amount;
   } 

   /** 
       Drives a certain amount, consuming gas. 
       @param distance the distance driven 
   */ 
   public void drive(double distance) 
   { 
       milesDriven += distance; 
        gas-= milesDriven/efficiency;
   } 

   /** 
       Gets the amount of gas left in the tank. 
       @return the amount of gas 
   */ 
   public double getGasInTank() 
   { 
      return gas;
   } 

   /** 
       Gets the total miles driven by this car. 
       @return the miles driven
   */ 
   public double getMilesDriven() 
   { 
      return milesDriven;
   } 
   private double milesDriven;
   private double gasintank;
   private double gas;
   private double efficiency;
} 