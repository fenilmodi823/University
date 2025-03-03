import java.io.*;
import java.net.*;

public class FileTransferServer {
    @SuppressWarnings("CallToPrintStackTrace")
    public static void main(String[] args) {
        int port = 5000;
        ServerSocket serverSocket = null;
        Socket socket = null;

        try {
            serverSocket = new ServerSocket(port);
            System.out.println("Server is listening on port " + port);

            socket = serverSocket.accept();
            System.out.println("Client connected: " + socket.getInetAddress());

            File file = new File("D:\\Example.txt");
            if (!file.exists()) {
                System.out.println("File not found. Exiting...");
                return;
            }

            try (
                    FileInputStream fis = new FileInputStream(file);
                    BufferedInputStream bis = new BufferedInputStream(fis)) {
                OutputStream os = socket.getOutputStream();

                byte[] buffer = new byte[4096];
                int bytesRead;
                System.out.println("Sending file: " + file.getName());

                while ((bytesRead = bis.read(buffer)) != -1) {
                    os.write(buffer, 0, bytesRead);
                }

                os.flush();
                System.out.println("File transfer complete.");

            }
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            try {
                if (socket != null)
                    socket.close();
                if (serverSocket != null)
                    serverSocket.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
}