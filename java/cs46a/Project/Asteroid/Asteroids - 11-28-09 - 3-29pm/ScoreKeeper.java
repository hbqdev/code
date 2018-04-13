/**
 * Construct  a class that keeps track of the score 
 * 
 * @author (Tin Tran) 
 */
public class ScoreKeeper
{
  
       public ScoreKeeper(int lives)
    {
        currentlives = lives;
        Score = 0;
        
        bonus = 1;
    }
    
    /**
     * counts the score
     * @para aScore the current score
     */
    public void addScore(int aScore)
    {
        Score +=aScore;
    }
/**
 * returns the score
  */
    public int getScore()
    {
        return Score;
    }
    
      /**
     * Decrease the current lives of the ship
     */
    public void lostLife()
    {
        currentlives--;
    }
    
    /**
     * returns the current lives of the ship
     */
    public int getLives()
    {
        return currentlives;
    }
    
    public void setBonus(int bonus)
    {
        this.bonus = bonus;
    }
    
    public int getBonus()
    {
        return bonus;
    }
    
  
   private int Score;
   private int currentlives;
   private int bonus;
}