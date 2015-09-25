/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package org.namhb;

import burp.IBurpExtenderCallbacks;
import java.io.*;

/**
 *
 * @author namhb1
 */
public class aws {
    public String awsFolderPath = "";
    public String url;
    public String tempFileName;
    public IBurpExtenderCallbacks callbacks;
    PrintWriter stdout, stderr;
    public aws(IBurpExtenderCallbacks callbacks, String url, String tempFileName)
    {
        this.callbacks = callbacks;
        this.url = url;
        this.tempFileName = tempFileName;
        this.stdout = new PrintWriter(callbacks.getStdout(), true);
        this.stderr = new PrintWriter(callbacks.getStderr(), true);
    }
    public void createCrawlFile()
    {
        String cmd = "c:\\Windows\\System32\\more.com "+tempFileName;
        String s = null;
        try 
        {
            Process p = Runtime.getRuntime().exec(cmd);
            BufferedReader stdInput = new BufferedReader(new InputStreamReader(p.getInputStream()));
            BufferedReader stdError = new BufferedReader(new InputStreamReader(p.getErrorStream()));
            
            //Print output
            stderr.println("Command Result: ");
            while((s = stdInput.readLine()) != null)
            {
                stdout.println(s);
            }
        }
        catch (java.io.IOException io)
        {
            stderr.println("Check folder AWS path");
        }
        catch (Exception ex) {
            stderr.println("createCrawlFile "+ex.toString());
        }
    }
    public void startScan()
    {
        
    }
    public void getResult()
    {
        
    }
}
