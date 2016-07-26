import java.util.ArrayList;

import java.sql.DriverManager;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.sql.SQLException;

/**
* Generic DB client
* Specific client libraries are located on classpath
* Tested clients - Oracle (ojdbc6.jar)
* 
* @author  Petr Rašek
* @version 0.2.0
* @since   2015-12-12 
*/
public class DBClient {
    
    /**********************************
              attributes
    **********************************/     
    
    private boolean verbose;
    private Connection conn;
    
    private String host;
    private String port;
    private String sid;
    private String user;
    private String passw;
    
    /**********************************
              constructors
    **********************************/ 
    
    /**
     * constructor
     * @param verbose 
     */
    public DBClient(boolean verbose) {
        
        this.verbose = verbose;
        
    }
    
    /**********************************
              methods
    **********************************/  
    
    /**
     * Connect to database
     * @param driver
     * @param connStr
     * @param user
     * @param passw
     * @return boolean
     */
    public boolean connect(String driver, String connStr, String user, String passw, int timeout) {
        
        try {
            
            if (conn != null) {
                
                System.out.println("INFO - Client is already connected to database");
                return false;
                
            }   
            
            if (verbose) {
                StringBuilder sb = new StringBuilder();
                sb.append("INFO - Connecting to database: driver:").append(driver).append(", connStr:").append(connStr);
                sb.append(", user:").append(user).append(", passw:").append(passw);
                System.out.println(sb.toString());
            }                         
            
            Class.forName(driver);
            DriverManager.setLoginTimeout(timeout);
            conn = DriverManager.getConnection(connStr, user, passw);            
            conn.setAutoCommit(false);
            
            if (verbose)
                System.out.println("INFO - Connected to database");  
            
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
    * Disconnect from database
    * @return boolean 
    */    
    public boolean disconnect() {
        
        try {
            
            if (conn == null) {
                
                System.out.println("INFO - Client is not connected to database");
                return false;
                
            }
            
            if (verbose)
                System.out.println("INFO - Disconnecting from database"); 
            
            conn.close();
            conn = null;
            
            if (verbose)
                System.out.println("INFO - Disconnected from database");             

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
    * Execute query
    * @param query
    * @param bindings
    * @param fetch_one
    * @return ArrayList<ArrayList<String>>
    */
    public ArrayList<ArrayList<String>> exec_query(String query, ArrayList<String> bindings, boolean fetch_one) {
        
        try {

            if (conn == null) {
                
                System.out.println("ERR - Client is not connected to database");
                return null;
                
            }  
            
            if (verbose) {
                StringBuilder sb = new StringBuilder();
                sb.append("INFO - Executing query: ").append(query).append(", bindings:").append(bindings);
                sb.append(", fetch_one:").append(fetch_one);
                System.out.println(sb.toString());
            }              
            
            PreparedStatement stmt = conn.prepareStatement(query);
            for (int i = 0; i < bindings.size(); i++)
                stmt.setString(i+1, bindings.get(i));
                
            ResultSet rs = stmt.executeQuery();
                       
            ArrayList<ArrayList<String>> rows = new ArrayList<ArrayList<String>>();
            ArrayList<String> row = new ArrayList<String>();
            
            try {
                
                ResultSetMetaData metadata  = rs.getMetaData();
            
                int colCnt = metadata.getColumnCount();
                for (int i = 0; i < colCnt; i++)
                    row.add(metadata.getColumnName(i+1));
            
                rows.add(row);
                
                boolean fetched = false;                
                while (!fetched && rs.next()) {
                
                    row = new ArrayList<String>();
                    for (int i = 0; i < colCnt; i++)
                        row.add(rs.getString(i+1));
                
                    rows.add(row);
                
                    if (fetch_one)
                        fetched = true;
                    
                }                
                
            }
            catch(SQLException ex) {
                
            }            
            
            rs.close();
            stmt.close();
            return rows;          
            
        }
        catch (Exception ex) {
            
            System.out.println("ERR - Exception: " + ex.toString());
            if (verbose)
                ex.printStackTrace();               
            return null;
            
        }
        
    }
    
    /**
    * Commit transaction
    */
    public boolean commit() {
    	
        try {

            if (conn == null) {
                
                System.out.println("ERR - Client is not connected to database");
                return false;
                
            } 
            
            conn.commit();
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
    * Rollback transaction
    */
    public boolean rollback() {
    	
        try {

            if (conn == null) {
                
                System.out.println("ERR - Client is not connected to database");
                return false;
                
            } 
            
            conn.rollback();
            return true;
            
        }
        catch (Exception ex) {

            System.out.println("ERR - Exception: " + ex.toString());
            if (verbose)
                ex.printStackTrace();               
            return false;
            
        }          
        
    }    
    
}
