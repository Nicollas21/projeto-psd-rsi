package br.com.rabbit.storm;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import com.rabbitmq.client.Connection;
import com.rabbitmq.client.Channel;
import com.rabbitmq.client.ConnectionFactory;
import com.rabbitmq.client.ConsumerCancelledException;
import com.rabbitmq.client.QueueingConsumer;
import com.rabbitmq.client.ShutdownSignalException;


public class ReceiveLogsTopic {
	private static final long WAIT_FOR_NEXT_MESSAGE = 1L;
    private static final String EXCHANGE_NAME = "topic_logs";
    private List<String> messages = new ArrayList<String>();
    
    public static void conection() throws IOException, ShutdownSignalException, ConsumerCancelledException, InterruptedException {

        ConnectionFactory factory = new ConnectionFactory();
        factory.setUsername("server");
        factory.setPassword("server123");
        factory.setPort(5672);
        factory.setVirtualHost("grupo1");
        factory.setHost("localhost");
        Connection connection = (Connection) factory.newConnection();
        Channel channel = ((com.rabbitmq.client.Connection) connection).createChannel();

        channel.exchangeDeclare(EXCHANGE_NAME, "topic");
        String queueName = channel.queueDeclare().getQueue();
        
        String[] bindingKeys = new String[] {"bittorrent","dchp", "http", "ssdp", "ssh", "ssl", "unknown"};
        //String[] bindingKeys = new String[] {"bittorrent"};
        
        for(String bindingKey : bindingKeys){
            channel.queueBind(queueName, EXCHANGE_NAME, bindingKey);
        }

        System.out.println(" [*] Waiting for messages. To exit press CTRL+C");

        QueueingConsumer consumer = new QueueingConsumer(channel);
        channel.basicConsume(queueName, true, consumer);

        while (true) {
            QueueingConsumer.Delivery delivery = consumer.nextDelivery();
            String message = new String(delivery.getBody());
            String routingKey = delivery.getEnvelope().getRoutingKey();
            System.out.println(message);
        }
        
    }
    public static void main(String[] args) throws Exception{
    	conection();
    }
}
    
