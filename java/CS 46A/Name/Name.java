public class Name
{
   /**
      Constructs a name.
      @param aFirst the first name of this name
      @param aMiddle the middle name of this name
      @param aLast the last name of this name
   */
   public Name(String aFirst, String aMiddle, String aLast)
   {
      first = aFirst;
      middle = aMiddle;
      last = aLast;
   }
   
   /**
      Gets the initials of this name
      @return a string consisting of the first character of the first, middle,
      and last name
   */
   public String getInitials()
   {
      return first.substring(0,1)+middle.substring(0,1)+last.substring(0,1);
   }
   
   private String first;
   private String middle;
   private String last;
}