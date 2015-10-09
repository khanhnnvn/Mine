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
    public Date dateAdd;

    LogEntry(int tool, IHttpRequestResponsePersisted requestResponse, URL url, String check, Date dateAdd)
    {
        this.tool = tool;
        this.requestResponse = requestResponse;
        this.url = url;
        this.check = check;
        this.status = "Pending";
        this.dateAdd = dateAdd;
    }
}
