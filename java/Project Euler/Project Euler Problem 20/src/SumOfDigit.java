public class SumOfDigit
{
    // Evaluate n!
    public static long factorial( int n )
    {
        if( n <= 1 )     // base case
            return 1;
        else
            return n * factorial( n - 1 );
    }

    // Simple test program
    public static void main( String [ ] args )
    {
        for( int i = 1; i < 101; i++ )
            System.out.println( factorial( i ) );
    }
}
