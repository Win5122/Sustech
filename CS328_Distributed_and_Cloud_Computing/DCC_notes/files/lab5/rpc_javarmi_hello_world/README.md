# Java RMI
[Java RMI (Remote Method Invocation)](https://docs.oracle.com/javase/8/docs/technotes/guides/rmi/) is a Java-specific RPC implementation that utilizes dynamic proxies (since Java 5) via Java Reflection.

An official hello-world example can be found here: https://docs.oracle.com/javase/8/docs/technotes/guides/rmi/hello/hello-world.html. 

## Requirements
- Java Development Kit (JDK) - `sudo apt install default-jdk` for Ubuntu/WSL2. It will include a `rmiregistry` program 

## Define the Remote Interface
The remote interface in Java RMI works similarly to the `.proto` file in gRPC, in that both define the contract (protocol) between the client and the server.

Check the `protocol/AssistantService.java` file. Define the required service procedures here. To completely mimic the behavior of the proto file, where remote procedures may have multiple inputs and outputs, define the message classes manually in separate files from this package. Requests may be skipped since Java handles multiple inputs naturally.

```java
public interface AssistantService extends Remote {
  String greetWithInfo(String userName, String institution) throws RemoteException;
  double multiply(double xin, double yin) throws RemoteException;
}
```

## Implement the Server
Check the `server/AssistantServer.java` file. The actual remote procedures are implemented. Besides, a main function sets up the RMI server by:

1. creating a service remote object;
2. generating a client stub (and a server skeleton as well behind the scene) via `exportObject`;
3. registering the generated client stub to a local/remote RMI registry.

The server will not exit immediately because: 
> "The static method UnicastRemoteObject.exportObject exports the supplied remote object to receive incoming remote method invocations on an anonymous TCP port and returns the stub for the remote object to pass to clients. As a result of the exportObject call, the runtime may begin to listen on a new server socket or may use a shared server socket to accept incoming remote calls for the remote object. The returned stub implements the same set of remote interfaces as the remote object's class and contains the host name and port over which the remote object can be contacted."

We will now dig a bit deeper into the source code of `UnicastRemoteObject.exportObject`. This function finally points to the `exportObject` function from a `UnicastServerRef` object:

```java
public Remote exportObject(Remote impl, Object data, boolean permanent) throws RemoteException {
  Class<?> implClass = impl.getClass();

  Remote stub;
  try {
     stub = Util.createProxy(implClass, this.getClientRef(), this.forceStubUse);
  } catch (IllegalArgumentException var7) {
     throw new ExportException("remote object implements illegal remote interface", var7);
  }

  if (stub instanceof RemoteStub) {
     this.setSkeleton(impl);
  }

  Target target = new Target(impl, this, stub, this.ref.getObjID(), permanent);
  this.ref.exportObject(target);
  this.hashToMethod_Map = (Map)hashToMethod_Maps.get(implClass);
  return stub;
}
```

It can be noticed that in this code snippet, a client stub is further created via `Util.createProxy` and returned in the end. Besides, a server skeleton (or a server stub) is also generated and maintained via `setSkeleton`, which is the following:

```java
public void setSkeleton(Remote impl) throws RemoteException {
  if (!withoutSkeletons.containsKey(impl.getClass())) {
     try {
        this.skel = Util.createSkeleton(impl);
     } catch (SkeletonNotFoundException var3) {
        withoutSkeletons.put(impl.getClass(), (Object)null);
     }
  }

}
```

As a conclusion, the client stub and the server stub/skeleton are generate by Java RMI's internal implementation, so we say dynamic proxy is supported.

## Implement the Client
Check the `client/Client.java` file. In this file, the corresponding client stub is fetched from the RMI registry via the `lookup` function. Then, we just use the client stub to perform some remote procedure calls.

## Compile the Source Files
Run the following to compile the source files and generate the binaries to the `bin/` folder:
```bash
javac -d bin/ protocol/AssistantService.java server/AssistantServer.java client/Client.java
```

- `-d` specifies the destination folder of the generated classes.

## Run the RMI Registry, Server, and Client
With a basic knowledge of RPC and Java RMI, it is straightforward to understand that the execution order is:

1. Run the RMI Registry.
2. Run the Server.
3. Run the Client.

To start the registry at port=`1099` (the default one in Java RMI):
```bash
cd bin/   # IMPORTANT: start the RMI registry from the class path directory!!!
rmiregistry 1099
```
To run it as a background task: `rmiregistry 1099 &`, but we will need to find and kill the process afterwards. **Note that the RMI registry MUST be started from the generated class path folder, otherwise the server and the client will fail to locate the defined interface so that they can marshal and unmarshal remote objects as required in Java RMI.**

The java files can be executed by `java -cp bin/ <PACKAGE+CLASS_NAME>`, where `-cp` specifies the class path `bin/`.

To start the server in another terminal, run:
```bash
java -cp bin/ server.AssistantServer
```

The server will keep running until a manual interruption.

Finally, to execute the client in another terminal, run:
```bash
java -cp bin/ client.Client
```

The expected output will be:
```text
> Greet: Hello Assistant? I am "Peter" from "SUSTech".
> Client received: Hello Peter from SUSTech!
> Mult: Requesting a multiplication task - 3.5 x 5
> Client received: 17.5
```
