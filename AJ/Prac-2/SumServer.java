import java.rmi.RemoteException;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.rmi.server.UnicastRemoteObject;

public class SumServer extends UnicastRemoteObject implements SumInterface {

    protected SumServer() throws RemoteException {
        super();
    }

    @SuppressWarnings("override")
    public int sum(int a, int b) throws RemoteException {
        return a + b;
    }

    @SuppressWarnings({ "UseSpecificCatch", "CallToPrintStackTrace" })
    public static void main(String[] args) {
        try {
            SumServer server = new SumServer();

            Registry registry = LocateRegistry.createRegistry(1099);

            registry.rebind("SumService", server);

            System.out.println("SumServer is running...");
        } catch (Exception e) {
            System.err.println("Server exception: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
