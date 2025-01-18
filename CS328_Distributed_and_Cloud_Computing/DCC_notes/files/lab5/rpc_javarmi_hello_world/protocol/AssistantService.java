package protocol;

import java.rmi.Remote;
import java.rmi.RemoteException;

public interface AssistantService extends Remote {
  String greetWithInfo(String userName, String institution) throws RemoteException;

  double multiply(double xin, double yin) throws RemoteException;
}

/**
 * To completely mimic the behavior of the proto file, where remote procedures
 * may have multiple inputs and outputs, define the message classes manually in
 * separate files from this package. Requests may be skipped since Java handles
 * multiple inputs naturally.
 */
