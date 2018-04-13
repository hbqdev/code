/**
 * Construct a class quiz that calculate the average score
 */
public class Quiz implements Measurable
{
/**
 * Construct a quiz
 * @para 
 */
public Quiz (double score, String grade)
{
ascore = score;
agrade= grade;
}
public double getScore()
{
return ascore;
}
public String getGrade()
{
return agrade;
}
   public double getMeasure()
   {
       return ascore;
    }
    
      private double ascore;
     private String agrade;
    
}