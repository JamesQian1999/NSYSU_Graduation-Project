import java.io.DataOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;


public class TCP_server_test {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		
		try {
			ServerSocket ss = new ServerSocket(10000);
			System.out.println("Server: wait for call..");
			Socket socket = ss.accept();
			System.out.println("Server: start!");
			DataOutputStream os = new DataOutputStream( socket.getOutputStream());
			File f = new File("Cat.jpg");
            System.out.println("Server File name: "+ f.length());
            int size = (int)f.length();
            os.writeInt(size);
			FileInputStream fis= new FileInputStream(f);
			byte[] b = new byte[2048];
            int len=0;
			while((len=fis.read(b, 0, b.length))>0)
			{
                System.out.println("Server: "+len);
				os.write(b);
                os.flush();
			}
            socket.close();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
    }
}