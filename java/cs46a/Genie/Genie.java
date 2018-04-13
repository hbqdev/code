/**
   A Genie will grant 3 wishes.
*/
public class Genie
{
   /**
      Constructs a genie, who will grant 3 wishes.
   */
   public Genie()
   {
      grantedWishes = 0;
   }

   /**
      The genie accepts or rejects your wish.
      If you have not yet used 3 wishes, he claims to grant it, otherwise
      he threatens you.
      @param wish Your wish
   */
   public void grant(String wish)
   {
      if (grantedWishes <= TOTAL_WISHES)
         System.out.println("Your wish (" + wish + ") is my command!");
      else
         System.out.println("I smite thee for greed!");
   }

   public static int TOTAL_WISHES = 3;

   private int grantedWishes;
}