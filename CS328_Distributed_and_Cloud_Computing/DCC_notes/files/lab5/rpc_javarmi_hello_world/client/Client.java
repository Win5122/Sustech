package client;

import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;

import protocol.AssistantService;

public class Client {
  private Client() {
  }

  public static void main(String[] args) {
    try {
      // Find the client stub we want from the RMI registry
      Registry registry = LocateRegistry.getRegistry("localhost", 1099);
      AssistantService stub = (AssistantService) registry.lookup("Assistant");
      /* RMI now! */
      // Greeting
      System.out.println("> Greet: Hello Assistant? I am \"Peter\" from \"SUSTech\".");
      String greetMsg = stub.greetWithInfo("Peter", "SUSTech");
      System.out.println("> Client received: " + greetMsg);
      // Multiplication
      System.out.println("> Mult: Requesting a multiplication task - 3.5 x 5");
      double multRes = stub.multiply(3.5, 5);
      System.out.println("> Client received: " + multRes);
    } catch (Exception e) {
      System.err.println("Client exception: " + e.toString());
      e.printStackTrace();
    }
  }
}
