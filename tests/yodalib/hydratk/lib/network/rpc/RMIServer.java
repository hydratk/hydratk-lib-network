import java.rmi.*;
import java.rmi.server.*;
import java.rmi.registry.*;

class RMIServer extends UnicastRemoteObject implements IServer
{
    public RMIServer() throws RemoteException 
    {
		super();
	}
    
    public void callRemote() throws RemoteException
    {
        System.out.println("Method has been called!!!!");
    }
    
    public int out_int() throws RemoteException
    {
        return 666;
    }
    
    public String out_string() throws RemoteException
    {
        return "Sucker";
    }
    
    public int in_int(int i) throws RemoteException
    {
        System.out.println(i);
        return i+6;
    }
    
    public String in_string(String s) throws RemoteException
    {
        System.out.println(s);
        return s + " xxx";
    }
    
    public String in2(int i1, int i2) throws RemoteException
    {
        return String.valueOf(i1) + String.valueOf(i2);
    }
    
    public static void main(String args[]) 
    {
        
		// Create and install a security manager
//		if (System.getSecurityManager() == null) {
//		    System.setSecurityManager(new RMISecurityManager());
//		}
		
		try {
	        Registry reg = LocateRegistry.createRegistry(2004);
		    
		    
		    RMIServer obj = new RMIServer();
		
		    // Bind this object instance to the name "HelloServer"
		    Naming.rebind("//localhost:2004/server", obj);
		
		    System.out.println("HelloServer bound in registry");
		} catch (Exception e) {
		    System.out.println("HelloImpl err: " + e.getMessage());
		    e.printStackTrace();
		}
	}    
}
