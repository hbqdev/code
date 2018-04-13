import java.util.ArrayList;

/**
   An itinerary holds a collection of city names.
*/
public class Itinerary
{
   /**
      Constructs an empty itinerary.
   */
   public Itinerary()
   {
       cities = new ArrayList<String>();
   }

   /**
      Add a city to the itinerary.
      @param cityName the city to add
   */
   public void addCity(String cityName)
   {
      cities.add(cityName); 
    }

   /**
      Returns a string describing the object.
      @return a string in the format "Itinerary[cityName1,cityName2,...]"
   */
   public String toString()
   {
      String cityName1 = "San Francisco";
      String cityName2 = "Denver";
      String cityName3 = "Chicago";

      String str = "Itinerary[" + (cities.get(0) + "," + cities.get(1)+ "," +
cities.get(2) + "," + cities.get(1)) + "]";
      return str;
   }

   /**
      Reverses the elements in the itinerary.
   */
   public void reverse()
   {
      ArrayList<String> reversed = new ArrayList<String>();
      for(int i = cities.size() - 1; i >= 0; i--)
         reversed.add(cities.get(i));
         reversed = cities;
   }

   private ArrayList<String> cities;
} 