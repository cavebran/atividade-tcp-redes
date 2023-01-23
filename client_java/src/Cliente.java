/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Main.java to edit this template
 */

/**
 *
 * @author felipe
 */
import java.io.*;
import java.net.*;
import java.util.Scanner;

public class Cliente {
    private static DataOutputStream dataOutputStream = null;
    private static DataInputStream dataInputStream = null;
    private static Scanner scanner = new Scanner(System.in);

    public static void main(String[] args) {
        try(Socket socket = new Socket("localhost",9000)){
            dataInputStream = new DataInputStream(socket.getInputStream());
            dataOutputStream = new DataOutputStream(socket.getOutputStream());

         
            while (true) {
                System.out.print("input> ");
                String message = scanner.nextLine();
                dataOutputStream.writeUTF(message);
                if(message.equalsIgnoreCase("close"))
                    break;
                if("upload".equals(message)){
                    System.out.println("Coloque o caminho do arquivo:  -- ");
                    String fpath = scanner.nextLine();
                    sendFile(fpath);
                }
                if("download".equals(message)){
                    System.out.println("Coloque o nome do arquivo:  -- ");
                    String fname = scanner.nextLine();
                    receiveFile(fname);
                }
            }
            dataInputStream.close();
            dataInputStream.close();

        }catch (Exception e){
            System.out.println(e.toString());
        }
    

    }
    private static void sendFile(String path) throws Exception{
        dataOutputStream.writeChars("upload");
        int bytes = 0;
        File file = new File(path);
        FileInputStream fileInputStream = new FileInputStream(file);
        
        // send file size
        dataOutputStream.writeLong(file.length());  
        // break file into chunks
        byte[] buffer = new byte[4*1024];
        while ((bytes=fileInputStream.read(buffer))!=-1){
            dataOutputStream.write(buffer,0,bytes);
            dataOutputStream.flush();
        }
        fileInputStream.close();
    }
    private static void receiveFile(String fileName) throws Exception{
        dataOutputStream.writeChars("download");
        int bytes = 0;
        FileOutputStream fileOutputStream = new FileOutputStream(fileName);
        
        long size = dataInputStream.readLong();     // read file size
        byte[] buffer = new byte[4*1024];
        while (size > 0 && (bytes = dataInputStream.read(buffer, 0, (int)Math.min(buffer.length, size))) != -1) {
            fileOutputStream.write(buffer,0,bytes);
            size -= bytes;      // read upto file size
        }
        fileOutputStream.close();
    }
    
    
}


