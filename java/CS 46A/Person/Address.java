/**
   Describes a mailing address.
*/
public class Address
{  
   /**
      Constructs a mailing address. 
      @param aStreet the street
      @param aCity the city
      @param aState the two-letter state code
      @param aZip the ZIP postal code
   */
   public Address(String aStreet, String aCity, String aState, String aZip)
   {  
      street = aStreet;
      city = aCity;
      state = aState;
      zip = aZip;
   }   

   /**
      Formats the address.
      @return a string containing the address in mailing list format
   */
   public String format()
   {  
      return street + "\n"
            + city + ", " + state + " " + zip;
   }
   
   private String street;
   private String city;
   private String state;
   private String zip;
}