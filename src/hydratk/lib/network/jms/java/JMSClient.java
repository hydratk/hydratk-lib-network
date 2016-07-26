import java.util.Properties;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.concurrent.ConcurrentHashMap;
import java.util.Map.Entry;
import java.util.Enumeration;

import javax.naming.Context;
import javax.naming.InitialContext;
import javax.jms.ConnectionFactory;
import javax.jms.Queue;
import javax.jms.Topic;
import javax.jms.Connection;
import javax.jms.Session;
import javax.jms.MessageProducer;
import javax.jms.MessageConsumer;
import javax.jms.QueueBrowser;
import javax.jms.Message;
import javax.jms.TextMessage;
import javax.jms.BytesMessage;
import javax.jms.DeliveryMode;

/**
* Generic JMS client
* Specific client libraries are located on classpath
* Tested clients - WebLogic, OpenMQ, ActiveMQ
* 
* @author  Petr Rašek
* @version 0.2.0
* @since   2015-12-12 
*/

public class JMSClient {

    private boolean verbose;
    private boolean connected = false;
    private Context ctx = null;
    private Connection connection = null;
    private ConnectionFactory factory = null;
    private Session session = null;
    private MessageProducer producer = null; 
    private MessageConsumer consumer = null;
    
    public final static HashMap<String, String> propertyMap;
    static {
        
        propertyMap = new HashMap<String, String>();
        propertyMap.put("APPLET", Context.APPLET);
        propertyMap.put("AUTHORITATIVE", Context.AUTHORITATIVE);
        propertyMap.put("BATCHSIZE", Context.BATCHSIZE);
        propertyMap.put("DNS_URL", Context.DNS_URL);
        propertyMap.put("INITIAL_CONTEXT_FACTORY", Context.INITIAL_CONTEXT_FACTORY);
        propertyMap.put("LANGUAGE", Context.LANGUAGE);
        propertyMap.put("OBJECT_FACTORIES", Context.OBJECT_FACTORIES);
        propertyMap.put("PROVIDER_URL", Context.PROVIDER_URL);
        propertyMap.put("REFERRAL", Context.REFERRAL);
        propertyMap.put("SECURITY_AUTHENTICATION", Context.SECURITY_AUTHENTICATION);
        propertyMap.put("SECURITY_CREDENTIALS", Context.SECURITY_CREDENTIALS);
        propertyMap.put("SECURITY_PRINCIPAL", Context.SECURITY_PRINCIPAL);
        propertyMap.put("SECURITY_PROTOCOL", Context.SECURITY_PROTOCOL);
        propertyMap.put("STATE_FACTORIES", Context.STATE_FACTORIES);
        propertyMap.put("URL_PKG_PREFIXES", Context.URL_PKG_PREFIXES);
    }
    
    /**
     * constructor
     * @param verbose 
     */
    public JMSClient(boolean verbose)
    {
        
        this.verbose = verbose;
        
    }
    
    /**
    * connect
    * Connect to JMS server
    * @param connectionFactory
    * @param properties
    * @return boolean
    */    
    public boolean connect(String connectionFactory, ConcurrentHashMap<String, String> properties) 
    {        
        
        try {
            
            if (connected) {
                
                System.out.println("INFO - Client is already connected to JMS server");
                return true;
                
            }            
            
            if (verbose) {
                StringBuilder sb = new StringBuilder();
                sb.append("INFO - Connecting to JMS server with connectionFactory:").append(connectionFactory);
                sb.append(", properties:").append(properties);
                System.out.println(sb.toString());
            }
        
            Properties connectionProperties = new Properties();
            String mappedValue;
            for (Entry<String, String> property : properties.entrySet()) {

                mappedValue = propertyMap.get(property.getKey().toUpperCase());
                if (mappedValue != null)
                    connectionProperties.put(mappedValue, property.getValue());
                else
                    System.out.println("WARN - Unknown property: " + property.getKey());

            }
            
            ctx = new InitialContext(connectionProperties);            
            factory = (ConnectionFactory) ctx.lookup(connectionFactory);
            connection = factory.createConnection();
            session = connection.createSession(false, Session.AUTO_ACKNOWLEDGE); 
            
            if (verbose)
                System.out.println("INFO - Connected to JMS server.");            
            
            connected = true;
            return true;
            
        }
        catch(Exception ex) {
            
            System.out.println("ERR - Exception: " + ex.toString());
            if (verbose)
                ex.printStackTrace();
            return false;
            
        }
    }
    
    /**
    * disconnect  
    * Disconnect from JMS server
    * @return boolean
    */      
    public boolean disconnect() {
        
        try {
            
            if (!connected) {
                
                System.out.println("INFO - Client is not connected to JMS server");
                return false;
                
            }            
        
            if (verbose)
                System.out.println("INFO - Disconnecting from JMS server");
            
            if (producer != null)
                producer.close();
            
            if (consumer != null)
                consumer.close();
            
            if (session != null)
                session.close();
            
            if (connection != null)
                connection.close();  
                        
            if (verbose)
                System.out.println("INFO - Disconnected from JMS server");
            
            connected = false;
            return true;
            
        } 
        catch (Exception ex) {
            
            System.out.println("ERR - Exception: " + ex.toString());
            if (verbose)
                ex.printStackTrace();            
            return false;
            
        }
        
    }
    
    /**
    * send
    * Send JMS message
    * @param destinationType
    * @param destinationName
    * @param headers
    * @param message
    * @return boolean
    */      
    public boolean send(String destinationType, String destinationName, ConcurrentHashMap<String, String> headers,
                        String message) {
       
        try {            
            
            if (!connected) {
                
                System.out.println("ERR - Client is not connected to JMS server");
                return false;
                
            }
            
            if (verbose) {
                StringBuilder sb = new StringBuilder();
                sb.append("INFO - Sending message destinationType:").append(destinationType);
                sb.append(", destinationName:").append(destinationName).append(", headers:");
                sb.append(headers).append(", message:").append(message);
                System.out.println(sb.toString());
            }            
            
            if (destinationType.toUpperCase().equals("QUEUE")) {
                Queue queue = (Queue)ctx.lookup(destinationName);
                producer = session.createProducer(queue);
            }
            else if (destinationType.toUpperCase().equals("TOPIC")) {
                Topic topic = (Topic)ctx.lookup(destinationName);
                producer = session.createProducer(topic);                
            }
            else {
                System.out.println("ERR - Unknown destination type:" + destinationType + 
                                   ", expected QUEUE, TOPIC");
                return false;
            }
            
            TextMessage msg = session.createTextMessage();
            for (Entry<String, String> header : headers.entrySet()) {
                
                switch (header.getKey().toUpperCase()) {
                    
                    case "JMSCORRELATIONID":
                        msg.setJMSCorrelationID(header.getValue());
                        break;
                        
                    case "JMSDELIVERYMODE":                        
                        if (header.getValue().toUpperCase().equals("NON_PERSISTENT"))
                            msg.setJMSDeliveryMode(DeliveryMode.NON_PERSISTENT);
                        else if (header.getValue().toUpperCase().equals("PERSISTENT"))
                            msg.setJMSDeliveryMode(DeliveryMode.PERSISTENT);
                        else 
                            System.out.println("WARN - Unknown delivery mode: " + header.getValue() +
                                               ", expected NON_PERSISTENT, PERSISTENT");
                        break;
                        
                    case "JMSDESTINATION":
                        msg.setJMSDestination((Queue)ctx.lookup(header.getValue()));
                        break;
                        
                    case "JMSEXPIRATION":
                        msg.setJMSExpiration(Long.parseLong(header.getValue()));
                        break;
                        
                    case "JMSMESSAGEID":
                        msg.setJMSMessageID(header.getValue());
                        break;
                        
                    case "JMSPRIORITY":
                        msg.setJMSPriority(Integer.parseInt(header.getValue()));
                        break;
                        
                    case "JMSREDELIVERED":
                        if (header.getValue().toUpperCase().equals("TRUE")) 
                            msg.setJMSRedelivered(true);
                        else if (header.getValue().toUpperCase().equals("FALSE"))
                            msg.setJMSRedelivered(false);
                        else
                            System.out.println("WARN - unknown redelivered value: " + header.getValue() + 
                                               ", expected true, false");
                        break;
                        
                    case "JMSREPLYTO":
                        if (destinationName.toUpperCase().equals("QUEUE"))
                            msg.setJMSReplyTo((Queue)ctx.lookup(header.getValue()));
                        else if (destinationName.toUpperCase().equals("TOPIC"))
                            msg.setJMSReplyTo((Topic)ctx.lookup(header.getValue())); 
                        break;
                        
                    case "JMSTIMESTAMP":
                        msg.setJMSTimestamp(Long.parseLong(header.getValue()));
                        break;
                        
                    case "JMSTYPE":
                        msg.setJMSType(header.getValue());
                        break;
                        
                    default:
                        msg.setStringProperty(header.getKey(), header.getValue());
                        break;
                    
                }
                
            }
            
            msg.setText(message);  
            producer.send(msg);
            
            if (verbose)
                System.out.println("INFO - Message sent");
            
            return true;
            
        }
        catch (Exception ex) {
            
            System.out.println("ERR - Exception: " + ex.toString());
            if (verbose)
                ex.printStackTrace();            
            return false;
            
        }
        
    }  
    
    /**
    * receive
    * Receive JMS message
    * @param destinationName
    * @param cnt
    * @return List of JMSMessage
    */      
    public ArrayList<JMSMessage> receive(String destinationName, int cnt) {
       
        try {            
            
            if (!connected) {
                
                System.out.println("ERR - Client is not connected to JMS server");
                return null;
                
            }
            
            if (verbose) {
                StringBuilder sb = new StringBuilder();
                sb.append("INFO - Receiving messages destinationName:").append(destinationName).append(", cnt:").append(cnt);
                System.out.println(sb.toString());
            }            
            
            Queue queue = (Queue)ctx.lookup(destinationName);
            consumer = session.createConsumer(queue);           
            
            connection.start();
            Message message = null;
            int msgCnt = 0;
            boolean matchCorr = false;
            boolean matchType = false;
            ArrayList<JMSMessage> messages = new ArrayList<JMSMessage>();
            
            while (msgCnt < cnt && ((message = consumer.receive(1000)) != null)) {                                           
                
                String body;
                if (message instanceof TextMessage)
                    body = ((TextMessage) message).getText();
                else {
                  
                    BytesMessage msg = (BytesMessage) message;
                    byte[] bytes = new byte[(int)msg.getBodyLength()];
                    msg.readBytes(bytes); 
                    body = new String(bytes, "UTF-8");
                
                }
                    
                messages.add(new JMSMessage(message.getJMSCorrelationID(), message.getJMSDeliveryMode(),
                            (message.getJMSDestination() != null) ? ((Queue) message.getJMSDestination()).getQueueName() : null, 
                    	     message.getJMSExpiration(),
                   		     message.getJMSMessageID(), message.getJMSPriority(), message.getJMSRedelivered(),
                		    (message.getJMSReplyTo() != null) ? ((Queue) message.getJMSReplyTo()).getQueueName() : null,
                    	     message.getJMSTimestamp(), message.getJMSType(), body));
                ++msgCnt;
            
            }
            
            connection.stop();
            
            if (verbose)
                System.out.println("INFO - Messages read");
            
            return messages;
            
        }
        catch (Exception ex) {
            
            System.out.println("ERR - Exception: " + ex.toString());
            if (verbose)
                ex.printStackTrace();            
            return null;
            
        }
        
    }    
    
    /**
    * browse
    * Browse queue
    * @param destinationName
    * @param cnt
    * @param JMSCorrelationID
    * @param JMSType
    * @return List of JMSMessage
    */      
    public ArrayList<JMSMessage> browse(String destinationName, int cnt, String JMSCorrelationID, String JMSType) {
       
        try {            
            
            if (!connected) {
                
                System.out.println("ERR - Client is not connected to JMS server");
                return null;
                
            }
            
            if (verbose) {
                StringBuilder sb = new StringBuilder();
                sb.append("INFO - Browsing queue destinationName:").append(destinationName).append(", cnt:").append(cnt);
                sb.append(", JMSCorrelationID:").append(JMSCorrelationID).append(", JMSType:").append(JMSType);
                System.out.println(sb.toString());
            }            
            
            Queue queue = (Queue)ctx.lookup(destinationName);
            QueueBrowser browser = session.createBrowser(queue);           
            connection.start();
            
            Enumeration msgs = browser.getEnumeration();
            Message message = null;
            int msgCnt = 0;
            boolean matchCorr = false;
            boolean matchType = false;
            ArrayList<JMSMessage> messages = new ArrayList<JMSMessage>();
            
            while (msgCnt < cnt && msgs.hasMoreElements()) {                            
                
            	message = (Message) msgs.nextElement();
            	
                if (JMSCorrelationID == null || JMSCorrelationID.equals(message.getJMSCorrelationID()))
                    matchCorr = true;
                
                if (JMSType == null || JMSType.equals(message.getJMSType()))
                    matchType = true;
                
                if (matchCorr && matchType) {
                
                    String body;
                    if (message instanceof TextMessage)
                    	body = ((TextMessage) message).getText();
                    else {
                  
                        BytesMessage msg = (BytesMessage) message;
                        byte[] bytes = new byte[(int)msg.getBodyLength()];
                        msg.readBytes(bytes); 
                        body = new String(bytes, "UTF-8");
                
                    }
                    
                    messages.add(new JMSMessage(message.getJMSCorrelationID(), message.getJMSDeliveryMode(),
                    		     (message.getJMSDestination() != null) ? ((Queue) message.getJMSDestination()).getQueueName() : null, 
                    		     message.getJMSExpiration(),
                    		     message.getJMSMessageID(), message.getJMSPriority(), message.getJMSRedelivered(),
                    		     (message.getJMSReplyTo() != null) ? ((Queue) message.getJMSReplyTo()).getQueueName() : null,
                    		     message.getJMSTimestamp(), message.getJMSType(), body));
                    ++msgCnt;
                
                }
                
                matchCorr = false;
                matchType = false;
            
            }
            
            connection.stop();
            
            if (verbose)
                System.out.println("INFO - Messages read");
            
            return messages;
            
        }
        catch (Exception ex) {
            
            System.out.println("ERR - Exception: " + ex.toString());
            if (verbose)
                ex.printStackTrace();            
            return null;
            
        }
        
    }      
    
}

class JMSMessage {
	
	public String JMSCorrelationID;
	public int JMSDeliveryMode;
	public String JMSDestination;
	public long JMSExpiration;
	public String JMSMessageID;
	public int JMSPriority;
	public boolean JMSRedelivered;
	public String JMSReplyTo;
	public long JMSTimestamp;
	public String JMSType;
	public String message;
	
	/**
	 * constructor
	 * @param JMSCorrelationID
	 * @param JMSDeliveryMode
	 * @param JMSDestination
	 * @param JMSExpiration
	 * @param JMSMessageID
	 * @param JMSPriority
	 * @param JMSRedelivered
	 * @param JMSReplyTo
	 * @param JMSTimestamp
	 * @param JMSType
	 * @param message
	 */
	public JMSMessage(String JMSCorrelationID, int JMSDeliveryMode, String JMSDestination,
			long JMSExpiration, String JMSMessageID, int JMSPriority, boolean JMSRedelivered,
			String JMSReplyTo, long JMSTimestamp, String JMSType, String message) {
		
		this.JMSCorrelationID = JMSCorrelationID;
		this.JMSDeliveryMode  = JMSDeliveryMode;
		this.JMSDestination   = JMSDestination;
		this.JMSExpiration    = JMSExpiration;
		this.JMSMessageID     = JMSMessageID;
		this.JMSPriority      = JMSPriority;
		this.JMSRedelivered   = JMSRedelivered;
		this.JMSReplyTo       = JMSReplyTo;
		this.JMSTimestamp     = JMSTimestamp;
		this.JMSType          = JMSType;
		this.message          = message;
		
	}
	
}
