import java.io.Console;



public class TreeStory {

	public static void main(String[] args) {

		Console console = System.console();

		//String ageStr = console.readLine("Your age? ");
		
		/*int age = Integer.parseInt(ageStr);
		if (age < 13) {
			console.printf("Sorry, no go...");
			System.exit(0);
		}*/

		String name = console.readLine("Enter your name: ");

		String noun;
		boolean valid;


		do {

			noun = console.readLine("Enter a noun: ");
			valid = (noun.equalsIgnoreCase("dork") || noun.equalsIgnoreCase("jerk"));
			if (valid) {
				console.printf("HEY! Try again...\n");
			}
		} while(valid);

		//console.printf("%s is very %s\n", name, noun);
		System.out.println(name + " is a large " + noun);

	}
}