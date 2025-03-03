import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;

public class SumClient {
    @SuppressWarnings({ "UseSpecificCatch", "CallToPrintStackTrace" })
    public static void main(String[] args) {
        try {
            Registry registry = LocateRegistry.getRegistry("localhost", 1099);

            SumInterface stub = (SumInterface) registry.lookup("SumService");

            int result = stub.sum(5, 10);
            System.out.println("Sum: " + result);
        } catch (Exception e) {
            System.err.println("Client exception: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
