import java.net.*;
import java.io.*;
import java.net.ServerSocket;
import java.net.Socket;
import java.lang.Math;

public class TCP_client{
    public static void main(String[] args) throws IOException {
        try{
            Socket s = new Socket("192.168.0.111", 53272);
            System.out.println("Client: start!");
            new ReceiveThread(s).start();
        }catch(Exception e){
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
	    	
	    	while(isConnected) {
		        try {
		        	is = s.getInputStream();
		            dis= new DataInputStream(is);
		            byte[] buf = new byte[2048];
		            //int size = is.read(buf);
                    int size = dis.read(buf);
                    int temp=0;
                    size = 6;
                    for(int i = 0; i < size; i++) {
                        temp+= (buf[i]-48)*Math.pow(10, size-i-1);
                    }
                    System.out.println("Client Size: "+temp);
		            int len = 0;
                    int cnt=1;
		            while((len =dis.read(buf, 0, buf.length))>0){
                        if(fout == null) { 
                            fout = new FileOutputStream(new File("photo.jpg")); 
                        }
                        System.out.println(cnt+++": Client: "+len);

		                fout.write(buf, 0, len);
                        fout.flush();
                        // temp-=2048;
                        // if(temp<2048){
                        //     len =dis.read(buf, 0, buf.length);
                        //     System.out.println(cnt+++": Client: "+temp);
                        //     fout.write(buf, 0, temp);
                        //     fout.flush();
                        //     break;
                        // }
		            }
		            
		            isConnected = false; 
		            
		            if(fout != null) { 
                        fout.close();
                    } 
		            dis.close();
		            s.close();
                    System.out.println("Finish");
		        }catch(IOException eIO) { eIO.printStackTrace(); }
	    		
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