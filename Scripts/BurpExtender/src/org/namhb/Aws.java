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
public class Aws {
    public String awsFolderPath = "C:\\Program Files (x86)\\Acunetix\\Web Vulnerability Scanner 10";
    public String saveFolderPath = "C:\\Users\\Public\\";
    public String url;
    public String tempFileName;
    public String crawlResult = null;
    public IBurpExtenderCallbacks callbacks;
    PrintWriter stdout, stderr;
    public String profile = "Sql_Injection";
    public Aws(IBurpExtenderCallbacks callbacks, String url, String tempFileName)
    {
        this.callbacks = callbacks;
        this.url = url;
        this.tempFileName = tempFileName;
        this.stdout = new PrintWriter(callbacks.getStdout(), true);
        this.stderr = new PrintWriter(callbacks.getStderr(), true);
    }
    public int createCrawlFile()
    {
        String cmd = awsFolderPath + "\\wvs_console.exe /Crawl " + this.url +" --GetFirstOnly=true /SaveFolder " + saveFolderPath + " /Import "+tempFileName;
        //stdout.println("Run Crawler: " + cmd);
        boolean crawlResult = false;
        String s = null;
        String crawlResultFileName = null;
        int start, end =0;
        try 
        {
            Process p = Runtime.getRuntime().exec(cmd);
            BufferedReader stdInput = new BufferedReader(new InputStreamReader(p.getInputStream()));
            BufferedReader stdError = new BufferedReader(new InputStreamReader(p.getErrorStream()));
            
            //Print output
            while((s = stdInput.readLine()) != null)
            {
                //stdout.println(s);
                if(s.equals("Crawling done."))
                {
                    stdout.println("Crawl finished!");
                    crawlResult = true;
                }
                if(crawlResult == true)
                {
                    if(s.startsWith("Saving to file"))
                    {
                       start = s.indexOf('"');
                       end = s.lastIndexOf('"');
                       crawlResultFileName = s.substring(start+1, end);
                    }
                }
            }
            if(p.exitValue() == 0)
            {
                stdout.println("Crawl Result file: " + crawlResultFileName);
                this.crawlResult = crawlResultFileName;
                return 1;
            }
            else
            {
                stdout.println("Crawl error!");
                return 0;
            }
        }
        catch (java.io.IOException io)
        {
            stderr.println("Check folder AWS path");
            return 0;
        }
        catch (Exception ex) {
            stderr.println("createCrawlFile "+ex.toString());
            return 0;
        }
        
    }
    public void start()
    {
        int crawlerResult = createCrawlFile();
        if (crawlerResult == 1)
        {
            stdout.println("Start scan");
            scan();
        }
        else
        {
            stdout.println("Stop scan!!!");
        }
        
    }
    public void scan()
    {
        boolean scanlResult = false;
        String cmd = awsFolderPath + "\\wvs_console.exe /ScanFromCrawl " + crawlResult + " /Profile " + profile + " /SaveFolder " + saveFolderPath + " /ExportXML /Verbose ";
        //stdout.println("Run Scanner: " + cmd);
        String s = null;
        try 
        {
            Process p = Runtime.getRuntime().exec(cmd);
            BufferedReader stdInput = new BufferedReader(new InputStreamReader(p.getInputStream()));
            BufferedReader stdError = new BufferedReader(new InputStreamReader(p.getErrorStream()));
            
            //Print output
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
    public void getResult()
    {
        
    }
}
