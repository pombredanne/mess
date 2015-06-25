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

    public static void main(String[] args) {
        for (String s: args) {
            System.out.println(s);
        }
    }
}