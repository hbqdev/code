/**
      A student who is taking quizzes.
   */
   public class Student
   {

      /**
         Constructs a student with a given name.
         @param n the name
      */
      public Student(String n)
      {
         Name = n;
      }

      /**
         Gets the name of this student.
         @return the name
      */
      public String getName()
      {
         return Name;
      }

      /**
         Adds a quiz score.
         @param score the score to add
      */
      public void addQuiz(int score)
      {
         somescore = score;
      }

      /**
         Gets the sum of all quiz scores.
         @return the total score
      */
      public double getTotalScore()
      {
         return TotalScore;
      }

      /**
         Gets the average of all quiz scores.
         @return the average score
      */
      public double getAverageScore()
      {
         return AverageScore;
      }
      private String Name;
      private int somescore;
     private double TotalScore;
     private double AverageScore ;
   }
