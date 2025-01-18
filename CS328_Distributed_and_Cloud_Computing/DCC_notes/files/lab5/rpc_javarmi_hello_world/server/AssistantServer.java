package server;

import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.rmi.server.UnicastRemoteObject;

import protocol.AssistantService;

public class AssistantServer implements AssistantService {
  public AssistantServer() {
  }

  /* Implement remote procedures as a service. */

  public String greetWithInfo(String userName, String institution) {
    return String.format("Hello %s from %s!", userName, institution);
  }

  public double multiply(double xin, double yin) {
    return xin * yin;
  }

  /*
   * Main program to start a server and register the service to the RMI registry.
   */
  public static void main(String[] args) {
    try {
      AssistantServer s = new AssistantServer();
      // Create a stub for the assistant service.
      // The corresponding remote object will accept incoming RMI calls on port=0,
      // meaning the RMI system will automatically select an available TCP port.
      AssistantService stub = (AssistantService) UnicastRemoteObject.exportObject(s, 0);
      // Bind the remote object's stub in the registry
      Registry registry = LocateRegistry.getRegistry("localhost", 1099);
      registry.rebind("Assistant", stub);
      System.out.println("Server ready.");
    } catch (Exception e) {
      System.err.println("Server exception: " + e.toString());
      e.printStackTrace();
    }
  }
}

/**
 * The server will not exit immediately because:
 * 
 * "The static method UnicastRemoteObject.exportObject exports the supplied
 * remote object to receive incoming remote method invocations on an anonymous
 * TCP port and returns the stub for the remote object to pass to clients. As a
 * result of the exportObject call, the runtime may begin to listen on a new
 * server socket or may use a shared server socket to accept incoming remote
 * calls for the remote object. The returned stub implements the same set of
 * remote interfaces as the remote object's class and contains the host name and
 * port over which the remote object can be contacted."
 */
