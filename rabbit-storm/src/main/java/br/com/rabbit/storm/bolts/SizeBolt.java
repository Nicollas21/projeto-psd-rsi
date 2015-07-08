package br.com.rabbit.storm.bolts;

import com.rabbitmq.client.ConnectionFactory;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.Channel;

import java.awt.List;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Map;
import java.util.logging.Logger;

import com.googlecode.charts4j.AxisLabels;
import com.googlecode.charts4j.AxisLabelsFactory;
import com.googlecode.charts4j.AxisStyle;
import com.googlecode.charts4j.AxisTextAlignment;
import com.googlecode.charts4j.BarChart;
import com.googlecode.charts4j.BarChartPlot;
import com.googlecode.charts4j.Data;
import com.googlecode.charts4j.Fills;
import com.googlecode.charts4j.GCharts;
import com.googlecode.charts4j.LinearGradientFill;
import com.googlecode.charts4j.Plots;

import backtype.storm.task.OutputCollector;
import backtype.storm.task.TopologyContext;
import backtype.storm.topology.IRichBolt;
import backtype.storm.topology.OutputFieldsDeclarer;
import backtype.storm.tuple.Fields;
import backtype.storm.tuple.Tuple;
import backtype.storm.tuple.Values;
import backtype.storm.utils.Utils;

public class SizeBolt implements IRichBolt{
	
	private static final long serialVersionUID = 1L;
	OutputCollector collector;
	
	private float media = 15;
	private float sizeTotal = 0;
	private int cont=0;

	public void prepare(Map stormConf, TopologyContext context,
			OutputCollector collector) {
		this.collector = collector;
		
	}

	public void execute(final Tuple input) {
		try {
			metricas(input);
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
	}
	
	public void metricas(Tuple input) throws IOException{
		ArrayList<String> tuplas = new ArrayList<String> ();
		String messages = input.getString(0);
		messages = messages.replace("(","");
		messages = messages.replace(")","");
		messages = messages.replace(" ","");
		
		for (String tupla: messages.split(",")){
	        tuplas.add(tupla);
	        //System.out.println(tupla);
		}
		
		String msg_size = tuplas.get(2);
		String protocolo = tuplas.get(0);
		protocolo = protocolo.replace("'","");
		
		float size = Float.parseFloat(msg_size);

		if (size>=media){
			//System.out.println(protocolo+" Elefante "+size+" "+media+" "+cont+" "+sizeTotal);
			String tupla = protocolo+","+"Elefante";
			//System.out.println(tupla);
			sendQueue(tupla);
		}else{
			//System.out.println(protocolo+" Rato "+size+" "+media+" "+cont+" "+sizeTotal);
			String tupla = protocolo+","+"Rato";
			//System.out.println(tupla);
			sendQueue(tupla);
		}
		this.cont+=1;
		this.sizeTotal += size;
		this.media = (sizeTotal/cont);
		
		//this.collector.emit(new Values(messages));
		//collector.ack(input);
		
	}
	public void sendQueue(String message) throws IOException{
		final String QUEUE_NAME = "dados";
		
		ConnectionFactory factory = new ConnectionFactory();
	    factory.setHost("localhost");
	    Connection connection = factory.newConnection();
	    Channel channel = connection.createChannel();
	    
	    channel.queueDeclare(QUEUE_NAME, false, false, false, null);
	    
	    channel.basicPublish("", QUEUE_NAME, null, message.getBytes());
	    System.out.println(" [x] Sent '" + message + "'");
	    
	    channel.close();
	    connection.close();
		
    }
	public void cleanup() {
		// TODO Auto-generated method stub
		
	}

	public void declareOutputFields(OutputFieldsDeclarer declarer) {
		declarer.declare(new Fields("message"));
		
	}

	public Map<String, Object> getComponentConfiguration() {
		// TODO Auto-generated method stub
		return null;
	}

	

}
