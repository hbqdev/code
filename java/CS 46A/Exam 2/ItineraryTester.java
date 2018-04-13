/**
   This class tests the Itinerary class.
*/
public class ItineraryTester
{
   public static void main(String[] args)
   {
      Itinerary it = new Itinerary();
      it.addCity("San Francisco");
      it.addCity("Denver");
      it.addCity("Chicago");
      it.addCity("Denver");
      
      System.out.println("Original itinerary: " + it.toString());
      System.out.println("Expected: Itinerary[San Francisco,Denver,Chicago,Denver]");
      it.reverse();
      System.out.println("Reversed itinerary: " + it.toString());
      System.out.println("Expected: Itinerary[Denver,Chicago,Denver,San Francisco]");
   }
}