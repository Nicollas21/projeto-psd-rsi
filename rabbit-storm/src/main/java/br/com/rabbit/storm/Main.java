
package br.com.rabbit.storm;

import java.io.IOException;
import java.sql.SQLException;
import java.util.HashMap;
import java.util.List;

import backtype.storm.Config;
import backtype.storm.LocalCluster;
import backtype.storm.StormSubmitter;
import backtype.storm.topology.TopologyBuilder;
import backtype.storm.utils.Utils;
import br.com.rabbit.storm.bolts.DurationBolt;
import br.com.rabbit.storm.bolts.RateBolt;
import br.com.rabbit.storm.bolts.SizeBolt;
import br.com.rabbit.storm.spouts.AMQPRecvSpoutBitTorrent;
import br.com.rabbit.storm.spouts.AMQPRecvSpoutDHCP;
import br.com.rabbit.storm.spouts.AMQPRecvSpoutHTTP;
import br.com.rabbit.storm.spouts.AMQPRecvSpoutSSDP;
import br.com.rabbit.storm.spouts.AMQPRecvSpoutSSH;
import br.com.rabbit.storm.spouts.AMQPRecvSpoutSSL;
import br.com.rabbit.storm.spouts.AMQPRecvSpoutUnknown;

public class Main {
	public static void main(String[] args) throws Exception{
		/**ReceiveLogsTopic receive = new ReceiveLogsTopic();
		receive.conection();
		receive.getMsg();**/
		
		
		TopologyBuilder builder = new TopologyBuilder();
    	builder.setSpout("spoutBitTorrent", new AMQPRecvSpoutBitTorrent("localhost", 5672, "server", "server123", "grupo1", true, false), 1);
    	builder.setSpout("spoutDHCP", new AMQPRecvSpoutDHCP("localhost", 5672, "server", "server123", "grupo1", true, false), 1);
    	builder.setSpout("spoutHTTP", new AMQPRecvSpoutHTTP("localhost", 5672, "server", "server123", "grupo1", true, false), 1);
    	builder.setSpout("spoutSSDP", new AMQPRecvSpoutSSDP("localhost", 5672, "server", "server123", "grupo1", true, false), 1);
    	builder.setSpout("spoutSSH", new AMQPRecvSpoutSSH("localhost", 5672, "server", "server123", "grupo1", true, false), 1);
    	builder.setSpout("spoutSSL", new AMQPRecvSpoutSSL("localhost", 5672, "server", "server123", "grupo1", true, false), 1);
    	builder.setSpout("spoutUnknown", new AMQPRecvSpoutUnknown("localhost", 5672, "server", "server123", "grupo1", true, false), 1);

        
    	builder.setBolt("sizeBit", new SizeBolt()).shuffleGrouping("spoutBitTorrent");
        builder.setBolt("durBit", new DurationBolt()).shuffleGrouping("spoutBitTorrent");
        builder.setBolt("rateBit", new RateBolt()).shuffleGrouping("spoutBitTorrent");
        
    	builder.setBolt("sizeDhcp", new SizeBolt()).shuffleGrouping("spoutDHCP");
        builder.setBolt("durDhcp", new DurationBolt()).shuffleGrouping("spoutDHCP");
        builder.setBolt("rateDhcp", new RateBolt()).shuffleGrouping("spoutDHCP");
        
        builder.setBolt("sizeHttp", new SizeBolt()).shuffleGrouping("spoutHTTP");
        builder.setBolt("durHttp", new DurationBolt()).shuffleGrouping("spoutHTTP");
        builder.setBolt("rateHttp", new RateBolt()).shuffleGrouping("spoutHTTP");
        
        builder.setBolt("sizeSsdp", new SizeBolt()).shuffleGrouping("spoutSSDP");
        builder.setBolt("durSsdp", new DurationBolt()).shuffleGrouping("spoutSSDP");
        builder.setBolt("rateSsdp", new RateBolt()).shuffleGrouping("spoutSSDP");
        
        builder.setBolt("sizeSsh", new SizeBolt()).shuffleGrouping("spoutSSH");
        builder.setBolt("durSsh", new DurationBolt()).shuffleGrouping("spoutSSH");
        builder.setBolt("rateSsh", new RateBolt()).shuffleGrouping("spoutSSH");
        
        builder.setBolt("sizeSsl", new SizeBolt()).shuffleGrouping("spoutSSL");
        builder.setBolt("durSsl", new DurationBolt()).shuffleGrouping("spoutSSL");
        builder.setBolt("rateSsl", new RateBolt()).shuffleGrouping("spoutSSL");
        
        builder.setBolt("sizeUnk", new SizeBolt()).shuffleGrouping("spoutUnknown");
        builder.setBolt("durUnk", new DurationBolt()).shuffleGrouping("spoutUnknown");
        builder.setBolt("rateUnk", new RateBolt()).shuffleGrouping("spoutUnknown");
        
        
        Config conf = new Config();
        LocalCluster cluster = new LocalCluster();
        cluster.submitTopology("test", conf, builder.createTopology());
        //Utils.sleep(100);
        //cluster.killTopology("test");
        //cluster.shutdown();
    	
	}
	
	
}