import java.rmi.*;

interface IServer extends Remote
{
    void callRemote() throws RemoteException;
    
    int out_int() throws RemoteException;
    
    String out_string() throws RemoteException;
    
    int in_int(int i) throws RemoteException;
    
    String in_string(String s) throws RemoteException;
    
    String in2(int i1, int i2) throws RemoteException;
}
