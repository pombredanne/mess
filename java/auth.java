/* This is the main backend class API, it must to the following tasks:
1) Authenticate user somewhere with user/pass as input (flat file to start with, then anything else...)
2) Spit out random float between 0.00-100.00
3) Calculate change based on single int input, return breakdown of notes
*/

public class auth {

    public String user = "user";
    public String pword = "pass";

    //Invoke main with user/pass
    //main(user, pword);

    public static void authenticate(String user, String pass) {

    	//boolean answer = True;
    	System.out.println("Authenticatin with " + user);
    	System.out.println("And password " + pass);
    		//return answer;
    
    }

    public static void main(String[] args) {
        System.out.println("Starting...");
        String user = "USER";
        String pass = "PW";
        authenticate(user, pass);

        //boolean finalAnswer = authenticate(user, pass);
        //System.out.println(finalAnswer);
        System.out.println("DONE!");

    }
}

