public class Example {
	
	public static void main(String[] args) {
		System.out.println("Starting...");
		PezDispenser dispenser = new PezDispenser("Test");
		System.out.printf("The char name is %s\n", dispenser.getCharacterName());
		//System.out.printf("The char name is %s\n", dispenser.mCharacterName);
	}
}