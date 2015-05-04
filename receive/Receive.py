#!/usr/bin/env python

from Pacote import *
import pika
import sys

class Receive:
    credentials = pika.PlainCredentials('server', 'server123')
    connection = pika.BlockingConnection(pika.ConnectionParameters(
                   '172.16.205.153', 5672, 'grupo1', credentials))
    channel = connection.channel()
    
    channel.exchange_declare(exchange='topic_logs',
                             type='topic')
    
    result = channel.queue_declare(exclusive=True)
    queue_name = result.method.queue
    
    
    binding_keys = ["bittorrent","dchp", "http", "ssdp", "ssh", "ssl", "unknown"]
    
    for binding_key in binding_keys:
        channel.queue_bind(exchange='topic_logs',
                           queue=queue_name,
                           routing_key=binding_key)
    
    print " [*] Waiting for logs. To exit press CTRL+C" 
    
    def callback(ch, method, properties, body):
        print " [x] %r:%r" % (method.routing_key, body)
        
        #separatedPackage(method, body)
        tupla = body.split(',')
        size = tupla[0]
        size = size[1:]
        time = tupla[1]
        pacote = Pacote(method.routing_key, size, time)
       
        channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)
             
        channel.start_consuming()
    
'''    def separatedPackage(method, body):
        tupla = body.split(',')
        size = tupla[0]
        size = size[1:]
        time = tupla[1]
        
        pacote = Pacote(method.routing_key, size, time)'''
        
        
