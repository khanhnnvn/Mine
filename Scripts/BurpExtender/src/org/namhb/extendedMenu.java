/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package org.namhb;

import java.io.FileWriter;
import java.net.InetAddress;
import java.util.Date;
import java.io.PrintWriter;
import burp.*;
/**
 *
 * @author habachnam
 */
public class extendedMenu implements IMenuItemHandler {
    public IBurpExtenderCallbacks callbacks;
    public IExtensionHelpers helpers;
    public String tempFileName = "C:\\Users\\Public\\req.tmp";
    PrintWriter stdout, stderr;
    public String stringTemplate = "<?xml version=\"1.1\"?>\n" +
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
    public extendedMenu(IBurpExtenderCallbacks callbacks, IExtensionHelpers helpers)
    {
        super();
        this.callbacks = callbacks;
        this.helpers = helpers;
        //stdout and stderr
        this.stdout = new PrintWriter(callbacks.getStdout(), true);
        this.stderr = new PrintWriter(callbacks.getStderr(), true);
        this.stdout.println("Custom menu loaded!!!");
    }
    public int saveToFile(String req)
    {
        try
        {
            try (FileWriter fw = new FileWriter(tempFileName)) {
                fw.write(req);
                fw.close();
                this.stdout.println("Saved to file: "+tempFileName);
                return 1;
            }
        }
        catch (java.io.FileNotFoundException fe)
        {
            //Send to alert
            callbacks.issueAlert("File access Permisson: "+tempFileName);
            return 0;
        }
        catch (Exception e)
        {
            this.stderr.println(e.getStackTrace());
            return 0;
        }

    }
    public void saveFile(IHttpRequestResponse messageInfo)
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
            //Save to file
            int ret = saveToFile(result);
            if(ret == 1)
            {
                aws aws = new aws(callbacks, url, tempFileName);
                aws.start();
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
    @Override
    public void menuItemClicked(String menuItemCaption, IHttpRequestResponse[] messageInfo) {
        //throw new UnsupportedOperationException("Not supported yet."); //To change body of generated methods, choose Tools | Templates.
        try
        {
            //messageInfo
            if(messageInfo.length == 1)
            {
               saveFile(messageInfo[0]);
            }
            else
            {
                callbacks.issueAlert("Select 1 request only!");
            }
           
        }
        catch(Exception e)
        {   
            this.stderr.println(e.getStackTrace());
        }
    }
}
