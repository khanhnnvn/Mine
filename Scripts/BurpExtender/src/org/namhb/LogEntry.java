/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package org.namhb;

import burp.IHttpRequestResponsePersisted;
import java.net.URL;
import java.util.Date;

/**
 *
 * @author namhb1
 */
public class LogEntry {
    final int tool;
    final IHttpRequestResponsePersisted requestResponse;
    final URL url;
    final String check;
    public String status;
    public String debugLog;
    public Date dateAdd, finishTime;
    public String profile;
    public String hackable = "No";
    public int high, medium, low, info;

    LogEntry(int tool, IHttpRequestResponsePersisted requestResponse, URL url, String check, Date dateAdd)
    {
        this.tool = tool;
        this.requestResponse = requestResponse;
        this.url = url;
        this.check = check;
        this.status = "Pending";
        this.dateAdd = dateAdd;
        this.finishTime = null;
        this.debugLog = dateAdd.toString()+": Add to List";
        if(check.equals("SQL injection"))
        {
            this.profile = "Sql_Injection";
        }
        if(check.equals("Cross Site Sripting"))
        {
            this.profile = "XSS";
        }
        if(check.equals("File Inclusion"))
        {
            this.profile = "Sql_Injection";
        }
        this.high = 0;
        this.medium = 0;
        this.low = 0;
        this.info = 0;
    }
}
