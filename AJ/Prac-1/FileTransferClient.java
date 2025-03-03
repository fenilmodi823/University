import java.io.*;
import java.net.*;

public class FileTransferClient {
    @SuppressWarnings("CallToPrintStackTrace")
    public static void main(String[] args) {
        String serverAddress = "localhost";
        int port = 5000;

        Socket socket = null;
        FileOutputStream fos = null;
        BufferedOutputStream bos = null;

        try {
            socket = new Socket(serverAddress, port);
            System.out.println("Connected to server.");

            InputStream is = socket.getInputStream();
            fos = new FileOutputStream("E:\\received_Example.txt");
            bos = new BufferedOutputStream(fos);

            byte[] buffer = new byte[4096];
            int bytesRead;
            System.out.println("Receiving file...");

            while ((bytesRead = is.read(buffer)) != -1) {
                bos.write(buffer, 0, bytesRead);
            }

            bos.flush();
            System.out.println("File received successfully.");
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            try {
                if (bos != null)
                    bos.close();
                if (fos != null)
                    fos.close();
                if (socket != null)
                    socket.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
}