package br.com.rabbit.storm;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import com.rabbitmq.client.Connection;
import com.rabbitmq.client.Channel;
import com.rabbitmq.client.ConnectionFactory;
import com.rabbitmq.client.ConsumerCancelledException;
import com.rabbitmq.client.QueueingConsumer;
import com.rabbitmq.client.ShutdownSignalException;


public class Main2 {
	private static Map<String,Integer> protocolos = new HashMap<String, Integer>();
	
	public static void putHash(){
		protocolos.put("bittorrent", 0);
		protocolos.put("dchp", 0);
		protocolos.put("http", 0);
		protocolos.put("ssdp", 0);
		protocolos.put("ssh", 0);
		protocolos.put("ssl", 0);
		protocolos.put("unknown", 0);
	      
	}
    
    public static void conection()  {
    	putHash();
    	System.out.print(protocolos);
    	Integer x =protocolos.get("dchp");
    	x +=1;
    	protocolos.put("dchp",x);        
    	
    }
    public static void main(String[] args) throws Exception{
    	conection();
    }
}
    
