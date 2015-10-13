/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package org.namhb;

import burp.IBurpExtenderCallbacks;
import burp.IExtensionHelpers;
import burp.IHttpRequestResponse;
import burp.IHttpRequestResponsePersisted;
import burp.IRequestInfo;
import java.io.*;

import java.net.InetAddress;
import java.nio.file.Files;
import java.util.Date;

/**
 *
 * @author namhb1
 */
public class Aws {
    public String awsFolderPath = "";
    public String saveFolderPath = "";
    public String tempFileName = "";
    public String tempFilePath = "";
    public String url;
    public String crawlResult = null;
    public IBurpExtenderCallbacks callbacks;
    public IExtensionHelpers helpers;
    PrintWriter stdout, stderr;
    public String profile = "Sql_Injection";
    public LogEntry logEntry;
    public Gui gui;
    public String stringTemplate = 
        "<?xml version=\"1.1\"?>\n" +
        "<!-- NOTE: Any NULL bytes in requests and responses are preserved within this output, even though this strictly breaks the XML syntax. If your XML parser rejects the NULL bytes then you will need to remove or replace these bytes before parsing. Alternatively, you can use the option to base64-encode requests and responses. -->\n" +
        "<!DOCTYPE items [\n" +
        "<!ELEMENT items (item*)>\n" +
        "<!ATTLIST items burpVersion CDATA \"\">\n" +
        "<!ATTLIST items exportTime CDATA \"\">\n" +
        "<!ELEMENT item (time, url, host, port, protocol, method, path, extension, request, status, responselength, mimetype, response, comment)>\n" +
        "<!ELEMENT time (#PCDATA)>\n" +
        "<!ELEMENT url (#PCDATA)>\n" +
        "<!ELEMENT host (#PCDATA)>\n" +
        "<!ATTLIST host ip CDATA \"\">\n" +
        "<!ELEMENT port (#PCDATA)>\n" +
        "<!ELEMENT protocol (#PCDATA)>\n" +
        "<!ELEMENT method (#PCDATA)>\n" +
        "<!ELEMENT path (#PCDATA)>\n" +
        "<!ELEMENT extension (#PCDATA)>\n" +
        "<!ELEMENT request (#PCDATA)>\n" +
        "<!ATTLIST request base64 (true|false) \"false\">\n" +
        "<!ELEMENT status (#PCDATA)>\n" +
        "<!ELEMENT responselength (#PCDATA)>\n" +
        "<!ELEMENT mimetype (#PCDATA)>\n" +
        "<!ELEMENT response (#PCDATA)>\n" +
        "<!ATTLIST response base64 (true|false) \"false\">\n" +
        "<!ELEMENT comment (#PCDATA)>\n" +
        "]>\n" +
        "<items burpVersion=\"1.6.25\" exportTime=\"%s\">\n" +
        "  <item>\n" +
        "    <time>%s</time>\n" +
        "    <url><![CDATA[%s]]></url>\n" +
        "    <host ip=\"%s\">%s</host>\n" +
        "    <port>%d</port>\n" +
        "    <protocol>%s</protocol>\n" +
        "    <method>%s</method>\n" +
        "    <path><![CDATA[%s]]></path>\n" +
        "    <extension>null</extension>\n" +
        "    <request base64=\"false\"><![CDATA[%s" +
        "]]></request>\n" +
        "    <status></status>\n" +
        "    <responselength></responselength>\n" +
        "    <mimetype></mimetype>\n" +
        "    <response base64=\"false\"></response>\n" +
        "    <comment></comment>\n" +
        "  </item>\n" +
        "</items>";
    public Aws(IBurpExtenderCallbacks callbacks, IExtensionHelpers helpers, String url, LogEntry logEntry, Gui gui, String acunetixPath, String tempfolderPath, String tempfileName)
    {
        this.callbacks = callbacks;
        this.helpers = helpers;
        this.url = url;
        this.logEntry = logEntry;
        this.gui = gui;
        this.awsFolderPath = acunetixPath;
        this.saveFolderPath = tempfolderPath;
        this.tempFileName = tempfileName;
        this.tempFilePath = tempfolderPath + "//" + tempfileName;
        this.stdout = new PrintWriter(callbacks.getStdout(), true);
        this.stderr = new PrintWriter(callbacks.getStderr(), true);
        //*Delete req.tmp
        try
        {
            File f1 = new File(tempFilePath);
            if(f1.exists())
            {
                f1.delete();
                this.callbacks.issueAlert("Found req.tmp file, delete before scan!");
            }
            else
            {
                
            }
        }
        catch(Exception e)
        {
            stdout.println("Error: "+e.toString());
        }
        //*Delete xml before scan
        String exportFile = this.saveFolderPath + "//export.xml";
        try
        {
            File f = new File(exportFile);
            if(f.exists())
            {
                f.delete();
            }
            else
            {
                this.callbacks.issueAlert("File export.xml not found!");
            }
        }
        catch(Exception e)
        {
            stdout.println("Error: "+e.toString());
        }
    }
    public int saveToFile(String req)
    {
        try
        {
            try (FileWriter fw = new FileWriter(tempFilePath)) {
                fw.write(req);
                fw.close();
                this.stdout.println("Saved to file: "+tempFilePath);
                return 1;
            }
        }
        catch (java.io.FileNotFoundException fe)
        {
            //Send to alert
            callbacks.issueAlert("File access Permisson: "+tempFilePath);
            return 0;
        }
        catch (Exception e)
        {
            this.stderr.println(e.getStackTrace());
            return 0;
        }

    }
    public void saveFile(IHttpRequestResponsePersisted messageInfo)
    {
        try {
            //Get current time
            Date now = new Date();
            String time = now.toString();
            //Get URL
            IRequestInfo reqInfo = this.helpers.analyzeRequest(messageInfo);
            String url = reqInfo.getUrl().toString();
            //Get domain
            String host = messageInfo.getHttpService().getHost();
            //Get IP
            InetAddress address = InetAddress.getByName(host);
            String ip = address.getHostAddress();
            //Get port, protocol, method
            int port = messageInfo.getHttpService().getPort();
            String protocol = messageInfo.getHttpService().getProtocol();
            String method = reqInfo.getMethod();
            //Get request
            IHttpRequestResponsePersisted requestResponse = this.callbacks.saveBuffersToTempFiles(messageInfo);
            //Get path
            String path = reqInfo.getUrl().getPath();
            //Get request
            String req = new String(requestResponse.getRequest(), "UTF-8");
            String result = String.format(
                    stringTemplate, 
                    time, 
                    time,
                    url,
                    ip,
                    host,
                    port,
                    protocol,
                    method,
                    path,
                    req                 
            );
            //System.out.println(result);
            //gui.addDebugLog(logEntry, result);
            
            //Save to file
            int ret = saveToFile(result);
            if(ret == 1)
            {
                start();
            }
            else
            {
                this.stdout.println("File writer error, check stderr log!");
            }
        } catch (Exception ex) 
        {
            this.stderr.println(ex.getStackTrace());
        }
    }
    public int createCrawlFile()
    {
        String cmd = awsFolderPath + "\\wvs_console.exe /Crawl \"" + this.url +"\" --GetFirstOnly=true /SaveFolder " + saveFolderPath + " /Import "+tempFilePath;
        stdout.println("Run Crawler: " + cmd);
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
                    gui.addDebugLog(logEntry, s);
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
        //Set status
        gui.updateStatus(logEntry, "Crawling");
        int crawlerResult = createCrawlFile();
        if (crawlerResult == 1)
        {
            stdout.println("Start scan");
            gui.addDebugLog(logEntry, "Start scan");
            gui.updateStatus(logEntry, "Scanning");
            //Delete req.tmp file
            try
            {
                File f = new File(tempFilePath);
                if(f.exists())
                {
                    f.delete();
                }
                else
                {
                    this.callbacks.issueAlert("File "+tempFilePath+" not found!");
                }
            }
            catch(Exception e)
            {
                stdout.println("Error: "+e.toString());
            }
            scan();
        }
        else
        {
            stdout.println("Stop scan!!!");
            gui.addDebugLog(logEntry, "Stop scan!!!");
        }
    }
    public void scan()
    {
        boolean scanlResult = false;
        String cmd = awsFolderPath + "\\wvs_console.exe /ScanFromCrawl " + crawlResult + " /Profile " + logEntry.profile + " /SaveFolder " + saveFolderPath + " /ExportXML /Verbose ";
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
                gui.addDebugLog(logEntry, s);
                if(s.startsWith("[high]"))
                {
                    gui.updatevulnerability(logEntry, 1);
                }
                if(s.startsWith("[medium]"))
                {
                    gui.updatevulnerability(logEntry, 2);
                }
                if(s.startsWith("[low]"))
                {
                    gui.updatevulnerability(logEntry, 3);
                }
                if(s.startsWith("[info]"))
                {
                    gui.updatevulnerability(logEntry, 4);
                }
                if(s.startsWith("Progress:"))
                {
                    int startx = s.indexOf(":");
                    int endx = s.indexOf("%");
                    String proc = s.substring(startx+2, endx);
                    gui.updateProcess(logEntry, Integer.parseInt(proc));
                }
                gui.updateSiteAndAwsPanel(logEntry);
            }
            
        }
        catch (java.io.IOException io)
        {
            stderr.println("Check folder AWS path");
        }
        catch (Exception ex) {
            stderr.println("createCrawlFile "+ex.toString());
        }
        //Delete craw file
        try
        {
            File f = new File(crawlResult);
            if(f.exists())
            {
                f.delete();
            }
            else
            {
                this.callbacks.issueAlert("File "+crawlResult+" not found!");
            }
        }
        catch(Exception e)
        {
            stdout.println("Error: "+e.toString());
        }
    }
    public void getResult()
    {
        
    }
}
