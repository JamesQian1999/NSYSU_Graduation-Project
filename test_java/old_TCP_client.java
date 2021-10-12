import java.net.*;
import java.io.*;
import java.net.ServerSocket;
import java.net.Socket;

public class old_TCP_client {
    public static void main(String[] args) throws IOException {
        try {
            Socket s = new Socket("192.168.0.179", 10000);
            System.out.println("Client: start!");
            new ReceiveThread(s).start();
        } catch (Exception e) {
            System.out.println("Bad!");
            e.printStackTrace();
        }

    }

    private static class ReceiveThread extends Thread {

        private Socket s;
        private InputStream is;
        private OutputStream fout;
        private DataInputStream dis;
        private boolean isConnected;

        public ReceiveThread(Socket s) {
            this.s = s;
            isConnected = true;
        }

        @Override
        public void run() {

            while (isConnected) {
                try {
                    is = s.getInputStream();
                    dis = new DataInputStream(is);
                    byte[] buf = new byte[1024];
                    // int size = is.read(buf);
                    int size = dis.readInt();
                    System.out.println("Client Size: " + size);
                    int len = 0, count_bit = 0, r = size / 1024 + 1, i = 0;
                    while (true) {
                        for(long j=0;j<60000l;j++);
                        i++;
                        if (i == r) {
                            len = dis.read(buf, 0, size-count_bit);
                            System.out.println("Client: " + len);
                            fout.write(buf, 0, len);
                            fout.flush();
                            break;
                        }
                        len = dis.read(buf, 0, 1024);
                        if (fout == null) {
                            fout = new FileOutputStream(new File("photo.jpg"));
                        }
                        System.out.println("Client: " + len);
                        fout.write(buf, 0, len);
                        fout.flush();
                        count_bit += len;
                        System.out.println(count_bit);


                        // size-=2048;
                        // if(size<2048){
                        // len =dis.read(buf, 0, buf.length);
                        // System.out.println("Client: "+size);
                        // fout.write(buf, 0, size);
                        // fout.flush();
                        // }
                    }

                    isConnected = false;

                    if (fout != null) {
                        fout.close();
                    }
                    dis.close();
                    s.close();
                } catch (IOException eIO) {
                    eIO.printStackTrace();
                }

            }

        }

    }
}

// PrintWriter pr = new PrintWriter(s.getOutputStream());

// InputStreamReader in = new InputStreamReader(s.getInputStream());
// BufferedReader bf = new BufferedReader(in);


// out.write(msg.getBytes("UTF-8"));
// out.flush();

// int rcvLen = dis.read(buffer);
// String rcvMsg = new String(buffer, 0, rcvLen, "utf-8");
// System.out.println("Server:" + rcvMsg);

// msg="exit";
// out.write(msg.getBytes("UTF-8"));
// out.flush();



// pr.println("Hi Server");
// pr.flush();
// String str1 = bf.readLine();
// System.out.println("Server:" + str1);

// pr.println("87 Server");
// pr.flush();
// String str2 = bf.readLine();
// System.out.println("Server:" + str2);

// pr.println("exit");
// pr.flush();
